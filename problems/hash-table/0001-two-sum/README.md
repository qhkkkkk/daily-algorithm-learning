# LeetCode 1 · 两数之和

[返回首页](../../../README.md) · [哈希表分类](../../../categories/README.md#哈希表) · [力扣原题](https://leetcode.cn/problems/two-sum/)

| 难度 | 主分类 | 标签 | 语言 |
| --- | --- | --- | --- |
| 简单 | 哈希表 | 数组、枚举、空间换时间 | C++ / Java / Python 3；补充 C |

## 目录

- [题意与例子](#题意与例子)
- [暴力枚举](#暴力枚举)
- [哈希表思路](#哈希表思路)
- [逐步推演与正确性](#逐步推演与正确性)
- [三种语言源码](#三种语言源码)
- [C语言源码与内存](#c语言源码与内存)
- [原笔记中的困惑与修正](#原笔记中的困惑与修正)
- [语言差别与常用接口](#语言差别与常用接口)
- [复杂度与边界](#复杂度与边界)
- [复习自测](#复习自测)

## 题意与例子

在数组中找两个不同下标，使对应数值之和等于 target，返回这两个下标。题目保证恰有一组答案，返回下标的先后顺序不限。

```text
nums = [2, 7, 11, 15], target = 9
答案：[0, 1]，因为 nums[0] + nums[1] = 9
```

注意返回的是位置，不是数值 `[2, 7]`。`[3, 3]` 可以使用两个不同位置的 3，但同一个位置不能使用两次。

## 暴力枚举

固定 i，再让 j 从 i + 1 开始，逐个检查后面的元素。这样不会把元素与自身相加，也不会重复检查同一对位置。

```python
class Solution:
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):  # 从 i 后面开始
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
```

其他语言的独立源码：[C++](cpp/brute_force.cpp) · [Java](java/brute_force/Solution.java) · [C](c/brute_force.c)。

最多检查 n(n−1)/2 对，时间 O(n²)，额外空间 O(1)，不计返回的两个下标。

## 哈希表思路

每次看到当前数值 value，计算：

```text
need = target - value
```

我们只需知道：**此前是否见过 need？如果见过，它在哪个下标？**

因此哈希表存储的是：

```text
数值 key -> 此前出现的下标 value
```

顺序必须是：

```text
计算 need -> 查询 need -> 找到则返回 -> 没找到再存当前数值与下标
```

“先查后存”保证取出的下标属于以前的元素。

## 逐步推演与正确性

对于 `[2, 7, 11, 15]`、target = 9：

| i | 当前值 | need | 查询前 seen | 操作 |
| ---: | ---: | ---: | --- | --- |
| 0 | 2 | 7 | {} | 没有 7，存入 2 -> 0 |
| 1 | 7 | 2 | {2: 0} | 找到 2，返回 [0, 1] |

对于 `[3, 3]`、target = 6，第一次查询不到 3，才存 `3 -> 0`；第二次查询得到下标 0，返回 `[0, 1]`。

每轮查询前，seen 中只存此前扫描过的元素。若存在答案，扫描到答案中靠后的那个位置时，另一个值已经在表里，因此能找到答案；表中的下标小于当前下标，所以不会重复使用同一位置。

## 三种语言源码

### C++

[源码](cpp/hash.cpp)。`std::unordered_map<int, int>` 的两个类型分别是 key 和 value；`auto` 让编译器推断迭代器类型。

```cpp
#include <unordered_map>
#include <vector>

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& nums, int target) {
        std::unordered_map<int, int> seen;  // 数值 -> 下标
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            int need = target - nums[i];
            auto it = seen.find(need);  // find 不会插入不存在的键
            if (it != seen.end()) {
                return {it->second, i};
            }
            seen[nums[i]] = i;  // 先查，后存
        }
        return {};
    }
};
```

`find(need)` 返回迭代器，不是直接返回下标。`end()` 表示尾后位置，比较不等后才可以访问 `it->second`。键值对中 `first` 是 key，`second` 是 value。

### Java

[源码](java/hash/Solution.java)。`HashMap` 的泛型参数使用包装类型 `Integer`，不能写基本类型 `int`。

```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            if (seen.containsKey(need)) {  // 先判断存在，再获取下标
                return new int[]{seen.get(need), i};
            }
            seen.put(nums[i], i);  // 先查，后存
        }
        return new int[0];
    }
}
```

`Map` 是接口，`HashMap` 是实现。`put` 插入或更新；`containsKey` 判断键是否存在；`get` 读取对应下标。int 与 Integer 之间会自动装箱/拆箱。

### Python 3

[源码](python/hash.py)。`seen = {}` 创建字典，`enumerate(nums)` 同时提供下标与元素。

```python
class Solution:
    def twoSum(self, nums, target):
        seen = {}  # 数值 -> 已经遍历过的下标
        for i, value in enumerate(nums):
            need = target - value
            if need in seen:  # 先查，再存，避免同一个元素使用两次
                return [seen[need], i]
            seen[value] = i
        return []
```

如果暂时不熟悉 enumerate，可以把循环改成：

```python
for i in range(len(nums)):
    value = nums[i]
```

`class` 定义类，`def` 定义方法，`self` 是当前实例。`Solution` 是力扣约定的类名；这些结构不改变哈希算法本身。

## C语言源码与内存

原笔记中的 C 语言探索保留为独立源码和[专题说明](../../../docs/c-and-hashing.md)。

- [暴力枚举](c/brute_force.c)：找到答案后 malloc 两个整数，使用 returnSize 传出长度。
- [手写哈希表](c/hash.c)：结构体保存 key、index、used，取模定位，冲突后线性探测。

手写哈希版如下：

```c
#include <stdlib.h>

typedef struct {
    int key;
    int index;
    int used;  /* 单独标记占用，因为 0 也是合法的值和下标 */
} HashNode;

static int hashIndex(int key, int capacity) {
    int index = key % capacity;
    return index < 0 ? index + capacity : index;
}

/* 本实现面向本题约束：numsSize <= 10000，数值和 target 在 +/-10^9 内。 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    *returnSize = 0;
    int capacity = 2 * numsSize + 1;  /* 留足空槽，线性探测能遇到未用位置 */
    HashNode* table = calloc((size_t)capacity, sizeof(*table));
    if (table == NULL) return NULL;

    for (int i = 0; i < numsSize; ++i) {
        int need = target - nums[i];
        int slot = hashIndex(need, capacity);

        /* 冲突只表示槽位相同，必须继续比较原始 key。 */
        while (table[slot].used) {
            if (table[slot].key == need) {
                int* result = malloc(2 * sizeof(*result));
                if (result == NULL) {
                    free(table);
                    return NULL;
                }
                result[0] = table[slot].index;
                result[1] = i;
                *returnSize = 2;
                free(table);  /* 哈希表不再需要；结果留给调用方释放 */
                return result;
            }
            slot = (slot + 1) % capacity;
        }

        /* 先查后存。重复 key 可更新下标，不需要增加一个重复槽位。 */
        slot = hashIndex(nums[i], capacity);
        while (table[slot].used && table[slot].key != nums[i]) {
            slot = (slot + 1) % capacity;
        }
        table[slot].key = nums[i];
        table[slot].index = i;
        table[slot].used = 1;
    }
    free(table);
    return NULL;
}
```

C 没有内置通用哈希容器，所以代码比另外三种语言长。本版本用 calloc 在堆上建立与 n 成比例的表，结束时 free；返回的结果由调用方 free。分配失败或无答案时返回 NULL，并将 *returnSize 保持为 0。题目约束下，容量 2n+1 不会被填满。

## 原笔记中的困惑与修正

以下来自原“两数之和”学习笔记，按问题重新组织，重复的讲解合并到语言速查表。

| 当时的困惑或尝试 | 原因与修正 |
| --- | --- |
| C 中写 `return [i, j];` | C 不支持 Python 列表字面量，需要分配结果数组并返回指针 |
| 指针返回类型却写 `return;` | 需要返回指针值，例如 NULL |
| 返回局部 `int result[2]` | 自动存储期数组在函数结束后失效，不能返回其地址供调用方使用 |
| `returnSize` 是什么 | 指向输出长度的参数，写 `*returnSize = 2` 才修改外部长度 |
| 哈希表到底存什么 | 本题存“数值 -> 下标”，只存数值不能直接返回位置 |
| 先存当前数值再查询 | 可能与自身匹配，改成先查后存 |
| 用数值直接作为数组下标 | 数值可以为负或很大，不能拿长度为 n 的数组直接索引 |
| `memset(hash, -1, size)` | 第三个参数是字节数，不是 int 元素个数 |
| 取模后下标仍为负 | C 中负数余数可能为负，需要归一化到合法下标 |
| 不同数值落在同一槽 | 哈希冲突，必须比较 key 并继续探测 |
| 发生冲突时写 `i++` | i 是输入下标；此处应移动哈希槽位 slot |
| `if (node.key = need)` | `=` 是赋值，应使用 `==` 比较 |
| C++ `seen[need]` 用于判断存在 | 缺失时会插入默认值 0，且下标 0 本身有效，应使用 find/count |
| 把 C++ find 的结果当下标 | 返回的是迭代器；先检查 end，再读 second |
| Java 数组长度写 `length()` | 数组使用属性 length；字符串才用 length() |
| Java 写 `return {i, j};` | 应写 `return new int[]{i, j};` |
| Java HashMap 使用 `[]` | 应使用 put、get、containsKey |
| Java get 缺失键 | 返回 null；拆箱到 int 会触发异常，先判断存在 |
| Python 循环、冒号与缩进 | `for i in range(...):`，代码块靠缩进 |
| Python `need in seen` 的含义 | 判断字典的 key 是否存在，不是判断 value |

原文中标作“最终正确”的 C 代码还有可改进处：大固定数组放在自动存储区、分配失败未检查、无答案路径返回未初始化结果。整理后的源码补全了这些处理。memset 设置为 -1 的可移植性也见 [C 专题](../../../docs/c-and-hashing.md)。

原始学习记录仍可从[重构前的 Git 历史](https://github.com/qhkkkkk/daily-algorithm-learning/tree/2f42b6579e48de1a4577ca3efc6802f0af377cd8)查看；仓库根目录原文件名保留为导航入口。

## 语言差别与常用接口

| 操作 | C++ | Java | Python |
| --- | --- | --- | --- |
| 哈希表 | `std::unordered_map<int, int>` | `HashMap<Integer, Integer>` | `dict` / `{}` |
| 判断存在 | `seen.find(k) != seen.end()` | `seen.containsKey(k)` | `k in seen` |
| 获取值 | `it->second` 或已确认存在后 `seen[k]` | `seen.get(k)` | `seen[k]` |
| 插入或更新 | `seen[k] = v;` | `seen.put(k, v);` | `seen[k] = v` |
| 返回下标数组 | `return {a, b};` | `return new int[]{a, b};` | `return [a, b]` |
| 数组长度 | `nums.size()` | `nums.length` | `len(nums)` |

不要把容器名字都写成 hash：Python 有内置 `hash()` 函数，使用 seen 更能表达“此前见过的元素”。

`map` 与 `unordered_map` 都映射 key 到 value，但前者按键排序、查找 O(log n)，后者不按键排序、查找平均 O(1)。本题不需要排序。Set 只保存元素，不直接保存对应下标；因此这里选择 Map。

更多常用操作、遍历、容器差别见[语言速查表](../../../docs/language-cheatsheet.md)。

## 复杂度与边界

| 方法 | 时间 | 额外空间 |
| --- | --- | --- |
| 双重循环 | O(n²) | O(1) |
| 哈希表 | 平均 O(n) | O(n) |

C++ unordered_map、Python dict 在严重冲突时，单次查询可能退化到 O(n)；手写 C 线性探测在本题这样的简单哈希函数下也可能退化，整题最坏 O(n²)。这里的平均 O(n) 依赖哈希分布良好。Java HashMap 有树化等实现细节，不把所有容器的最坏行为混为一谈。

| 输入 | target | 检查点 |
| --- | ---: | --- |
| [2, 7, 11, 15] | 9 | 普通情况 |
| [3, 2, 4] | 6 | 答案不含首元素 |
| [3, 3] | 6 | 重复值，不同位置 |
| [0, 4, 3, 0] | 0 | 值和下标 0 都有效 |
| [-3, 4, 3, 90] | 0 | 负数 |
| [1, 12, 4, 8, 20] | 28 | C 表容量为 11，1 与 12 冲突 |
| [-1000000000, 1000000000] | 0 | 本题数值边界 |

本题数值和 target 在 ±10^9 内，int 的加减在常见 32 位有符号范围内。若迁移到允许完整 32 位输入的题，C/C++/Java 需要另行考虑溢出和更宽类型；Python 整数不受固定 32 位范围限制。题目保证有解，代码末尾的空结果是防御性返回，不是题目通常输出。

## 复习自测

1. 为什么 j 从 i + 1 开始？
2. 哈希表的 key 和 value 分别是什么？
3. `[3, 3]` 为什么必须先查后存？
4. C++ find 返回什么，为什么要比较 end？
5. Java get 缺失键后直接赋给 int 会怎样？
6. C 为什么不能返回普通局部数组？谁释放 malloc 的结果？
7. 为什么对 key 取模后仍必须保存并比较完整 key？
