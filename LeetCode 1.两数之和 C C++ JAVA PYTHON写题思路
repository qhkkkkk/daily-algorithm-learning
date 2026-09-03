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

