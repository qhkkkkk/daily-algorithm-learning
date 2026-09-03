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

#C++暴力法
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
