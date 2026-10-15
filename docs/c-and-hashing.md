# C 语言：返回数组与手写哈希表

[返回首页](../README.md) · [两数之和题解](../problems/hash-table/0001-two-sum/README.md)

本篇整理原学习笔记中的 C 语言探索。实际源码见[暴力版](../problems/hash-table/0001-two-sum/c/brute_force.c)与[哈希版](../problems/hash-table/0001-two-sum/c/hash.c)。

## 目录

- [返回指针与数组长度](#返回指针与数组长度)
- [内存分配与释放](#内存分配与释放)
- [为什么不能直接用数值当下标](#为什么不能直接用数值当下标)
- [初始化与memset](#初始化与memset)
- [取模与负数](#取模与负数)
- [冲突与线性探测](#冲突与线性探测)
- [从原错误代码中复习](#从原错误代码中复习)

## 返回指针与数组长度

力扣接口：

```c
int* twoSum(int* nums, int numsSize, int target, int* returnSize);
```

| 部分 | 含义 |
| --- | --- |
| int* 返回值 | 结果数组的首元素地址 |
| nums | 输入数组的首元素地址 |
| numsSize | 输入长度，指针本身不携带数组长度 |
| returnSize | 输出参数，用 *returnSize 写出结果长度 |

C 中不能写 `return [i, j];`，也不能用没有值的 `return;` 满足指针返回类型。无结果可返回 NULL，同时写 `*returnSize = 0;`。

函数内普通局部数组具有自动存储期：

```c
/* 错误示范：函数返回后，result 对象已经失效 */
int result[2] = {i, j};
return result;
```

需要给结果分配函数返回后仍有效的存储空间。本题约定使用 malloc，由调用方 free。不能把“所有局部变量都在栈上”当作 C 标准保证；理解存储期比记具体栈布局更准确。

## 内存分配与释放

```c
int* result = malloc(2 * sizeof(*result));
if (result == NULL) {
    return NULL;  /* 分配失败 */
}
result[0] = i;
result[1] = j;
*returnSize = 2;
return result;    /* 此处不能 free(result)，调用方还要读取 */
```

使用 malloc/calloc/free 需要 `#include <stdlib.h>`。malloc 不初始化内容；calloc 将分配的字节置零，适合本题全部由 int 字段组成的 HashNode 表。表内 used 为 0 表示空槽。

本题整理后的实现只在找到答案时分配结果；哈希表放在堆上，所有返回路径释放哈希表。C 的返回值需要调用方在读完后释放，不要依赖垃圾回收。

## 为什么不能直接用数值当下标

`int hash[numsSize]` 的合法下标为 0 到 numsSize−1。输入数值可能为负、也可能达到 10^9，不能写 `hash[nums[i]]` 直接访问。

将 key 映射到有限槽位是哈希函数的任务，但映射会产生冲突；只做取模不等于实现了完整哈希表。

## 初始化与memset

原代码写过：

```c
memset(hash, -1, size);
```

第三个参数是字节数，不是 int 个数。如果 hash 是当前作用域中真正的数组，要覆盖完整存储可写 `sizeof(hash)`；若 hash 已经是指针，sizeof(hash) 仅是指针大小，不能用来求数组长度。

此外 memset 按字节设置值，不是逐个整数赋值。若目标是可移植地将 int 数组每个元素设为 -1，最直接是循环：

```c
for (int i = 0; i < capacity; ++i) {
    indexTable[i] = -1;
}
```

在常见补码平台，全字节 0xff 对应 int 的 -1，但不要把 memset 当作任意整数初始化函数。比如 memset(a, 1, ...) 通常不会得到每个 int 都是 1。使用它还需要 `<string.h>`。本仓库哈希版使用独立 used 标记与 calloc，不依赖 -1 哨兵。

## 取模与负数

C/C++/Java 中，负数余数可能为负。例如：

```text
-7 % 3 = -1
```

Python 在正模数下结果非负：

```python
-7 % 3  # 2
```

要得到 0 到 capacity−1 的槽位，C 中可以：

```c
int slot = key % capacity;
if (slot < 0) slot += capacity;
```

原笔记中的 `((key % capacity) + capacity) % capacity` 在此处容量较小时也可用。源码选用条件加法，避免在更大容量下无谓的加法溢出风险。

## 冲突与线性探测

例如容量为 11 时，1 和 12 都映射到槽位 1。槽位相同不代表数值相同。

因此保存：

```c
typedef struct {
    int key;    /* 原始数值 */
    int index;  /* 输入中的下标 */
    int used;   /* 该槽是否占用 */
} HashNode;
```

查找步骤：

1. 由 need 得到槽位。
2. 槽已使用且 key 相等，找到答案。
3. 槽已使用但 key 不同，移动到下一个槽。
4. 遇到空槽，说明没找到；前提是该表没有删除操作破坏探测链。

移动槽位：

```c
slot = (slot + 1) % capacity;
```

这里不能增加输入下标 i，它控制的是另一个遍历过程。插入也使用同样的探测规则。若允许删除，需要墓碑标记等额外处理；本题不涉及删除。

源码使用 2n+1 个槽位，最多存入 n 个不同 key，因此保留空槽，不会因为表满而无限探测。简单取模仍可能遭遇大量冲突，平均 O(n) 的整体时间不是对每组输入都保证。

## 从原错误代码中复习

- `=` 赋值，`==` 比较；`if (node.key = need)` 会修改 key。
- 槽位被占用后，要比较完整 key，不能只判断 used。
- 下标 0 有效，不能用“下标非零”表示存在。
- 先查后存，避免将同一个位置使用两次。
- 对无解或分配失败路径也要设置清晰的返回值和长度。
- 若输入扩大到完整 int 范围，要检查 target−nums[i] 的溢出；当前代码按本题 ±10^9 约束编写。
