# LeetCode 560 · 和为 K 的子数组

[返回首页](../../../README.md) · [前缀和分类](../../../categories/README.md#前缀和) · [力扣原题](https://leetcode.cn/problems/subarray-sum-equals-k/)

| 难度 | 主分类 | 标签 | 语言 |
| --- | --- | --- | --- |
| 中等 | 前缀和 | 数组、哈希表、频次统计、连续区间 | C++ / Java / Python 3 |

## 目录

- [题意与例子](#题意与例子)
- [从朴素思路到前缀和](#从朴素思路到前缀和)
- [变量分别记录什么](#变量分别记录什么)
- [逐步推演与正确性](#逐步推演与正确性)
- [三种语言源码](#三种语言源码)
- [本次困惑与解答](#本次困惑与解答)
- [语言差别与常用接口](#语言差别与常用接口)
- [复杂度与边界](#复杂度与边界)
- [复习自测](#复习自测)

## 题意与例子

统计数组中**连续、非空、元素和等于 k** 的子数组数量，返回一个整数，不需要修改输入。

以 nums = [1, 1, 1]、k = 2 为例：

| 下标区间 | 子数组 | 和 |
| --- | --- | ---: |
| [0, 1] | [1, 1] | 2 |
| [1, 2] | [1, 1] | 2 |

答案是 2，表示有两段符合要求。数值相同但位置不同，算不同子数组。下标 0 和 2 不能跳过中间元素单独组合，因为它们不连续。

子数组不一定只有两个数。nums = [1, 2, 3]、k = 3 时，[1, 2] 和 [3] 都符合要求，答案也是 2。不要把本题理解为“两数之和”。

## 从朴素思路到前缀和

先固定起点 left，再让终点 right 向右扩展，用一个变量累加这一段的和。每次和为 k 就让答案加一。这种双重循环需要 O(n²) 时间、O(1) 辅助空间，适合作为小输入的参考方法。

优化的关键是：不用重新计算每一段，只比较两个“从头加起”的和。

定义 P[t] 为前 t 个元素之和：

```text
nums = [2, 3, 4]
P[0] = 0          没取元素
P[1] = 2          2
P[2] = 5          2 + 3
P[3] = 9          2 + 3 + 4

P[3] - P[1] = 9 - 2 = 7
对应子数组 [3, 4]
```

一般地，下标闭区间 [left, right] 的和为：

```text
P[right + 1] - P[left]
```

要让这一段的和等于 k：

```text
当前前缀和 - 之前的某个前缀和 = k
之前的某个前缀和 = 当前前缀和 - k
```

因此从左到右扫描，每到一个终点，询问“此前有多少个前缀和等于 prefix − k”。用哈希表记录频次，就能一次得到以这个位置结尾的答案数量。

不需要真的创建 P 数组：只维护当前 prefix 与此前前缀和的频次即可。本题主分类为前缀和，哈希表用于加速查询。

**补充讲解：为什么不能直接套用普通滑动窗口？** 本题允许负数，加入一个数可能让和减小，移走一个数也可能让和增大。例如 [2, -1]、k = 1，若读到 2 就因为和过大而收缩，会漏掉之后完整的 [2, -1]。这里没有“和过大就缩小、过小就扩展”的简单单调关系。

## 变量分别记录什么

| 变量 | 类型或含义 | 特别注意 |
| --- | --- | --- |
| ans | 已找到的合法子数组数量 | 是整数，不是子数组列表，也不是元素和 |
| prefix | 从开头累加到当前元素的和 | 每轮执行 prefix += num |
| need | prefix − k | 要寻找的旧前缀和值 |
| counts | 前缀和值 → 此前出现次数 | 键不是下标，值也不是元素本身 |

初始化 counts = {0: 1} 的含义是：“还没读取任何元素时，前缀和 0 已经出现一次。”这代表一个可选择的区间起点边界，不代表 nums 里有一个额外的 0。

每轮的固定顺序：

1. 累加当前元素，得到 prefix。
2. 计算 need = prefix − k。
3. 查询 counts[need]，把匹配数量加入 ans。
4. 将当前 prefix 的出现次数加一，供后面的终点查询。

## 逐步推演与正确性

### 示例一如何得到2

nums = [1, 1, 1]，k = 2。初始 ans = 0、prefix = 0、counts = {0: 1}。

| 当前下标 | num | prefix | need | 查询到的次数 | 本轮新增区间 | 累计 ans |
| ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 0 | 1 | 1 | -1 | 0 | 无 | 0 |
| 1 | 1 | 2 | 0 | 1 | [0, 1] | 1 |
| 2 | 1 | 3 | 1 | 1 | [1, 2] | 2 |

每轮查询完成后，依次记录前缀和 1、2、3。最终返回 2。

### 一次为什么可能增加两个答案

nums = [1, -1, 1]，k = 1：

| 当前下标 | prefix | need | 查询前 counts | 新增数量 | 累计 ans |
| ---: | ---: | ---: | --- | ---: | ---: |
| 0 | 1 | 0 | {0: 1} | 1 | 1 |
| 1 | 0 | -1 | {0: 1, 1: 1} | 0 | 1 |
| 2 | 1 | 0 | {0: 2, 1: 1} | 2 | 3 |

最后一轮查询到 counts[0] = 2，两个旧前缀和 0 分别来自：

```text
边界 0：[] | [1, -1, 1]     去掉空前缀，留下整个数组
边界 2：[1, -1] | [1]        去掉前两个数，留下最后一个 1
```

两段都连续，只是起点不同。所以这轮加 2。第一个 [1] 在下标 0 那轮已经统计过，整个答案是 3。

### 为什么不漏解也不重复

处理下标 right 时，prefix 等于 P[right+1]；查询前的 counts 精确记录 P[0] 到 P[right] 的频次。

任意合法起点 left 都满足 P[left] = prefix − k，且 left ≤ right。每个符合条件的旧前缀对应一段完整的 [left, right]；反过来，每段以 right 结尾的合法子数组也对应一个这样的旧前缀。

所以 counts[need] 就是本轮应新增的数量。查询后记录 P[right+1]，保持下一轮需要的状态。每段子数组只在其唯一终点被统计，且同一终点下每个起点只计一次。

## 三种语言源码

以下是同一基础算法的三种语言版本，保留本次使用的 ans、prefix、need、counts 命名。源码补齐必要导入与注释；Python 展开更新分支，便于理解。

### Python 3

[源码](python/solution.py)。counts 是字典，先判断键是否存在，再读取次数。

```python
from typing import List


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        ans = 0
        prefix = 0
        # 空前缀的和为 0，出现一次，用于统计从下标 0 开始的子数组。
        counts = {0: 1}

        for num in nums:
            prefix += num
            need = prefix - k

            # 只查询此前的前缀；每次出现都对应一个合法起点。
            if need in counts:
                ans += counts[need]

            # 查询后才记录当前前缀，避免把空子数组算进去。
            if prefix in counts:
                counts[prefix] += 1
            else:
                counts[prefix] = 1

        return ans
```

### C++

[源码](cpp/solution.cpp)。与本次代码相比，关键修正是补上 counts[0] = 1；标准库名称显式加 std::，便于本地编译。

```cpp
#include <unordered_map>
#include <vector>

class Solution {
public:
    int subarraySum(std::vector<int>& nums, int k) {
        int ans = 0;
        int prefix = 0;
        std::unordered_map<int, int> counts;
        // 空前缀保证从下标 0 开始的子数组也能被统计。
        counts[0] = 1;

        for (int num : nums) {
            prefix += num;
            int need = prefix - k;
            if (counts.find(need) != counts.end()) {
                ans += counts[need];
            }
            // 必须先查后存；不存在的 int 值会先初始化为 0。
            counts[prefix]++;
        }
        return ans;
    }
};
```

### Java

[源码](java/Solution.java)。HashMap 通过 containsKey/get 查询，再通过 getOrDefault/put 更新次数。

```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int subarraySum(int[] nums, int k) {
        int ans = 0;
        int prefix = 0;
        Map<Integer, Integer> counts = new HashMap<>();
        // 空前缀保证从下标 0 开始的子数组也能被统计。
        counts.put(0, 1);

        for (int num : nums) {
            prefix += num;
            int need = prefix - k;
            if (counts.containsKey(need)) {
                ans += counts.get(need);
            }
            // 先查后存；getOrDefault 只读取，put 才插入或更新。
            counts.put(prefix, counts.getOrDefault(prefix, 0) + 1);
        }
        return ans;
    }
}
```

## 本次困惑与解答

本节记录本次实际提出的问题；额外知识在文中标为“补充讲解”。

### prefix等于0这个变量是干嘛的

prefix 用来保存“从数组开头加到当前位置”的和。初始还没读任何数，所以是 0。

```text
nums = [2, 3, 4]
初始 prefix = 0
读到 2：prefix = 2
读到 3：prefix = 5
读到 4：prefix = 9
```

它不是每次从 0 重新加，也不是当前元素的下标。need = prefix − k 则是要在旧前缀里寻找的值。

### counts等于零冒号一是什么类型

```python
counts = {0: 1}
```

这是 Python 的 dict（字典）。大括号中使用“键: 值”：

```text
键 0：前缀和为 0
值 1：目前出现过一次
```

如果后来又遇到一次前缀和 0，字典会变为 {0: 2}，不会增加第二个相同的键。不同位置得到的同一个前缀和值，其频次会累加。

### ans是干嘛的，为什么不是总加1

ans 是答案的数量，初始为 0。查询到几个旧前缀匹配，就有几个不同起点，因此增加几：

```python
if need in counts:
    ans += counts[need]
```

例如 counts = {0: 2, 1: 1}，need = 0，counts[need] 就是 2，ans 应增加 2。

ans += 1 只适用于本轮恰好找到一个答案的情况。它与 ans += counts[need] 是数量恰好为 1 时的等价写法，不能两句一起执行。

ans += counts[need] 等价于 ans = ans + counts[need]；它不会改变 counts 中的次数。

### 只看需要的数出现几次，不连续怎么办

counts 记录的是**从开头累加得到的前缀和**，不是“数组中某个元素出现几次”。

从整段开头到当前终点的和，减去开头连续一段的和，剩下的仍是一整段连续区间：

```text
[开头的一段] [剩下的连续区间]
 旧前缀和     希望其和为 k
[-------- 当前前缀和 --------]
```

不会从中间跳着挑元素。前面的 [1, -1, 1] 推演说明了：前缀和相同但边界不同，会得到不同起点的连续子数组，因此频次必须保留，不能只用集合判断存在。

### C++代码为什么漏掉了答案

本次提交的 C++ 初始化了空 counts，却漏写：

```cpp
counts[0] = 1;
```

例如 nums = [2, 3]、k = 5，读完 3 后 prefix = 5、need = 0。只有预先记录空前缀 0，才能统计从下标 0 开始的 [2, 3]。

这也解释了为什么它不是可有可无的“默认设置”。Python、Java 同样需要各自的初始化写法。

### 为什么必须先查询再记录当前前缀

查询时只能使用当前终点之前的前缀边界，保证区间非空。

例如 nums = [1]、k = 0，本来没有任何合法子数组：

```text
读到 1 后：prefix = 1，need = 1

正确顺序：
counts 只有 {0: 1}，找不到 1 → ans 不变
然后记录前缀和 1

错误顺序：
先记录 1，再查询 1 → 误加一个答案
相当于当前前缀减去自己，得到长度为 0 的空子数组
```

特别是 k = 0 时，need 就等于 prefix，顺序错误会在每轮把当前前缀自己也算进去。起始的空前缀 0 是一个合法的左边界；错误在于把**当前右边界**同时当成左边界，形成空区间。

## 语言差别与常用接口

| 目的 | Python 3 | C++ | Java |
| --- | --- | --- | --- |
| 创建频次表 | `counts = {0: 1}` | `std::unordered_map<int, int> counts;` 后赋初值 | `Map<Integer, Integer> counts = new HashMap<>();` 后 put 初值 |
| 初始化空前缀 | 已在字典字面量中完成 | `counts[0] = 1;` | `counts.put(0, 1);` |
| 遍历元素 | `for num in nums:` | `for (int num : nums)` | `for (int num : nums)` |
| 判断键存在 | `need in counts` | `counts.find(need) != counts.end()` | `counts.containsKey(need)` |
| 读取已有次数 | `counts[need]` | `counts[need]` 或迭代器的 second | `counts.get(need)` |
| 缺失时读作0 | `counts.get(key, 0)` | find 检查；本题 int 映射也可用下标默认插入 | `counts.getOrDefault(key, 0)` |
| 更新次数 | `counts[key] = 次数` | `counts[key]++;` | `counts.put(key, 次数);` |
| 返回答案类型 | `int` | `int` | `int` |

C++ 的 counts.find(need) 返回迭代器；与 end() 不同表示找到了键。end() 表示尾后位置，不是频次数值。本题源码先确认存在，再用下标读取。

缺失键时，下标操作差别很大：Python counts[key] 会抛 KeyError；C++ counts[key] 会插入一个默认值为 0 的 int；Java Map 不支持 counts[key]，get(key) 对缺失键返回 null，直接拆箱为 int 会报错。

Python 的更新可以压缩为：

```python
ans += counts.get(need, 0)
counts[prefix] = counts.get(prefix, 0) + 1
```

这两句替换完整源码中的查询与更新分支。get(key, 0) 的两个参数分别是“要查询的键”和“缺失时返回的默认值”；get 本身不插入键，第二行的赋值才写入字典。

Java 的对应写法：

```java
counts.put(prefix, counts.getOrDefault(prefix, 0) + 1);
```

从内到外读：取出旧次数（不存在则为 0）→ 加 1 → put 回同一个键。put 接收键和值，用于插入或覆盖；getOrDefault 只读取，不会把默认值写入表。这里的 Map 泛型使用包装类型 Integer，不能写 `Map<int, int>`。

这些名称属于标准库接口，counts、prefix 则是自己取的变量名。跨题复习见[哈希频次与默认值](../../../docs/language-cheatsheet.md#哈希频次与默认值)及[前缀和入门](../../../docs/prefix-sum.md)。

## 复杂度与边界

设 n 为 nums 的长度。使用哈希表，在查找和更新平均 O(1) 的条件下：

- 时间：平均 O(n)。没有枚举所有起点与终点，也没有每轮复制子数组。
- 辅助空间：O(n)，最多保存 n+1 个不同前缀和值。返回的是一个整数，输出空间 O(1)。
- 输入：只读取，不排序、不修改；C++ 引用参数也不意味着必须修改数组。

哈希查询的平均复杂度依赖哈希分布，不能把上述时间写成对所有哈希实现都无条件成立的最坏保证。

本题 n ≤ 20000、每个元素绝对值 ≤ 1000、k 绝对值 ≤ 10000000。前缀和绝对值最多 20000000，need 绝对值最多 30000000；最多有 n(n+1)/2 = 200010000 个子数组，所以本题 C++/Java 的 32 位 int 足够。推广到更大范围时应重新检查，必要时改用 long long / long；Python 整数没有固定 32 位上限。

| nums | k | 答案 | 检查点 |
| --- | ---: | ---: | --- |
| [1, 1, 1] | 2 | 2 | 重叠区间与不同起点 |
| [1, 2, 3] | 3 | 2 | 单元素子数组也合法 |
| [2, 3] | 5 | 1 | 空前缀初始化 |
| [1] | 0 | 0 | 先存后查会误算空区间 |
| [0] | 0 | 1 | 原数组中的零是非空合法答案 |
| [0, 0, 0] | 0 | 6 | 重复前缀，不能只加一 |
| [1, -1, 1] | 1 | 3 | 同一轮可能出现多个起点 |
| [-1, -1, 1] | -1 | 3 | 负数目标与负前缀 |
| [2, -1] | 1 | 1 | 不能按和过大就收缩窗口 |

自动验证入口见[测试说明](../../../tests/README.md)。小输入通过枚举所有连续非空区间并累加的独立暴力参考比较，大输入使用可推导的预期值；同时检查三种语言的输入没有被修改。本地验证与力扣平台提交分别记录，不以本地测试代替平台通过记录。

## 复习自测

1. [1, 1, 1]、k = 2 为什么答案为 2？为什么不能任意选两个位置？
2. 如何从 P[right+1] − P[left] = k 推导出 need = prefix − k？
3. counts 的键和值分别是什么？为什么初始为 {0: 1}？
4. 手算 [1, -1, 1]、k = 1，解释最后一轮为什么增加 2。
5. 用 [1]、k = 0 解释先查后存；用 [2, 3]、k = 5 解释初始化。
6. 分别写出 Python、C++、Java 的查键与频次更新，说明缺失键时的差别。
