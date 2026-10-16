# LeetCode 15 · 三数之和

[返回首页](../../../README.md) · [双指针分类](../../../categories/README.md#双指针) · [力扣原题](https://leetcode.cn/problems/3sum/)

| 难度 | 主分类 | 标签 | 语言 |
| --- | --- | --- | --- |
| 中等 | 双指针 | 数组、排序、左右指针、去重 | C++ / Java / Python 3 |

## 目录

- [题意与例子](#题意与例子)
- [从三重枚举到排序加双指针](#从三重枚举到排序加双指针)
- [逐步推演与正确性](#逐步推演与正确性)
- [三种语言源码](#三种语言源码)
- [本次困惑与解答](#本次困惑与解答)
- [语言差别与常用接口](#语言差别与常用接口)
- [复杂度与边界](#复杂度与边界)
- [复习自测](#复习自测)

## 题意与例子

在数组中选择三个不同位置，使三个数之和为 0，返回所有不重复的三元组。

```text
输入：[-1, 0, 1, 2, -1, -4]
结果：[[-1, -1, 2], [-1, 0, 1]]
```

返回的是三个数的值，不是下标。两个不同位置上的 -1 可以同时使用，所以 [-1, -1, 2] 合法；同一组值不能因位置不同或排列顺序不同而重复返回。答案中三元组的顺序不限。

本题允许重排输入，本页代码通过排序直接修改原数组。如果调用方需要保留原顺序，需在排序前复制，额外计入复制空间。

## 从三重枚举到排序加双指针

朴素做法枚举 i < j < k 的所有组合，时间 O(n³)，然后还要按数值对结果去重。

改进的关键是：**先固定一个数，把三数之和变成在有序区间里找另外两个数。**

```text
nums[i] + nums[left] + nums[right] = 0
          nums[left] + nums[right] = -nums[i]
```

流程：

1. 排序，让相同值相邻，也让数值随下标非递减。
2. 用 i 固定第一个数，i 最多到 n−3，后面要留至少两个位置。
3. left 从 i+1 开始，right 从 n−1 开始，保证 i < left < right。
4. 和偏小，left 右移；和偏大，right 左移。
5. 和为 0，保存答案，两边移动并跳过刚用过的相同值。
6. 外层遇到重复的第一个数时跳过。

对照前面两道题：

| 题目 | 双指针的移动依据 |
| --- | --- |
| 移动零 | 遇到非零时交换到慢指针位置 |
| 盛最多水的容器 | 移动较矮的一端 |
| 三数之和 | 排序后，根据三数之和与 0 的大小移动 |

这里不是比较哪一侧更矮。每道题的移动规则都要结合题意理解。

## 逐步推演与正确性

先排序：

```text
nums = [-4, -1, -1, 0, 1, 2]
下标 =   0   1   2  3  4  5
```

| i | left | right | 三个数 | 和 | 操作 |
| ---: | ---: | ---: | --- | ---: | --- |
| 0 | 1 | 5 | -4、-1、2 | -3 | left 加一 |
| 0 | 2 | 5 | -4、-1、2 | -3 | left 加一 |
| 0 | 3 | 5 | -4、0、2 | -2 | left 加一 |
| 0 | 4 | 5 | -4、1、2 | -1 | left 加一后相遇，结束本轮 |
| 1 | 2 | 5 | -1、-1、2 | 0 | 保存 [-1, -1, 2]，两边移动并去重 |
| 1 | 3 | 4 | -1、0、1 | 0 | 保存 [-1, 0, 1]，两边移动后交错 |
| 2 | — | — | 第一个数仍是 -1 | — | continue，跳过这个 i |
| 3 | 4 | 5 | 0、1、2 | 3 | right 减一后相遇 |

表中“left 加一”表示左指针向右走，不是数值向左移动。

### 为什么和小就移动left

固定 i、left，如果当前与最右侧组成的和已经小于 0，那么让 right 向左只会使右值更小或相等，不可能达到 0。因此可以排除当前 left，尝试更大的左值。

和大于 0 时同理：固定 i、right，继续增加 left 不会让和变小，所以排除当前 right。

### 找到答案为什么两边都能移动

固定 i 和一个左值后，满足总和为 0 的右值是唯一确定的。若继续使用相同左值或相同右值，只会得到相同数值组合。因此记录答案后，两边各移动一步，再跳过刚用过的值，不会漏掉新的三元组。

每个固定的首值只搜索一次，每次匹配后跳过相同左右值，所以不会产生重复答案。i < left < right 也保证三个位置互不相同。

## 三种语言源码

代码保持本次练习的基础版本：先排序、固定 i、三分支扫描、两处去重。仅把每轮重复写的三数之和提取成 total，便于阅读和避免同一轮更新指针后重新计算条件。

### Python 3

[源码](python/solution.py)。条件分支写 elif，添加三元组用 append。

```python
class Solution:
    def threeSum(self, nums):
        nums.sort()  # 排序后才能按和的大小移动指针
        n = len(nums)
        ans = []

        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue  # 相同的值只作为第一个数查找一次

            left = i + 1
            right = n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total == 0:
                    ans.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    # 跳过刚用过的值，避免生成重复三元组
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif total < 0:
                    left += 1
                else:
                    right -= 1

        return ans
```

### C++

[源码](cpp/solution.cpp)。包含必要头文件并显式写 std::，可在本地测试入口中直接编译。

```cpp
#include <algorithm>
#include <vector>

class Solution {
public:
    std::vector<std::vector<int>> threeSum(std::vector<int>& nums) {
        std::sort(nums.begin(), nums.end());
        int n = static_cast<int>(nums.size());
        std::vector<std::vector<int>> ans;

        for (int i = 0; i < n - 2; ++i) {
            if (i > 0 && nums[i] == nums[i - 1]) {
                continue;
            }
            int left = i + 1;
            int right = n - 1;

            while (left < right) {
                int total = nums[i] + nums[left] + nums[right];
                if (total == 0) {
                    ans.push_back({nums[i], nums[left], nums[right]});
                    ++left;
                    --right;
                    // 移动后，与刚用过的左值、右值比较
                    while (left < right && nums[left] == nums[left - 1]) {
                        ++left;
                    }
                    while (left < right && nums[right] == nums[right + 1]) {
                        --right;
                    }
                } else if (total < 0) {
                    ++left;
                } else {
                    --right;
                }
            }
        }
        return ans;
    }
};
```

### Java

[源码](java/Solution.java)。List 是接口，ArrayList 用于创建结果容器，Arrays 提供排序和 asList 方法。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        int n = nums.length;
        List<List<Integer>> ans = new ArrayList<>();

        for (int i = 0; i < n - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) {
                continue;
            }
            int left = i + 1;
            int right = n - 1;

            while (left < right) {
                int total = nums[i] + nums[left] + nums[right];
                if (total == 0) {
                    // asList 组成一组三个数，add 将这一组放进答案
                    ans.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    left++;
                    right--;
                    while (left < right && nums[left] == nums[left - 1]) {
                        left++;
                    }
                    while (left < right && nums[right] == nums[right + 1]) {
                        right--;
                    }
                } else if (total < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        return ans;
    }
}
```

## 本次困惑与解答

以下来自本次练习的实际问题与代码修改。

### 怎么把一个三元组放进ans

Python 的 ans 是外层列表，里面每个元素也是一个列表：

```python
ans = []
ans.append([-1, -1, 2])
ans.append([-1, 0, 1])
# [[-1, -1, 2], [-1, 0, 1]]
```

放入 nums[i]、nums[left]、nums[right]，才是数值；放入 i、left、right 就成了下标。

### Python为什么不能写else if

Python 使用 elif，C++/Java 使用 else if：

```python
if total == 0:
    pass
elif total < 0:
    pass
else:
    pass
```

每个分支末尾有冒号，代码块要缩进。

### 为什么会超出内存限制

本次 Python 在找到答案时只执行 append，没有移动左右指针。下一轮还是原来的三个数，条件仍为真，不断追加同一个三元组，直到内存不足。

因此找到答案后也必须推进状态：

```python
ans.append([nums[i], nums[left], nums[right]])
left += 1
right -= 1
```

### 为什么C++会超时

本次 C++ 的一版代码漏了排序，还漏了和偏小、偏大时的分支。和不等于 0 时，两个指针完全不动，while 一直检查同一组位置，形成死循环。

排序与分支是两个不同问题：排序保证移动规则正确；每种情况都移动指针，保证循环能够结束。只补排序不能解决死循环。

### 如何给第一个数去重，连续三个相同值也行吗

排序后：

```python
if i > 0 and nums[i] == nums[i - 1]:
    continue
```

for 每取到一个新 i 都会检查，不是只比较一次。

| nums = [-1, -1, -1, 0, 1, 2] | 判断 | 操作 |
| --- | --- | --- |
| i = 0 | 没有前一个元素 | 正常搜索 |
| i = 1 | 当前 -1 等于前一个 -1 | 跳过 |
| i = 2 | 当前 -1 等于前一个 -1 | 跳过 |
| i = 3 | 当前 0 不等于前一个 -1 | 正常搜索 |

continue 只是结束这一轮外层循环，不删除数组元素。下标 1 被跳过作为 i 的搜索后，仍存在于数组中，下标 2 仍可与它比较。

重复的 -1 仍能作为 left 或 right，因此不会漏掉 [-1, -1, 2]。不要直接把整个输入数组转成集合去掉重复值。

### 找到答案后的去重为什么要用while

连续相同值可能不止两个。if 最多跳过一个，while 会一直跳到下一个不同值或指针相遇。

先执行 left += 1、right -= 1，然后：

```python
while left < right and nums[left] == nums[left - 1]:
    left += 1

while left < right and nums[right] == nums[right + 1]:
    right -= 1
```

左边与 left−1 比，右边与 right+1 比，是与刚用过的值比较。本次 Java 曾写成向尚未使用的一侧比较，不能正确表达“跳过刚用过的重复值”。

### 外层已经有left小于right，内层为什么还要判断

外层 while 只在每轮开始时检查条件，进入循环体后不会持续监控。指针移动可能让原先成立的条件失效：

```text
进入外层循环时：left = 1，right = 3
找到答案后：    left = 2，right = 2
```

此时外层循环体还没执行完。内层如果不再检查，可能继续越过相遇位置，甚至读出数组范围，例如全零数组一直去重的情况。

内层去重自己也会移动指针，因此每跳过一个值都需要再检查。Python 的 and、C++/Java 的 && 会短路：前面的 left < right 不成立，就不再读取后面的数组元素。

### 为什么Java不能写三个独立的if

找到答案后指针已经变了；三个独立 if 会继续执行后面的判断，甚至在同一轮再次移动。它与“根据本轮总和选择一种处理方式”不是一回事。

写成 if / else if / else，并先保存 total，每轮只选一个分支。与 Python 已通过的版本保持同一逻辑结构。

### C++的vector如何定义和添加

```cpp
std::vector<int> nums;                    // 一维整数动态数组
std::vector<std::vector<int>> ans;        // 多个整数数组
ans.push_back({nums[i], nums[left], nums[right]});
```

push_back 相当于本题 Python 的 append。此处 {} 是列表初始化语法，按外层容器的元素类型构造一个 `vector<int>`：

```cpp
std::vector<int> group = {nums[i], nums[left], nums[right]};
ans.push_back(group);
```

大括号不总表示“数组”，在这个位置用于初始化内层 vector。

### Java的ans如何定义

```java
List<List<Integer>> ans = new ArrayList<>();
```

外层 List 保存多组结果，内层 `List<Integer>` 保存一组三个整数。泛型参数用 Integer，不能写 `List<int>`。List 是接口，`new ArrayList<>()` 创建可以增添元素的具体容器。

### Java的Arrays.asList是固定写法吗

Arrays.asList 是标准库方法名，类名、大小写和方法名固定，括号中的元素由自己提供；参数个数也不限于三个。

```java
List<Integer> group = Arrays.asList(nums[i], nums[left], nums[right]);
ans.add(group);
```

asList 负责把这三个值组织成一个列表；add 才负责将这一组放入 ans。也能不用 asList，手动组装：

```java
List<Integer> group = new ArrayList<>();
group.add(nums[i]);
group.add(nums[left]);
group.add(nums[right]);
ans.add(group);
```

返回的 asList 列表长度固定，不能 add/remove；本题不再改变内层列表长度，所以适合使用。外层 ans 是新建的 ArrayList，可以继续 add。方法说明见 [Java Arrays 官方文档](https://docs.oracle.com/javase/8/docs/api/java/util/Arrays.html#asList-T...-)。

补充讲解：本题传入的是三个 int 表达式，会装箱成 Integer。不能把它与 Arrays.asList(nums) 混淆；如果 nums 是 int[]，后者会把整个基本类型数组视作一个元素，并不是把每个 int 变成一个 Integer 元素。

### Java类名为什么反复报找不到

本次拼写与所属类的修正：

| 错误 | 正确 | 用途 |
| --- | --- | --- |
| `new ArryList<>()` | `new ArrayList<>()` | 创建列表 |
| Arrys.sort(nums) | Arrays.sort(nums) | 排序 |
| ArryList.asList(...) | Arrays.asList(...) | 组成列表 |

Arrays 与 ArrayList 是两个不同的类，不能因为名字相似就互换。完整 import 见 Java 源码。

## 语言差别与常用接口

| 操作 | Python | C++ | Java |
| --- | --- | --- | --- |
| 排序 | nums.sort() | std::sort(nums.begin(), nums.end()) | Arrays.sort(nums) |
| 定义结果 | `ans = []` | `std::vector<std::vector<int>> ans` | `List<List<Integer>> ans = new ArrayList<>()` |
| 添加三元组 | ans.append([a, b, c]) | ans.push_back({a, b, c}) | ans.add(Arrays.asList(a, b, c)) |
| 并且 | and | && | && |
| 条件分支 | if / elif / else | if / else if / else | if / else if / else |
| 长度 | len(nums) | nums.size() | nums.length |

并且条件从左向右短路，所以 i > 0 要放在访问 nums[i−1] 的前面。源码提取 total 后，不会重复书写和的表达式，便于保持三个分支互斥。

排序、二维结果和添加方法的通用语法见[语言速查表](../../../docs/language-cheatsheet.md#排序与二维结果)。

## 复杂度与边界

固定一个 i 后，left 只向右、right 只向左，总移动次数 O(n)，不是每一层 while 都相乘。因此双指针部分 O(n²)，整体在常用标准排序实现下为 O(n²)。

双指针扫描本身只保存几个变量，额外空间 O(1)，但这不包含排序工作空间与结果。若排序工作空间记为 S_sort，答案有 k 组三元组，则含返回值的额外空间为 O(S_sort + k)。原地排序表示修改输入，不等于排序内部一定完全不使用额外内存。

本题数值在 ±10^5 内，三个数相加在 ±300000 内，C++ 常见 32 位 int 和 Java int 足够。若扩展到完整 int 范围，需要另行使用更宽类型。

| 输入 | 结果 | 检查点 |
| --- | --- | --- |
| [-1, 0, 1, 2, -1, -4] | [[-1, -1, 2], [-1, 0, 1]] | 基本示例 |
| [0, 1, 1] | [] | 无解 |
| [0, 0, 0] | [[0, 0, 0]] | 三个相同值仍可组成答案 |
| [0, 0, 0, 0] | [[0, 0, 0]] | 去重与内层边界 |
| [-1, -1, -1, 0, 1, 2] | [[-1, -1, 2], [-1, 0, 1]] | 外层连续三个重复值 |
| [-2, 0, 0, 2, 2] | [[-2, 0, 2]] | 左右重复值 |
| [-100000, 0, 100000] | [[-100000, 0, 100000]] | 本题数值边界 |

本地验证会与枚举所有三个不同下标的暴力参考比较，不依赖答案的外层顺序；还会单独检查结果中是否有重复三元组，避免“先转集合再比较”掩盖错误。

补充优化：排序后如果 nums[i] > 0，后续三数和不可能为 0，可以提前结束外层循环。基础源码保留本次手写的结构，先掌握正确扫描与去重。

## 复习自测

1. 三数之和为什么可以排序，而两数之和返回原下标时不能直接丢失位置关系？
2. 固定 i 后，和偏小为什么可以排除当前 left？和偏大呢？
3. 第一项连续重复三个，为什么一个 if 配合 continue 仍能跳过后两项？
4. 内层去重为什么是 while，并比较 left−1、right+1？
5. 外层 while 已经检查条件，内层为什么还需要检查？and/&& 起什么作用？
6. 分别用三种语言写出添加三元组；解释 C++ {}、Java Arrays.asList 和 ans.add 各自的作用。
