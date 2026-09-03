## 1. 第一阶段：直觉驱动的暴力解法

### 1.1 初始思路

拿到“两数之和”的题目，最直观的解法就是双重循环。遍历数组中的每一个元素，再遍历它后面的所有元素，判断两者之和是否等于目标值 `target`。

### 1.2 第一版代码（错误示范）

```c
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    if( numsSize<2)
        return; // 隐患1：返回值类型不匹配
    int i = 0;
    int j = 0;
    for(i=0;i<numsSize;i++) {
        for(j=i+1;j<numsSize;j++) {
            if(nums[i]+nums[j]==target)
                return [i,j]; // 致命错误：C语言没有这种数组字面量语法
        }
    }
}
```

### 1.3 问题剖析

1. **语法误区**：习惯了 Python 等高级语言，误以为 C 语言也能用 `[i, j]` 直接返回一个列表。
2. **类型不匹配**：函数签名要求返回 `int*`（指针），但 `return;` 没有返回值，且空返回在指针函数中是非法的。

## 2. 第二阶段：局部数组的陷阱

### 2.1 修正思路

既然不能直接返回 `[i, j]`，那我可以在函数内部先定义一个数组，把 `i` 和 `j` 存进去，然后再把这个数组返回出去。

### 2.2 第二版代码（依然错误）

```c
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    if(numsSize<2)
        return; // 隐患1：依然没有处理空返回
    int i = 0;
    int j = 0;
    int result[2]={0}; // 隐患2：局部数组
    for(i=0;i<numsSize;i++) {
        for(j=i+1;j<numsSize;j++) {
            if(nums[i]+nums[j]==target) {
                result[0]=i;
                result[1]=j;
                return result; // 致命错误：返回了局部变量的地址
            }
        }
    }
}
```

### 2.3 问题剖析

这一版代码在逻辑上看似通顺，但触犯了 C 语言最核心的内存规则：

- **栈区内存的生命周期**：`int result[2]` 是局部变量，分配在栈区（Stack）。当函数执行完毕，栈帧被销毁，这块内存会被系统自动回收。
- **悬垂指针（Dangling Pointer）**：将这块已经被销毁的内存地址返回给调用者，调用者再去访问时，要么读到乱码，要么直接导致程序崩溃（Segmentation Fault）。

## 3. 第三阶段：拥抱堆区与动态内存分配

### 3.1 核心顿悟

既然栈区的内存会在函数结束时被回收，那我只需要把结果存到**堆区（Heap）**。堆区的内存只要不被手动释放，就会一直存在。C 语言提供了 `malloc` 函数来实现这一点。

同时，我重新审视了力扣的函数签名：
`int* twoSum(int* nums, int numsSize, int target, int* returnSize)`
这里的 `returnSize` 是一个指针，力扣需要通过它来知道返回的数组到底有几个元素。我必须通过 `*returnSize = 2;` 来给它赋值。

### 3.2 最终版代码（正确解法）

```c
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    int i, j;
    // 1. 在堆区动态分配能容纳2个整数的内存
    int* result = malloc(sizeof(int) * 2);

    for(i = 0; i < numsSize; i++) {
        for(j = i + 1; j < numsSize; j++) {
            if(nums[i] + nums[j] == target) {
                result[0] = i;
                result[1] = j;
                *returnSize = 2; // 2. 告诉外部数组长度为2
                return result;   // 3. 返回堆区指针，安全！
            }
        }
    }

    // 4. 遍历完没找到答案的处理
    *returnSize = 0;
    return result; 
}
```

### 3.3 细节完善

- **内存安全**：使用 `malloc` 成功解决了悬垂指针问题。
- **契约精神**：正确使用了 `returnSize` 参数，满足了接口契约。
- **工程习惯**：在实际工程中，`malloc` 之后最好加上 `if (result == NULL)` 的判空处理，以防内存分配失败。同时别忘了 `#include <stdlib.h>`。

---

## 4. 总结与反思

通过这道简单的“两数之和”，我深刻体会到了 C 语言“把控制权完全交给程序员”的设计哲学：

1. **不要想当然**：高级语言的语法糖（如直接返回数组）在 C 语言中是不存在的，必须理解底层的内存模型。
2. **栈与堆的区别**：局部变量在栈上，随函数生灭；动态分配在堆上，由程序员掌控生命周期。
3. **接口契约**：写代码不仅是实现逻辑，还要严格遵守函数签名定义的规则（如 `returnSize` 的赋值）。

# LeetCode 1：Two Sum —— C语言哈希表解法学习记录

## 一、从暴力法转向哈希法

Two Sum 最开始使用的是双重循环暴力搜索：

```text
遍历第一个数字
    ↓
遍历它后面的所有数字
    ↓
判断两个数字之和是否等于 target
```

这种方法比较容易理解，但是时间复杂度是：

```text
O(n²)
```

因为对于每一个 `nums[i]`，都需要继续遍历后面的元素。

后来开始思考：

> 如果我已经遍历过一个数字，能不能把它保存起来？
> 下一次需要寻找它的时候，直接查找，而不是重新遍历？

于是开始尝试使用哈希表。

---

# 二、哈希法的核心思路

假设：

```text
nums = [2, 7, 11, 15]
target = 9
```

遍历到：

```text
nums[i] = 2
```

那么需要寻找：

```text
need = target - nums[i]
     = 9 - 2
     = 7
```

此时检查哈希表：

```text
之前有没有出现过 7？
```

如果没有，就把当前数字保存起来：

```text
2 → 下标 0
```

继续遍历。

当遍历到：

```text
nums[i] = 7
```

计算：

```text
need = 9 - 7
     = 2
```

此时哈希表中已经存在：

```text
2 → 下标 0
```

因此直接得到：

```text
[0, 1]
```

所以哈希法的核心流程是：

```text
当前数字
    ↓
计算 need = target - 当前数字
    ↓
去哈希表查找 need
    ↓
找到了？
  ↓       ↓
 是       否
 ↓        ↓
返回     保存当前数字和下标
```

最重要的一个顺序：

> **先查，再存。**

不能先存当前数字再查，否则可能把当前数字自己当成答案。

例如：

```text
nums = [3, 3]
target = 6
```

如果先存：

```text
hash[3] = 0
```

然后马上查 `need = 3`，就会误认为已经找到了另一个 `3`。

---

# 三、第一次尝试：简单数组模拟哈希表

最开始想到的是：

```c
int hash[numsSize];
```

希望通过：

```text
hash[数字] = 下标
```

来记录数字的位置。

例如：

```text
2 → 0
7 → 1
11 → 2
```

然后通过：

```c
hash[need]
```

直接找到下标。

但是这里很快发现一个问题：

如果：

```c
int hash[4];
```

那么只能访问：

```text
hash[0] ~ hash[3]
```

而 `nums` 中的数字可能远远大于数组长度，甚至可能是负数。

因此不能简单地使用：

```c
hash[nums[i]]
```

---

# 四、第一次哈希版本

当时尝试：

```c
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {

    #define size 10001

    int* result=malloc(sizeof(int)*2);

    int hash[size]={0};

    int i=0,need=0;

    for(i=0;i<numsSize;i++)
    {
        need=target-nums[i];

        if()
    }

}
```

## 当时卡住的地方

主要卡在：

```c
if()
```

不知道如何判断：

> `need` 是否已经存在于哈希表中。

后来明确了哈希表实际上要保存：

```text
数字 → 下标
```

而不是单纯保存数字。

例如：

```text
hash 中：

2 → 0
7 → 1
```

这样找到 `need = 2` 时，就能得到它对应的下标 `0`。

---

# 五、第二次尝试：开始真正使用 hash

代码：

```c
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {

    #define size 10001

    int* result=malloc(sizeof(int)*2);

    int hash[size];

    int i=0,need=0;

    for(i=0;i<numsSize;i++)
    {
        need=target-nums[i];

        hash[nums[i]]=i;

        if(hash[need]>=0)
        {
            result[0]=i;
            result[1]=hash[need];

            *returnSize=2;

            return result;
        }
    }

    *returnSize=0;
    return result;
}
```

## 🟠 问题 1：先存后查

当时写成：

```c
hash[nums[i]]=i;

if(hash[need]>=0)
```

这是错误的逻辑。

应该：

```text
先查 need
↓
没找到
↓
再存 nums[i]
```

原因是防止当前元素和自己匹配。

---

# 六、第三次尝试：解决 hash 初始化

修改后：

```c
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {

    #define size 10001

    int* result=malloc(sizeof(int)*2);

    int hash[size];

    memset(hash,-1,size);

    int i=0,need=0;

    for(i=0;i<numsSize;i++)
    {
        need=target-nums[i];

        if(hash[need]>=0)
        {
            result[0]=i;
            result[1]=hash[need];

            *returnSize=2;

            return result;
        }

        hash[nums[i]]=i;
    }

    *returnSize=0;
    return result;
}
```

## 🔴 发现 `memset` 的问题

原来写：

```c
memset(hash, -1, size);
```

这里第三个参数表示：

> **字节数**

而不是：

> `int` 的个数。

所以应该写：

```c
memset(hash, -1, size * sizeof(int));
```

后来改成：

```c
memset(hash,-1,size*sizeof(int));
```

这样才是把整个数组初始化。

---

# 七、第四次尝试：解决数字过大和负数

发现：

```c
hash[nums[i]]
```

仍然有问题。

例如：

```text
nums[i] = -5
```

就会变成：

```c
hash[-5]
```

数组下标不能这样使用。

于是开始尝试通过取模把数字转换成哈希数组下标：

```c
nums[i] % size
```

代码：

```c
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {

    #define size 10001

    int* result=malloc(sizeof(int)*2);

    int hash[size];

    memset(hash,-1,size*sizeof(int));

    int i=0,need=0;

    for(i=0;i<numsSize;i++)
    {
        need=target-nums[i];

        if(hash[need%size]>=0)
        {
            result[0]=i;
            result[1]=hash[need];

            *returnSize=2;

            return result;
        }

        hash[nums[i]%size]=i;
    }

    *returnSize=0;
    return result;
}
```

---

# 八、理解负数取模

这里第一次真正遇到了：

```c
-5 % 10001
```

在 C 中结果仍然可能是负数。

例如：

```c
-7 % 3
```

结果是：

```text
-1
```

所以：

```c
hash[nums[i] % size]
```

仍然可能变成：

```c
hash[-5]
```

依然会数组越界。

---

# 九、解决负数哈希下标

后来理解了这个公式：

```c
((x % size) + size) % size
```

它的作用是：

> 无论 `x` 是正数还是负数，都把最终结果限制在 `0 ~ size-1`。

例如：

```text
x = -17
size = 10
```

计算：

```text
-17 % 10 = -7
-7 + 10 = 3
3 % 10 = 3
```

最终：

```text
-17 → 3
```

因此修改成：

```c
int index = ((need % size) + size) % size;
```

以及：

```c
index = ((nums[i] % size) + size) % size;
```

---

# 十、第五次尝试：开始处理哈希冲突

代码：

```c
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    #define size 10001

    int* result=malloc(sizeof(int)*2);

    int hash[size];

    memset(hash,-1,size*sizeof(int));

    int i=0,need=0;

    for(i=0;i<numsSize;i++)
    {
        need=target-nums[i];

        int index=((need%size)+size)%size;

        if(hash[index]>=0)
        {
            result[0]=i;
            result[1]=hash[index];

            *returnSize=2;

            return result;
        }

        while(hash[index]>=0)
        {
           i++;
        }

        hash[index]=i;
    }

    *returnSize=0;
    return result;
}
```

## 🔴 这里又出现一个问题

当哈希位置被占用时，当时写的是：

```c
while(hash[index]>=0)
{
    i++;
}
```

后来发现：

> **这里应该移动的是 `index`，而不是 `i`。**

因为：

```text
i
```

表示：

> 当前正在遍历 `nums` 的第几个元素。

而：

```text
index
```

表示：

> 当前正在访问哈希表的哪个位置。

两者完全不是一回事。

所以解决哈希冲突应该是：

```c
index = (index + 1) % size;
```

而不是：

```c
i++;
```

这就是**线性探测**。

---

# 十一、进一步理解哈希冲突

即使使用：

```c
index = (index + 1) % size;
```

还发现一个更深的问题。

例如：

```text
size = 10
```

那么：

```text
1 % 10 = 1
11 % 10 = 1
21 % 10 = 1
```

不同的数字可能映射到同一个位置。

这叫：

> **哈希冲突（Hash Collision）**

因此：

```c
int hash[size];
```

只保存：

```text
下标
```

是不够的。

必须同时知道：

```text
这个位置存的到底是什么数字？
这个数字原来的下标是多少？
这个位置是否被使用？
```

于是开始使用结构体。

---

# 十二、最终自己写出的哈希表版本

```c
/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    #define size 100001

    int* result=malloc(sizeof(int)*2);

    typedef struct {
        int index;
        int key;
        int used;
    }HashNode;

    HashNode hash[size]={0};

    int i=0;

    for(i=0;i<numsSize;i++)
    {
        int need=target-nums[i];

        int index=(need%size+size)%size;

        while(hash[index].used)
        {
            if(hash[index].key=need)
            {
                result[0]=i;
                result[1]=hash[index].index;

                *returnSize=2;

                return result;
            }

            index=(index+1)%size;
        }

        index=(nums[i]%size+size)%size;

        while(hash[index].used)
        {
            index=(index+1)%size;
        }

        hash[index].used=1;
        hash[index].key=nums[i];
        hash[index].index=i;
    }

    *returnSize=0;
    return result;
}
```

---

# 十三、最终发现的错误：`=` 和 `==`

最后只剩下一个关键的 C 语言错误：

```c
if(hash[index].key=need)
```

这里：

```text
=   → 赋值
==  → 判断是否相等
```

所以应该改成：

```c
if(hash[index].key == need)
```

例如：

```c
a = 10;
```

表示：

> 把 10 赋值给 a。

而：

```c
a == 10
```

表示：

> 判断 a 是否等于 10。

这是 C 语言非常重要的基础知识。

---

# 十四、最终正确版本

按照这次学习的思路，最终版本可以写成：

```c
/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {

    #define SIZE 100001

    typedef struct {
        int index;
        int key;
        int used;
    } HashNode;

    int* result = malloc(sizeof(int) * 2);

    HashNode hash[SIZE] = {0};

    for(int i = 0; i < numsSize; i++)
    {
        int need = target - nums[i];

        int index = ((need % SIZE) + SIZE) % SIZE;

        // 查找 need
        while(hash[index].used)
        {
            if(hash[index].key == need)
            {
                result[0] = hash[index].index;
                result[1] = i;

                *returnSize = 2;

                return result;
            }

            // 哈希冲突，向后寻找
            index = (index + 1) % SIZE;
        }

        // 没找到，把当前数字存入哈希表
        index = ((nums[i] % SIZE) + SIZE) % SIZE;

        while(hash[index].used)
        {
            index = (index + 1) % SIZE;
        }

        hash[index].key = nums[i];
        hash[index].index = i;
        hash[index].used = 1;
    }

    *returnSize = 0;
    return result;
}
```

---

# 十五、这次学习遇到的坑总结

| 问题                     | 原因                   | 解决办法                         |
| ---------------------- | -------------------- | ---------------------------- |
| 不知道 `if()` 怎么写         | 没理解哈希表存什么            | 存 `数字 → 下标`                  |
| 先存再查                   | 会把自己当成答案             | **先查，后存**                    |
| `memset(hash,-1,size)` | `size` 是元素数量，不是字节数   | `size * sizeof(int)`         |
| `hash[nums[i]]`        | 数字可能很大或为负数           | 使用哈希函数                       |
| `%` 后出现负数              | C 中负数取模结果可以为负        | `((x % size) + size) % size` |
| 哈希冲突                   | 不同数字可能映射到相同位置        | 线性探测                         |
| `while` 中写 `i++`       | `i` 是 nums 下标，不是哈希位置 | `index = (index + 1) % size` |
| 只保存 index              | 冲突后无法判断是不是目标数字       | 保存 `key + index + used`      |
| `=` 和 `==` 混淆          | C 语法基础问题             | `=` 赋值，`==` 判断               |
| 哈希表太大放栈上               | 局部数组占用栈空间            | 可以进一步改成动态内存                  |

---

# 十六、最终理解

这次真正学到的不是某一份 Two Sum 代码，而是哈希表的基本思想：

```text
                  Two Sum
                     ↓
          target - nums[i] = need
                     ↓
             查找 need
                     ↓
        ┌────────────┴────────────┐
        ↓                         ↓
      找到                       没找到
        ↓                         ↓
   返回两个下标             保存 nums[i]
                                  ↓
                              key + index
                                  ↓
                            哈希函数映射
                                  ↓
                            发生冲突？
                           ↓           ↓
                          否           是
                          ↓            ↓
                         存       线性探测
                                       ↓
                              index = index + 1
```

最终复杂度：

```text
平均时间复杂度：O(n)

空间复杂度：O(n)
```

相比最开始的暴力法：

```text
暴力法：O(n²)
哈希法：平均 O(n)
```

## 这次最值得记住的 5 个知识点

```text
1. 哈希表本质：通过 key 快速找到 value

2. Two Sum：
   need = target - nums[i]

3. 处理顺序：
   先查 need → 再存当前 nums[i]

4. 哈希冲突：
   不同 key 可能映射到相同位置
   可以使用线性探测解决

5. C 语言：
   = 赋值
   == 判断相等
```

# C++暴力法
和C没什么区别，需要的注意的地方主要是对vector的用法与理解
## 1. vector

```cpp
vector<int>
```

可以理解成：

> C++ 中的动态数组。

例如：

```cpp
vector<int> nums = {2, 7, 11, 15};
```

---

## 2. vector 的下标访问

和 C 数组一样：

```cpp
nums[0]
nums[1]
nums[2]
```

---

## 3. vector 的长度

C：

```c
numsSize
```

C++：

```cpp
nums.size()
```

---

## 4. vector 直接返回

C：

```c
int* result = malloc(...);
result[0] = i;
result[1] = j;
return result;
```

C++：

```cpp
return {i, j};
```

---

## 5. 空 vector

```cpp
return {};
```

表示：

```text
[]
```

---

# LeetCode 1：Two Sum —— C++ 哈希表学习总结

## 一、从 C 暴力法到 C++ 哈希法

Two Sum 最开始使用的是暴力法：

```text
固定 nums[i]
    ↓
遍历后面的 nums[j]
    ↓
判断 nums[i] + nums[j] == target
```

时间复杂度：

```text
O(n²)
```

后来学习 C 哈希表时，将问题转换成：

```text
当前数字 nums[i]
       ↓
need = target - nums[i]
       ↓
哈希表中有没有 need？
       ↓
有 → 直接找到答案
没有 → 保存当前数字和下标
```

时间复杂度降低到平均：

```text
O(n)
```

到了 C++，不需要像 C 一样自己实现 `HashNode`、哈希函数、冲突处理、线性探测。

C++ 标准库提供了：

```cpp
unordered_map
```

可以直接使用。

---

# 二、unordered_map 是什么？

`unordered_map` 是 C++ 标准库提供的**哈希表容器**。

基本形式：

```cpp
unordered_map<key类型, value类型> 哈希表名称;
```

例如：

```cpp
unordered_map<int, int> hash;
```

表示：

```text
key       value
int       int
```

在 Two Sum 中：

```text
key   = 数组中的数字
value = 这个数字对应的下标
```

例如：

```text
2  → 0
7  → 1
11 → 2
15 → 3
```

所以：

```cpp
hash[2] = 0;
hash[7] = 1;
```

---

# 三、为什么叫 unordered_map？

C++ 里面有两个容易混淆的容器：

```cpp
map
unordered_map
```

它们都可以理解成：

> key → value

但是底层实现不同。

### map

通常基于红黑树。

特点：

```text
key 会按照顺序排列
```

例如：

```text
1 → ...
3 → ...
5 → ...
8 → ...
```

查找复杂度：

```text
O(log n)
```

---

### unordered_map

基于哈希表。

特点：

```text
不保证 key 的顺序
```

例如遍历的时候可能出现：

```text
7 → ...
2 → ...
15 → ...
11 → ...
```

不一定按照大小排列。

平均查找：

```text
O(1)
```

所以 Two Sum 非常适合：

```cpp
unordered_map<int, int>
```

---

# 四、创建 unordered_map

最基本：

```cpp
unordered_map<int, int> hash;
```

例如：

```cpp
unordered_map<string, int> age;
```

表示：

```text
string → int
```

可以存：

```text
"Tom" → 18
"Jack" → 21
```

还可以：

```cpp
unordered_map<int, string> student;
```

表示：

```text
int → string
```

例如：

```text
1 → "Tom"
2 → "Jack"
```

所以：

```cpp
unordered_map<键类型, 值类型>
```

是一个非常重要的语法。

---

# 五、Two Sum 中的核心定义

你的代码：

```cpp
unordered_map<int, int> hash;
```

实际上定义的是：

```text
数字 → 下标
```

例如遍历：

```text
nums = [2, 7, 11, 15]
```

经过几次保存后：

```text
hash

2  → 0
7  → 1
11 → 2
15 → 3
```

这就对应了你之前 C 语言自己定义的：

```cpp
typedef struct {
    int index;
    int key;
    int used;
} HashNode;
```

C 需要自己维护：

```text
key
index
used
```

C++：

```cpp
unordered_map<int, int>
```

这些事情由容器帮你处理。

---

# 六、插入数据

最常见的写法：

```cpp
hash[key] = value;
```

例如：

```cpp
hash[2] = 0;
```

表示：

```text
2 → 0
```

Two Sum 中：

```cpp
hash[nums[i]] = i;
```

意思就是：

> 把当前数字 `nums[i]` 和它的下标 `i` 保存到哈希表。

例如：

```text
i = 0
nums[i] = 2
```

执行：

```cpp
hash[nums[i]] = i;
```

实际上就是：

```cpp
hash[2] = 0;
```

---

# 七、通过 key 获取 value

例如：

```cpp
hash[2]
```

如果之前保存：

```cpp
hash[2] = 0;
```

那么：

```cpp
hash[2]
```

得到：

```text
0
```

所以 Two Sum：

```cpp
return {hash[need], i};
```

就是：

```text
hash[need] → 之前保存的下标
i          → 当前下标
```

---

# 八、find()：查找 key

这是你这次最重要的新语法之一：

```cpp
hash.find(need)
```

表示：

> 在 `hash` 中寻找 key 为 `need` 的元素。

但是 `find()` **不是直接返回 value**。

它返回的是一个：

```text
iterator（迭代器）
```

目前可以先把迭代器简单理解成：

> “指向哈希表某个元素的位置”。

---

# 九、为什么要和 end() 比较？

你写的是：

```cpp
if(hash.find(need) != hash.end())
```

这句话非常重要。

可以拆开：

```cpp
hash.find(need)
```

↓

去找 `need`

如果找到：

```text
指向找到的元素
```

如果没找到：

```text
返回 hash.end()
```

所以：

```cpp
hash.find(need) != hash.end()
```

表示：

> **找到了 `need`。**

而：

```cpp
hash.find(need) == hash.end()
```

表示：

> **没有找到 `need`。**

---

# 十、为什么不能直接写 hash[need] 判断？

这是 C++ 哈希非常重要的一个坑。

例如：

```cpp
if(hash[need])
```

看起来好像是在判断：

> `need` 是否存在。

实际上不可靠。

因为：

```cpp
hash[need]
```

如果 `need` 不存在，`unordered_map` 可能会**自动创建这个 key**，并给它一个默认值。

例如：

```cpp
unordered_map<int, int> hash;

cout << hash[10];
```

原来没有 `10`。

访问：

```cpp
hash[10]
```

以后，可能已经变成：

```text
10 → 0
```

所以：

> `operator[]` 不适合单纯判断 key 是否存在。

判断存在性推荐：

```cpp
hash.find(key) != hash.end()
```

或者：

```cpp
hash.count(key)
```

---

# 十一、count()：判断 key 是否存在

另一个非常常用的写法：

```cpp
hash.count(need)
```

对于 `unordered_map`：

```text
存在 → 1
不存在 → 0
```

所以可以写：

```cpp
if(hash.count(need))
{
    return {hash[need], i};
}
```

这和：

```cpp
if(hash.find(need) != hash.end())
```

在这里的效果类似。

### 两种写法

```cpp
if(hash.find(need) != hash.end())
```

或者：

```cpp
if(hash.count(need))
```

初学阶段可以优先记：

```text
find() → 查找
count() → 判断有没有
```

---

# 十二、你的 C++ Two Sum 完整代码

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {

        unordered_map<int, int> hash;

        for(int i = 0; i < nums.size(); i++)
        {
            int need = target - nums[i];

            if(hash.find(need) != hash.end())
            {
                return {hash[need], i};
            }

            hash[nums[i]] = i;
        }

        return {};
    }
};
```

---


# 十三、为什么必须先查再存？

你的代码：

```cpp
if(hash.find(need) != hash.end())
{
    return {hash[need], i};
}

hash[nums[i]] = i;
```

顺序是：

```text
① 查找
② 保存
```

这个顺序非常重要。

例如：

```text
nums = [3, 3]
target = 6
```

第一次：

```text
3 → need = 3
```

哈希表为空：

```text
找不到
```

然后保存：

```text
3 → 0
```

第二次：

```text
3 → need = 3
```

现在找到：

```text
3 → 0
```

返回：

```text
[0,1]
```

如果先保存：

```cpp
hash[nums[i]] = i;
```

再查找：

```cpp
hash.find(need)
```

第一次就可能找到自己：

```text
3 → 0
```

导致错误。

所以 Two Sum 哈希法必须记住：

> **先查 need，再保存当前 nums[i]。**

---

# 十四、C 手写哈希和 C++ unordered_map 的对应关系

这是你从 C 转 C++ 最值得掌握的一部分。

### C

你之前自己定义：

```cpp
typedef struct {
    int index;
    int key;
    int used;
} HashNode;
```

然后：

```text
计算哈希位置
↓
处理负数
↓
处理冲突
↓
线性探测
↓
判断 key
↓
保存 index
```

---

### C++

直接：

```cpp
unordered_map<int, int> hash;
```

然后：

```cpp
hash[nums[i]] = i;
```

查：

```cpp
hash.find(need)
```

即可。

所以：

```text
C：
自己造哈希表

C++：
使用标准库提供的哈希表
```

但最重要的是：

> **底层思想没有变。**

你之前 C 里面学的：

```text
key → value
```

到了 C++ 依然是：

```text
key → value
```

只是 C++ 帮你完成了底层实现。

---

# 十五、unordered_map 常用语法总结

## 1. 创建

```cpp
unordered_map<int, int> hash;
```

---

## 2. 插入 / 修改

```cpp
hash[key] = value;
```

例如：

```cpp
hash[10] = 100;
```

---

## 3. 获取 value

```cpp
hash[key]
```

例如：

```cpp
int x = hash[10];
```

---

## 4. 查找

```cpp
hash.find(key)
```

---

## 5. 判断存在

```cpp
hash.find(key) != hash.end()
```

或者：

```cpp
hash.count(key)
```

---

## 6. 删除

```cpp
hash.erase(key);
```

例如：

```cpp
hash.erase(10);
```

删除：

```text
10 → value
```

---

## 7. 清空

```cpp
hash.clear();
```

---

## 8. 大小

```cpp
hash.size()
```

例如：

```cpp
cout << hash.size();
```

---

## 9. 是否为空

```cpp
hash.empty()
```

返回：

```text
true  → 空
false → 不空
```

例如：

```cpp
if(hash.empty())
{
    cout << "空";
}
```

---

# 十六、unordered_map 的遍历

以后你会经常遇到。

最简单：

```cpp
for(auto x : hash)
{
    cout << x.first << " " << x.second;
}
```

这里：

```cpp
x.first
```

表示：

```text
key
```

而：

```cpp
x.second
```

表示：

```text
value
```

例如：

```text
2 → 0
7 → 1
```

那么：

```text
x.first  = 2
x.second = 0
```

---

# 十七、auto 是什么？

上面的：

```cpp
auto x
```

也是 C++ 常见语法。

`auto` 的意思可以简单理解为：

> **让编译器自动判断变量类型。**

例如：

```cpp
auto a = 10;
```

编译器知道：

```text
a 是 int
```

再比如：

```cpp
auto x = hash.find(need);
```

编译器自动知道：

```text
x 是一个迭代器
```

初学阶段你可以先把 `auto` 理解成：

> **“类型太麻烦，让编译器帮我写。”**

---

# 十八、map 和 unordered_map 的区别

| 特性       | map      | unordered_map |
| -------- | -------- | ------------- |
| 底层       | 红黑树      | 哈希表           |
| key 有序   | ✅        | ❌             |
| 平均查找     | O(log n) | O(1)          |
| 插入       | O(log n) | 平均 O(1)       |
| 删除       | O(log n) | 平均 O(1)       |
| 是否适合快速查找 | 可以       | **非常适合**      |

刷算法题时：

```text
需要快速查找某个 key
        ↓
优先考虑 unordered_map
```

如果：

```text
需要 key 自动保持有序
```

则考虑：

```cpp
map
```

---

# 十九、unordered_map 的几个重要特点

### ① 不保证顺序

不要认为：

```cpp
hash[1]
hash[2]
hash[3]
```

遍历时一定是：

```text
1
2
3
```

`unordered_map` 不保证这个顺序。

---

### ② key 必须能够进行哈希

常见类型例如：

```cpp
unordered_map<int, int>
unordered_map<string, int>
```

都可以直接使用。

---

### ③ 一个 key 对应一个 value

例如：

```cpp
hash[10] = 100;
hash[10] = 200;
```

最终：

```text
10 → 200
```

后面的赋值会覆盖之前的 value。

这点和 Two Sum 也有关。

---

# 二十、unordered_map 和 unordered_set 的区别

以后刷题经常会遇到：

```cpp
unordered_map
```

和：

```cpp
unordered_set
```

可以简单理解：

### unordered_map

保存：

```text
key → value
```

例如：

```text
数字 → 下标
```

Two Sum：

```cpp
unordered_map<int, int>
```

---

### unordered_set

只保存：

```text
key
```

不保存对应的 value。

例如：

```cpp
unordered_set<int> s;
```

里面：

```text
2
7
11
15
```

主要用于：

> 快速判断一个元素存不存在。

所以可以简单记：

```text
map  → 键值对
set  → 只有键
```

---

# 二十一、这次 C++ 哈希容易犯的错误

### 🟠 错误 1：不知道 `unordered_map` 的两个类型是什么意思

```cpp
unordered_map<int, int>
```

前面的：

```text
int
```

是 key。

后面的：

```text
int
```

是 value。

Two Sum 中：

```text
key   = 数字
value = 下标
```

---

### 🟠 错误 2：把 `find()` 当成 value

错误理解：

```cpp
hash.find(need)
```

直接得到下标。

实际上：

```text
find()
↓
返回迭代器
```

如果只是判断存在：

```cpp
hash.find(need) != hash.end()
```

如果需要 value：

```cpp
hash[need]
```

---

### 🟠 错误 3：用 `hash[key]` 判断 key 是否存在

不要简单写：

```cpp
if(hash[key])
```

因为访问 `hash[key]` 可能会创建这个 key。

判断存在更推荐：

```cpp
hash.find(key) != hash.end()
```

或者：

```cpp
hash.count(key)
```

---

### 🟠 错误 4：Two Sum 先存后查

错误：

```cpp
hash[nums[i]] = i;

if(hash.find(need) != hash.end())
```

正确：

```cpp
if(hash.find(need) != hash.end())
{
    return {hash[need], i};
}

hash[nums[i]] = i;
```

---

### 🟡 错误 5：把 unordered_map 当成有序容器

不能依赖：

```text
遍历顺序
```

如果题目要求按照 key 排序，需要考虑：

```cpp
map
```

或者自己排序。

---

# 二十二、复杂度

Two Sum：

```cpp
unordered_map<int, int> hash;
```

每次查找：

```cpp
hash.find(need)
```

平均：

```text
O(1)
```

数组遍历：

```text
O(n)
```

所以整体平均时间复杂度：

**O(n)**

哈希表最多保存 `n` 个元素：

**空间复杂度 O(n)**

需要注意：

> `unordered_map` 的 O(1) 是平均复杂度，不是严格保证的最坏情况。

---
# LeetCode 1：两数之和 —— Java 暴力 + 哈希学习总结


## 1. 获取数组长度

Java：

```java
nums.length
```

例如：

```java
int[] nums = {2,7,11,15};

System.out.println(nums.length);
```

结果：

```text
4
```

这一点和 C++ 不一样。

### C++

```cpp
nums.size()
```

### Java

```java
nums.length
```

注意：

```java
length
```

是属性，不是方法。

所以不能写：

```java
nums.length()
```

---

# 五、Java 暴力代码

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {

        for(int i = 0; i < nums.length; i++)
        {
            for(int j = i + 1; j < nums.length; j++)
            {
                if(nums[i] + nums[j] == target)
                {
                    return new int[]{i, j};
                }
            }
        }

        return new int[]{};
    }
}
```

这就是你前面 C++ 暴力版本对应的 Java 写法。

---


# 八、Java 如何返回两个下标

C++：

```cpp
return {i, j};
```

Java：

```java
return new int[]{i, j};
```

这里：

```java
new int[]{i, j}
```

可以理解成：

> 创建一个新的 `int` 数组，并把 `i` 和 `j` 放进去。

例如：

```java
return new int[]{2, 5};
```

返回：

```text
[2,5]
```

---

# 九、没有找到时怎么返回

Java：

```java
return new int[]{};
```

表示返回一个空数组。

例如：

```text
[]
```

这里不能写：

```java
return {};
```

这是 C++ 中比较常见的写法：

```cpp
return {};
```

Java 必须写：

```java
return new int[]{};
```

---

# 十、Java 暴力的复杂度

假设数组长度为 `n`。

第一层循环：

```text
n
```

第二层循环：

```text
n
```

所以时间复杂度：

```text
O(n²)
```

空间复杂度：

```text
O(1)
```

因为除了返回结果之外，没有额外使用随着 `n` 增长的辅助数据结构。

---


# 十二、Java 的 HashMap

Java 中最常用的哈希表之一：

```java
HashMap
```

需要：

```java
import java.util.HashMap;
```

LeetCode 有些环境会自动导入相关类，但自己写完整 Java 程序时应该注意导包。

---

# 十三、HashMap 的基本结构

最重要的写法：

```java
HashMap<Integer, Integer> hash = new HashMap<>();
```

可以理解成：

```text
HashMap<键, 值>
```

这里：

```java
HashMap<Integer, Integer>
```

表示：

```text
key   → Integer
value → Integer
```

在两数之和中，我们规定：

```text
数字 → 下标
```

例如：

```text
2 → 0
7 → 1
11 → 2
15 → 3
```

---

# 十四、为什么是 `Integer`，不是 `int`

这里：

```java
HashMap<Integer, Integer>
```

使用的是：

```java
Integer
```

而不是：

```java
int
```

因为 Java 的泛型：

```java
<>
```

里面需要使用对象类型。

Java 中：

```text
int
```

是基本数据类型。

而：

```text
Integer
```

是 `int` 对应的包装类。

可以先简单记：

```text
int      → 基本类型
Integer  → int 的对象形式
```

因此：

```java
HashMap<Integer, Integer>
```

就是标准的：

> 整数 → 整数

哈希表。

---

# 十五、HashMap 的创建

最常用：

```java
HashMap<Integer, Integer> hash = new HashMap<>();
```

右边：

```java
new HashMap<>()
```

表示创建一个新的 HashMap。

这里的：

```text
<>
```

叫做钻石操作符（Diamond Operator）。

Java 可以根据左边的类型推断右边的泛型类型。

所以不用重复写：

```java
new HashMap<Integer, Integer>()
```

写：

```java
new HashMap<>()
```

即可。

---

# 十六、HashMap 最重要的三个操作

做两数之和主要掌握三个：

```java
put()
get()
containsKey()
```

---

## 1. `put()`

```java
hash.put(key, value);
```

作用：

> 把一个键值对放入 HashMap。

例如：

```java
hash.put(2, 0);
```

表示：

```text
2 → 0
```

也就是：

```text
数字 2 的下标是 0
```

---

## 2. `get()`

```java
hash.get(key);
```

作用：

> 根据 key 找 value。

例如：

```java
hash.put(2, 0);

int index = hash.get(2);
```

那么：

```text
index = 0
```

---

## 3. `containsKey()`

```java
hash.containsKey(key)
```

作用：

> 判断某个 key 是否存在。

例如：

```java
if(hash.containsKey(2))
```

意思就是：

> HashMap 里面有没有 2？

返回：

```text
true
```

或者：

```text
false
```

---



# 十八、Java 哈希最终代码

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {

        HashMap<Integer, Integer> hash = new HashMap<>();

        for(int i = 0; i < nums.length; i++)
        {
            int need = target - nums[i];

            if(hash.containsKey(need))
            {
                return new int[]{hash.get(need), i};
            }

            hash.put(nums[i], i);
        }

        return new int[]{};
    }
}
```

---



# 二十二、Java HashMap 常用语法总结

## 1. 创建

```java
HashMap<Integer, Integer> hash = new HashMap<>();
```

---

## 2. 添加

```java
hash.put(10, 5);
```

表示：

```text
10 → 5
```

---

## 3. 查询

```java
hash.get(10);
```

得到：

```text
5
```

---

## 4. 判断 key 是否存在

```java
hash.containsKey(10);
```

返回：

```text
true
```

或者：

```text
false
```

---

## 5. 删除

```java
hash.remove(10);
```

删除：

```text
10 → 5
```

---

## 6. 清空

```java
hash.clear();
```

---

## 7. 获取元素数量

```java
hash.size();
```

---

## 8. 判断是否为空

```java
hash.isEmpty();
```

---

# 二十三、一个非常容易踩的坑：`get()` 不等于判断存在

不要这样写：

```java
if(hash.get(need) != null)
```

虽然某些情况下可以使用，但初学阶段更推荐：

```java
if(hash.containsKey(need))
```

因为：

```text
containsKey()
```

的含义非常明确：

> 判断 key 是否存在。

而：

```java
get()
```

的职责是：

> 获取 key 对应的 value。

所以最好分工：

```java
if(hash.containsKey(need))
{
    int index = hash.get(need);
}
```

---

# 二十四、HashMap 修改已有数据

例如：

```java
hash.put(2, 0);
hash.put(2, 5);
```

最终：

```text
2 → 5
```

第二次 `put` 会覆盖原来的 value。

所以：

```java
put()
```

既可以：

> 添加

也可以：

> 修改

---

# 二十五、HashMap 遍历

如果想把 HashMap 中所有数据取出来：

```java
for(Map.Entry<Integer, Integer> entry : hash.entrySet())
{
    System.out.println(entry.getKey());
    System.out.println(entry.getValue());
}
```

这里出现几个新知识。

---

## `entrySet()`

```java
hash.entrySet()
```

表示获取 HashMap 中所有的：

```text
键值对
```

---

## `Map.Entry`

```java
Map.Entry<Integer, Integer>
```

表示：

> 一个键值对。

例如：

```text
2 → 0
```

就是一个 Entry。

---

## `getKey()`

```java
entry.getKey()
```

获取：

```text
key
```

---

## `getValue()`

```java
entry.getValue()
```

获取：

```text
value
```

---

# 二十六、`for-each` 循环

Java 中经常看到：

```java
for(int x : nums)
{
    System.out.println(x);
}
```

意思是：

> 依次取出数组中的每一个元素。

例如：

```text
nums = [2,7,11]
```

依次：

```text
x = 2
x = 7
x = 11
```

---

# 二十七、`for` 和 `for-each` 的区别

如果需要下标：

```java
for(int i = 0; i < nums.length; i++)
```

因为：

```java
i
```

可以表示下标。

如果只需要元素：

```java
for(int x : nums)
```

更加方便。

两数之和需要返回下标，所以这里使用普通 `for` 更合适。

---



# 二十九、Java 与 C++ 两数之和语法对照

## 数组

C++：

```cpp
vector<int>& nums
```

Java：

```java
int[] nums
```

---

## 数组长度

C++：

```cpp
nums.size()
```

Java：

```java
nums.length
```

---

## 哈希表

C++：

```cpp
unordered_map<int,int> hash;
```

Java：

```java
HashMap<Integer,Integer> hash = new HashMap<>();
```

---

## 插入

C++：

```cpp
hash[nums[i]] = i;
```

Java：

```java
hash.put(nums[i], i);
```

---

## 获取

C++：

```cpp
hash[need]
```

Java：

```java
hash.get(need)
```

---

## 判断是否存在

C++：

```cpp
hash.find(need) != hash.end()
```

Java：

```java
hash.containsKey(need)
```

---

## 返回数组

C++：

```cpp
return {i,j};
```

Java：

```java
return new int[]{i,j};
```

---

# 三十、Java 暴力 vs Java 哈希

| 方法      |   时间复杂度 | 空间复杂度 | 核心思想    |
| ------- | ------: | ----: | ------- |
| 暴力枚举    |   O(n²) |  O(1) | 两两比较    |
| HashMap | O(n) 平均 |  O(n) | 数字 → 下标 |

---

# 三十一、两种算法的思维区别

### 暴力：

```text
拿当前数字
    ↓
一个一个往后找
    ↓
找到目标
```

### 哈希：

```text
拿当前数字
    ↓
计算需要什么
    ↓
直接去 HashMap 查
    ↓
找到目标
```

本质上是：

> **用额外的空间，换取更快的查询速度。**

这就是非常经典的：

```text
空间换时间
```

---

# 三十二、Java HashMap 与 C++ unordered_map 的关系

你之前学习 C++：

```cpp
unordered_map<int,int>
```

现在 Java：

```java
HashMap<Integer,Integer>
```

虽然语法不同，但本质上做的是同一件事情：

```text
key → value
```

两数之和中：

```text
数字 → 下标
```

所以你可以把它们对应起来：

```text
C++ unordered_map
        ↓
Java HashMap
        ↓
都是哈希表
        ↓
都是通过 key 快速寻找 value
```

最大的区别只是：

> C++ 和 Java 提供的标准库接口不同。

---

# 三十三、Java 中其他常见集合

以后刷题还会经常遇到这些。

## 1. ArrayList

```java
ArrayList<Integer> list = new ArrayList<>();
```

可以理解成：

> Java 中比较常用的动态数组。

类似 C++：

```cpp
vector<int>
```

---

## 2. HashSet

```java
HashSet<Integer> set = new HashSet<>();
```

特点：

> 只保存元素，不保存“元素 → 值”的对应关系。

例如：

```text
{2,7,11}
```

如果只想判断：

> 某个数字有没有出现过？

HashSet 就非常适合。

---

## 3. HashMap

```java
HashMap<Integer,Integer> map = new HashMap<>();
```

保存：

```text
key → value
```

例如：

```text
数字 → 下标
```

---

# 三十四、Java 集合简单对照

| Java        | 作用      | 类似 C++          |
| ----------- | ------- | --------------- |
| `int[]`     | 固定长度数组  | 原生数组            |
| `ArrayList` | 动态数组    | `vector`        |
| `HashMap`   | 键值映射    | `unordered_map` |
| `HashSet`   | 去重/判断存在 | `unordered_set` |
| `TreeMap`   | 有序键值映射  | `map`           |
| `TreeSet`   | 有序集合    | `set`           |

这一部分以后刷题会大量用到。

---

# 三十五、这次 Java 学习中容易犯的错误

### 🔴 1. 把 `.length` 写成 `.length()`

错误：

```java
nums.length()
```

正确：

```java
nums.length
```

---

### 🔴 2. Java 返回数组写成 C++ 形式

错误：

```java
return {i,j};
```

正确：

```java
return new int[]{i,j};
```

---

### 🔴 3. HashMap 用 `[]`

错误：

```java
hash[nums[i]] = i;
```

这是 C++ 的写法。

Java：

```java
hash.put(nums[i], i);
```

---

### 🔴 4. Java 获取 HashMap 数据也不能使用 `[]`

错误：

```java
hash[need]
```

正确：

```java
hash.get(need)
```

---

### 🟠 5. 没有判断 key 是否存在就 `get`

更推荐：

```java
if(hash.containsKey(need))
{
    int index = hash.get(need);
}
```

---

### 🟠 6. 哈希表先存后查

容易造成：

```text
自己和自己匹配
```

正确顺序：

```text
查 → 存
```

---

### 🟡 7. 忘记返回值

方法：

```java
public int[] twoSum(...)
```

要求返回：

```text
int[]
```

所以所有执行路径最终都需要能够返回一个 `int[]`。

例如：

```java
return new int[]{};
```

---
# LeetCode 1：两数之和 —— Python 暴力 + 哈希学习总结
# 三、Python 的 LeetCode 基本结构

Python 的 LeetCode 通常写成：

```python
class Solution:
    def twoSum(self, nums, target):
        pass
```

---

## 1. `class`

```python
class Solution:
```

表示定义一个类。

LeetCode 通常规定：

```text
类名：Solution
```

所以直接使用即可。

---

## 2. `def`

Python 定义函数使用：

```python
def 函数名(参数):
```

例如：

```python
def add(a, b):
    return a + b
```

两数之和：

```python
def twoSum(self, nums, target):
```

表示定义一个叫：

```text
twoSum
```

的方法。

---

## 3. `self`

```python
def twoSum(self, nums, target):
```

这里的 `self` 表示当前对象。

目前刷 LeetCode 时，可以先简单理解：

> `Solution` 是一个类，`self` 是这个类当前的对象。

现阶段不需要深入研究面向对象原理。

---

# 四、Python 与 C++/Java 最大的语法区别之一：缩进

C++：

```cpp
if(condition)
{
    return;
}
```

Java：

```java
if(condition)
{
    return;
}
```

Python：

```python
if condition:
    return
```

Python 不使用 `{}` 表示代码块。

而是使用：

> **冒号 `:` + 缩进**

例如：

```python
if need in hash:
    return [hash[need], x]
```

这里 `return` 必须缩进。

---

# 五、Python 的变量不需要声明类型

C++：

```cpp
int need = target - nums[i];
```

Java：

```java
int need = target - nums[i];
```

Python：

```python
need = target - nums[x]
```

Python 不需要提前写：

```text
int
double
String
```

它会根据赋值自动判断类型。

例如：

```python
a = 10
```

`a` 是整数。

```python
a = "hello"
```

`a` 又可以是字符串。

这种方式称为：

> 动态类型。

---

# 六、Python 的 list

Python 最常用的数组结构之一是：

```python
list
```

例如：

```python
nums = [2,7,11,15]
```

可以暂时理解成：

> Python 中的动态数组。

访问元素：

```python
nums[0]
```

得到：

```text
2
```

访问：

```python
nums[2]
```

得到：

```text
11
```

---

# 七、Python 获取数组长度：`len()`

C++：

```cpp
nums.size()
```

Java：

```java
nums.length
```

Python：

```python
len(nums)
```

例如：

```python
nums = [2,7,11,15]

len(nums)
```

结果：

```text
4
```

注意：

```python
len(nums)
```

是函数调用。

不是：

```python
nums.length
```

也不是：

```python
nums.size()
```

---

# 八、Python 的 `range()`

例如：

```python
range(5)
```

表示：

```text
0
1
2
3
4
```

注意：

> `range()` 的结束位置不包含。

所以：

```python
range(len(nums))
```

正好可以用来遍历数组下标。

例如：

```python
nums = [2,7,11,15]

for x in range(len(nums)):
    print(x)
```

输出：

```text
0
1
2
3
```

---

# 九、Python 暴力枚举


# 十、Python 暴力代码

最终写法：

```python
class Solution(object):

    def twoSum(self, nums, target):

        for x in range(len(nums)):

            for y in range(x + 1, len(nums)):

                if nums[x] + nums[y] == target:

                    return [x, y]

        return []
```

---


# 十三、Python 返回两个下标

Python：

```python
return [x, y]
```

这里：

```python
[x, y]
```

是一个 list。

例如：

```python
return [0, 1]
```

得到：

```text
[0,1]
```

和 Java：

```java
return new int[]{0,1};
```

以及 C++：

```cpp
return {0,1};
```

作用类似。

---

# 十四、Python 暴力复杂度

假设数组长度为 `n`。

两个循环：

```text
第一层：O(n)
第二层：O(n)
```

所以：

```text
时间复杂度：O(n²)
空间复杂度：O(1)
```

核心特点：

> 不需要额外的数据结构，但需要大量比较。

---


# 十六、Python 的哈希表：dict

Python 中最常用的哈希表结构：

```python
dict
```

例如：

```python
hash = {}
```

表示：

> 创建一个空字典。

它对应前面学过的：

```text
C++：
unordered_map

Java：
HashMap

Python：
dict
```

本质都是：

```text
key → value
```

---

# 十七、Python dict 的基本操作

## 1. 创建

```python
hash = {}
```

---

## 2. 添加数据

```python
hash[2] = 0
```

表示：

```text
2 → 0
```

在两数之和中就是：

```text
数字 2 → 下标 0
```

---

## 3. 获取数据

```python
hash[2]
```

得到：

```text
0
```

---

## 4. 判断 key 是否存在

Python 非常方便：

```python
if 2 in hash:
```

意思：

> 判断 `2` 是否是字典中的 key。

返回：

```text
True
```

或者：

```text
False
```

---


# 二十一、最终 Python 哈希代码

你最后自己修改完成的是：

```python
class Solution(object):

    def twoSum(self, nums, target):

        hash = {}

        for x in range(len(nums)):

            need = target - nums[x]

            if need in hash:

                return [hash[need], x]

            hash[nums[x]] = x

        return []
```

这份代码：

> **算法正确，Python 语法正确，可以通过这道题。**


# 二十四、Python dict 常用操作

除了这道题使用的三个操作，还需要逐渐掌握下面这些。

## 添加 / 修改

```python
hash[key] = value
```

---

## 获取

```python
hash[key]
```

---

## 判断是否存在

```python
key in hash
```

---

## 删除

```python
del hash[key]
```

或者：

```python
hash.pop(key)
```

---

## 获取长度

```python
len(hash)
```

---

## 清空

```python
hash.clear()
```

---

# 二十五、Python 字典遍历

以后会经常看到：

```python
for key in hash:
    print(key)
```

表示遍历所有 key。

如果需要同时得到 key 和 value：

```python
for key, value in hash.items():
    print(key, value)
```

例如：

```python
hash = {
    2: 0,
    7: 1
}
```

遍历：

```python
for key, value in hash.items():
    print(key, value)
```

得到：

```text
2 0
7 1
```

---

# 二十六、`items()` 是什么

```python
hash.items()
```

可以理解成：

> 获取字典中的所有键值对。

例如：

```text
2 → 0
7 → 1
```

就可以同时得到：

```text
key = 2
value = 0

key = 7
value = 1
```

因此：

```python
for key, value in hash.items():
```

非常常用。

---

# 二十七、Python `dict` 和 Java `HashMap` 对照

| 操作 | Java              | Python        |
| -- | ----------------- | ------------- |
| 创建 | `new HashMap<>()` | `{}`          |
| 添加 | `put(k,v)`        | `hash[k] = v` |
| 获取 | `get(k)`          | `hash[k]`     |
| 判断 | `containsKey(k)`  | `k in hash`   |
| 删除 | `remove(k)`       | `del hash[k]` |
| 清空 | `clear()`         | `clear()`     |
| 数量 | `size()`          | `len(hash)`   |

---

# 二十八、Python 与 C++/Java 的两数之和对照

## 数组长度

C：

```c
numsSize
```

C++：

```cpp
nums.size()
```

Java：

```java
nums.length
```

Python：

```python
len(nums)
```

---

## 哈希表

C：

```text
自己实现 HashNode
```

C++：

```cpp
unordered_map<int,int>
```

Java：

```java
HashMap<Integer,Integer>
```

Python：

```python
hash = {}
```

---

## 判断 key 是否存在

C++：

```cpp
hash.find(need) != hash.end()
```

Java：

```java
hash.containsKey(need)
```

Python：

```python
need in hash
```

---

## 获取 value

C++：

```cpp
hash[need]
```

Java：

```java
hash.get(need)
```

Python：

```python
hash[need]
```

---

## 保存

C++：

```cpp
hash[nums[i]] = i;
```

Java：

```java
hash.put(nums[i], i);
```

Python：

```python
hash[nums[i]] = i
```

---

## 返回两个下标

C++：

```cpp
return {i,j};
```

Java：

```java
return new int[]{i,j};
```

Python：

```python
return [i,j]
```

---

# 二十九、Python 的一些重要语法特点

## 1. 不需要分号

C/C++/Java：

```cpp
int a = 10;
```

Python：

```python
a = 10
```

一般不写：

```python
a = 10;
```

---

## 2. 不使用 `{}` 表示代码块

Python：

```python
if x > 0:
    print(x)
```

---

## 3. 冒号非常重要

例如：

```python
if x > 0:
```

```python
for x in nums:
```

```python
def twoSum(...):
```

这些语句后面通常都有：

```text
:
```

---

## 4. 缩进非常重要

正确：

```python
if x > 0:
    print(x)
```

错误：

```python
if x > 0:
print(x)
```

Python 会根据缩进判断代码属于哪个代码块。

---

# 三十、Python `list` 的一些常见操作

以后刷题也会经常用到。

创建：

```python
nums = [1,2,3]
```

访问：

```python
nums[0]
```

修改：

```python
nums[0] = 10
```

添加：

```python
nums.append(4)
```

删除：

```python
nums.pop()
```

获取长度：

```python
len(nums)
```

判断元素是否存在：

```python
if 3 in nums:
```

---

# 三十一、Python 中 `in` 的使用

这次你已经用到了：

```python
if need in hash:
```

`in` 是 Python 非常重要的语法。

例如 list：

```python
3 in [1,2,3]
```

结果：

```text
True
```

字典：

```python
3 in hash
```

判断的是：

> **key 是否存在。**

所以：

```python
if need in hash:
```

非常适合两数之和。

---

# 三十二、Python 暴力和哈希对比

| 方法 |   时间复杂度 | 空间复杂度 | 思想      |
| -- | ------: | ----: | ------- |
| 暴力 |   O(n²) |  O(1) | 两两比较    |
| 哈希 | O(n) 平均 |  O(n) | 记录并快速查询 |

哈希方法本质上就是：

> **用额外空间换取查询速度。**

---

