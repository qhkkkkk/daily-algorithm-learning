# LeetCode 438 · 找到字符串中所有字母异位词

[返回首页](../../../README.md) · [滑动窗口分类](../../../categories/README.md#滑动窗口) · [力扣原题](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)

| 难度 | 主分类 | 标签 | 语言 |
| --- | --- | --- | --- |
| 中等 | 滑动窗口 | 字符串、固定长度窗口、字母计数、数组比较 | C++ / Java / Python 3 |

## 目录

- [题意与例子](#题意与例子)
- [从朴素检查到固定长度窗口](#从朴素检查到固定长度窗口)
- [先理解字母计数](#先理解字母计数)
- [窗口如何移动](#窗口如何移动)
- [完整推演与正确性](#完整推演与正确性)
- [三种语言源码](#三种语言源码)
- [本次困惑与解答](#本次困惑与解答)
- [语言差别与常用接口](#语言差别与常用接口)
- [复杂度与边界](#复杂度与边界)
- [复习自测](#复习自测)

## 题意与例子

在字符串 s 中找到所有与 p 互为字母异位词的连续子串，返回它们的起始下标。字母异位词允许顺序不同，但每个字母的出现次数必须相同。

```text
s = "cbaebabacd"
p = "abc"
答案：[0, 6]

起点 0 的 "cba" 与 abc 字母次数相同
起点 6 的 "bac" 与 abc 字母次数相同
```

返回的是起点，不是子串本身。不需要修改输入，也不能排序整个 s，否则会破坏原来的连续区间与下标。

另一个例子 s = "abab"、p = "ab"，答案是 [0, 1, 2]。窗口可以重叠，不能找到一次就跳过整段。

## 从朴素检查到固定长度窗口

设 n = len(s)、m = len(p)。字母次数相同，长度一定也相同，所以只用检查长度为 m 的子串。

朴素做法是枚举每个起点，取出 m 个字符后重新计数，或将子串排序后与排序的 p 比较。重新计数需要反复处理大量重叠字符；每个窗口单独排序还会增加开销。

相邻窗口几乎一样：

```text
[c b a] e b a b a c d
 c [b a e] b a b a c d
```

只有一个 c 离开、一个 e 进入，b 和 a 留在里面。因此维护一份窗口计数，每次减去旧字符、加上新字符即可。

与[无重复字符的最长子串](../0003-longest-substring-without-repeating-characters/README.md)对照：

| 题目 | 窗口长度 | 维护什么 | 怎么移动 |
| --- | --- | --- | --- |
| 第 3 题 | 可以变化 | 当前窗口内字符是否重复 | 右端前进，冲突时左端持续收缩 |
| 第 438 题 | 固定为 m | 各字母出现次数 | 每次移出一个，再移入一个 |

本题不会因为当前不匹配就额外缩短窗口；要继续保持长度 m，检查下一个起点。

## 先理解字母计数

计数列表存的是次数，不是字母：

```text
位置： 0  1  2  3 …… 25
字母： a  b  c  d …… z
```

例如 p = "aba"，从左到右统计：

| 读到的字符 | a 的次数 | b 的次数 |
| --- | ---: | ---: |
| 第一个 a | 1 | 0 |
| b | 1 | 1 |
| 最后一个 a | 2 | 1 |

最终列表的开头是 [2, 1, 0, …]。这是示意，实际数组有 26 项。

使用两份计数：

- target：p 的字母次数，统计好后不再变化。
- window：当前窗口的字母次数，随着窗口移动而变化。

例如 target 来自 abc，window 来自 cba：

| 字母 | a | b | c | d | e |
| --- | ---: | ---: | ---: | ---: | ---: |
| target | 1 | 1 | 1 | 0 | 0 |
| window | 1 | 1 | 1 | 0 | 0 |

其余字母也全为 0，因此两份计数相同，当前窗口就是异位词。

补充讲解：不能只比较字符集合。aab 和 abb 都只含 a、b，但出现次数不同；本题必须保留频次。

## 窗口如何移动

先统计 s 的前 m 个字符，检查起点 0。然后：

```python
for right in range(m, n):
```

right 表示新进入窗口的字符下标，从 m 开始，不是从 0 开始。

以 m = 3 为例，第一次右移：

```text
下标： 0  1  2  3  4  5  6  7  8  9
字符： c  b  a  e  b  a  b  a  c  d
旧窗：[c  b  a]
新窗：   [b  a  e]

right = 3
出去的是 s[0] = c
进来的是 s[3] = e
新窗口起点是 1
```

三个下标要区分：

| 表达式 | 含义 | 第一次移动 |
| --- | --- | ---: |
| right | 新进入的字符位置，也是新窗口右端 | 3 |
| right − m | 旧窗口最左边、此次离开的字符位置 | 0 |
| right − m + 1 | 新窗口的起点 | 1 |

right−m 是离开的位置，不能当成新起点记录。新窗口是闭区间 [right−m+1, right]，恰有 m 个字符。

这一步对次数的影响：

| 状态 | a | b | c | e |
| --- | ---: | ---: | ---: | ---: |
| 旧窗口 cba | 1 | 1 | 1 | 0 |
| 移出 c 后 | 1 | 1 | 0 | 0 |
| 再移入 e 后，新窗口 bae | 1 | 1 | 0 | 1 |

减去旧字符后，计数暂时只含 m−1 个字符。必须再加入新字符，恢复为完整窗口后，才比较并决定是否记录。

## 完整推演与正确性

对 s = cbaebabacd、p = abc，先检查第一个窗口，再向右移动：

| right | 移出字符 | 移入字符 | 新起点 | 当前子串 | 是否匹配 | ans |
| ---: | --- | --- | ---: | --- | --- | --- |
| — | — | 初始化前三个 | 0 | cba | 是 | [0] |
| 3 | c（下标 0） | e | 1 | bae | 否 | [0] |
| 4 | b（下标 1） | b | 2 | aeb | 否 | [0] |
| 5 | a（下标 2） | a | 3 | eba | 否 | [0] |
| 6 | e（下标 3） | b | 4 | bab | 否 | [0] |
| 7 | b（下标 4） | a | 5 | aba | 否 | [0] |
| 8 | a（下标 5） | c | 6 | bac | 是 | [0, 6] |
| 9 | b（下标 6） | d | 7 | acd | 否 | [0, 6] |

移出和移入恰好是同一个字母时，先减再加，最终计数不变，仍然正确。

正确性依据：

1. 初始化后，window 精确记录 s[0:m] 的字母次数。
2. 每次移走 s[right−m]，再加入 s[right]，会将旧窗口的计数精确更新成新窗口的计数。
3. 两份计数相同，当且仅当每种字母的次数相同，也就是异位词。
4. 第一个窗口与后续每个窗口都检查一次，起点依次为 0 到 n−m，不漏解、不重复记录。

n < m 时不存在长度足够的窗口，直接返回空答案。

## 三种语言源码

沿用本次完成的基础实现。将原变量名 widows 统一为更准确的 window，补齐必要导入与注释；没有改变扫描逻辑。

### Python 3

[源码](python/solution.py)。ord 完成字符到计数位置的转换，列表的 == 比较对应元素。

```python
class Solution:
    def findAnagrams(self, s, p):
        m = len(p)
        n = len(s)
        ans = []
        if m > n:
            return ans

        target = [0] * 26
        window = [0] * 26

        for ch in p:
            index = ord(ch) - ord('a')
            target[index] += 1

        # 先统计第一个窗口 s[0:m]
        for i in range(m):
            index = ord(s[i]) - ord('a')
            window[index] += 1

        if window == target:
            ans.append(0)

        # right 是新进入窗口的字符下标，从 m 开始
        for right in range(m, n):
            old_index = ord(s[right - m]) - ord('a')
            window[old_index] -= 1
            new_index = ord(s[right]) - ord('a')
            window[new_index] += 1
            if window == target:
                ans.append(right - m + 1)

        return ans
```

### C++

[源码](cpp/solution.cpp)。保留常见的 string 按值接口；头文件与 std:: 显式写出，便于本地编译。

```cpp
#include <string>
#include <vector>

class Solution {
public:
    std::vector<int> findAnagrams(std::string s, std::string p) {
        int m = static_cast<int>(p.size());
        int n = static_cast<int>(s.size());
        std::vector<int> ans;
        if (m > n) {
            return ans;
        }

        std::vector<int> target(26, 0);
        std::vector<int> window(26, 0);
        for (char ch : p) {
            int index = ch - 'a';
            ++target[index];
        }
        for (int i = 0; i < m; ++i) {
            int index = s[i] - 'a';
            ++window[index];
        }
        if (window == target) {
            ans.push_back(0);
        }

        for (int right = m; right < n; ++right) {
            int old_index = s[right - m] - 'a';
            --window[old_index];
            int new_index = s[right] - 'a';
            ++window[new_index];
            // vector 的 == 比较长度与对应元素
            if (window == target) {
                ans.push_back(right - m + 1);
            }
        }
        return ans;
    }
};
```

### Java

[源码](java/Solution.java)。String 使用 length()/charAt()，int[] 内容比较使用 Arrays.equals。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        int m = p.length();
        int n = s.length();
        List<Integer> ans = new ArrayList<>();
        if (m > n) {
            return ans;
        }

        int[] target = new int[26];
        int[] window = new int[26];
        for (int i = 0; i < m; i++) {
            int index = p.charAt(i) - 'a';
            target[index]++;
        }
        for (int i = 0; i < m; i++) {
            int index = s.charAt(i) - 'a';
            window[index]++;
        }
        if (Arrays.equals(window, target)) {
            ans.add(0);
        }

        for (int right = m; right < n; right++) {
            int old_index = s.charAt(right - m) - 'a';
            window[old_index]--;
            int new_index = s.charAt(right) - 'a';
            window[new_index]++;
            // Java 数组比较内容用 Arrays.equals，不能用 ==
            if (Arrays.equals(window, target)) {
                ans.add(right - m + 1);
            }
        }
        return ans;
    }
}
```

## 本次困惑与解答

以下问题来自本次对话，补充知识另行标注。

### ord(ch)是什么，为什么减去ord('a')

ord 是 Python 内置函数，接收一个字符并返回它的 Unicode 编码值：

```python
ord('a')  # 97
ord('b')  # 98
ord('c')  # 99
```

ch 是变量名，ch = 'b' 时，ord(ch) 就是 ord('b')。小写英文字母编码连续，因此：

```python
index = ord(ch) - ord('a')
# 如果 ch 是 b：98 - 97 = 1
window[index] += 1
# 相当于 window[1] += 1，即 b 的次数加一
```

不用背 97，只要记住“相对于 a 的位置”。本题只有小写英文字母，才可以用 26 个位置解决；不是所有文字都适用这个映射。[Python ord 官方说明](https://docs.python.org/3/library/functions.html#ord)。

### window等于target到底在比什么

在本题，window 与 target 存的是字母次数，比较它们就是比较各字母频次。例如 abc 与 cba 的顺序不同，但对应计数完全相同；bae 少了 c、多了 e，对应计数不同。

Python 的列表相等比较是内置行为：长度相同，而且每个对应位置的元素相等，整个比较才为 True。

```python
[1, 2, 3] == [1, 2, 3]  # True
[1, 2, 3] == [1, 3, 2]  # False
```

Python 本身只是在比较列表。每个下标分别代表某个字母，是我们设计的数据含义。参见 [Python 序列比较](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)。

### old_char为什么取s[right减m]

old_char = s[right−m] 只取出旧字符，并不删除原字符串。真正变化的是后面的计数：

```python
old_char = s[right - m]
old_index = ord(old_char) - ord('a')
window[old_index] -= 1
```

因为 right 是新窗口右端，而窗口长度固定为 m，新起点是 right−m+1；紧挨在它前面的 right−m 正是本次离开的旧位置。

本次疑问“right 刚开始不是 0 吗”的关键在于分清两个循环：前面的 i 从 0 开始，用来初始化；后面的 right 从 m 开始，用来滑动。第一个窗口已经处理过，不需要再从 0 开始加入字符。

### C++计数数组为什么用圆括号

```cpp
std::vector<int> target(26, 0);
```

表示 26 个元素，每个为 0。它不是：

```cpp
std::vector<int> target{26, 0};  // 只有两个元素：26 和 0
```

C++ 本题用 char 表示字符，可直接写 ch−'a' 求 a～z 的计数下标。不是把字符当成已经存在于 vector 里的元素，而是先计算其对应位置。

### C++为什么报idnex未声明

本次定义的是 index，使用时拼成了 idnex：

```cpp
int index = ch - 'a';
window[index]++;  // 名字必须与定义一致
```

这属于变量名拼写错误，不是 vector 不支持下标。

### C++右移循环为什么不能写i加加

本次写过：

```cpp
// 错误示范
for (int right = m; right < n; i++)
```

循环使用的是 right，应该更新 right：

```cpp
for (int right = m; right < n; right++)
```

前一个 for 中定义的 i 只在那个循环的作用域内有效。即使另有同名 i 可用，更新它也不能推进当前 right。检查 for 时，要一起看初始化变量、条件和步进是否对应。

### Java定义与取字符如何转换

```java
List<Integer> ans = new ArrayList<>();
int[] target = new int[26];  // 默认全为 0
int[] window = new int[26];

int n = s.length();
char ch = s.charAt(i);
int index = ch - 'a';
```

String 的长度是 length() 方法，数组长度是 length 属性，字符串不能直接写 s[i]。charAt(i) 返回 char，字符相减得到计数下标。

### Java为什么要用Arrays.equals

Java 数组的 == 判断两个引用是否指向同一个数组，不会比较每个元素。独立创建的两个零数组，用 == 比较也为 false：

```java
int[] a = new int[26];
int[] b = new int[26];

boolean sameReference = a == b;            // false
boolean sameContent = Arrays.equals(a, b); // true
```

所以本题使用 Arrays.equals(window, target)，先确认内容相等，再 ans.add(起点)。需要 import java.util.Arrays；完整导入见源码。[Arrays.equals 官方说明](https://docs.oracle.com/javase/8/docs/api/java/util/Arrays.html#equals-int:A-int:A-)。

## 语言差别与常用接口

| 操作 | Python | C++ | Java |
| --- | --- | --- | --- |
| 字符串长度 | len(s) | s.size() | s.length() |
| 第 i 个字符 | s[i] | s[i] | s.charAt(i) |
| 26 个零 | `[0] * 26` | `vector<int>(26, 0)` | `new int[26]` |
| 字母下标 | ord(ch) − ord('a') | ch − 'a' | ch − 'a' |
| 内容比较 | window == target | vector 的 window == target | Arrays.equals(window, target) |
| 添加起点 | ans.append(start) | ans.push_back(start) | ans.add(start) |

注意本表的 C++ 比较对象是 vector；不要直接推广为原生数组也可用 == 比较内容。统一语法说明见[字符计数与数组比较](../../../docs/language-cheatsheet.md#字符计数与数组比较)。

Python 的 window 与 target 应分开创建。如果写 window = target，就会让两个名字指向同一个列表，修改窗口时也会改到目标计数。当前源码没有这个问题，这是补充讲解。

## 复杂度与边界

初始化两份计数需要 O(m)，随后每次移动修改两个位置，并比较固定 26 个计数。n >= m 时：

```text
时间：O(m + 26 × (n−m+1))，字母表固定时写作 O(n+m)
计数数组辅助空间：O(26)，固定字母表下为 O(1)
输出空间：O(k)，k 是匹配起点数量，最多 n−m+1
```

比较数组不是抽象上的“一次操作”，本题是最多比较 26 项；字母表大小固定，所以仍是线性扫描。

C++ 源码保留 string 按值参数，调用方传入左值字符串时可能额外复制 O(n+m) 数据，不能把这些副本与窗口本身的常数空间混为一谈。若使用 const string& 接口，可避免这些参数副本。Java/Python 不会因本题扫描而复制整个输入字符串。

本题 s、p 都非空，长度不超过 30000，且只有小写英文字母；代码依据该约束编写。

| s | p | 答案 | 检查点 |
| --- | --- | --- | --- |
| cbaebabacd | abc | [0, 6] | 基本例子 |
| abab | ab | [0, 1, 2] | 重叠匹配 |
| aaa | aa | [0, 1] | 重复字母和次数 |
| a | a | [0] | 最短、首窗口就是答案 |
| a | b | [] | 无解 |
| ab | abc | [] | p 比 s 长 |
| aabb | abb | [1] | 字母种类相同也要检查次数 |
| zzzz | zz | [0, 1, 2] | 字母表末尾与重叠 |

小输入用“枚举每个子串后排序”的参考方法交叉检查，避免照抄滑动窗口更新逻辑。大输入使用可直接推导的预期结果。验证是本地测试，不等于宣称已替用户提交力扣判题。

## 复习自测

1. 异位词为什么能用字母次数判断？为什么只用集合不够？
2. ord(ch)−ord('a') 返回的是什么，window[index] 记录什么？
3. 第一个窗口如何初始化，为什么之后 right 从 m 开始？
4. 解释 right、right−m、right−m+1，并手动推演第一次移动。
5. 为什么先移出再移入，完成后才比较？移出与移入字母相同时会怎样？
6. Python 列表、C++ vector、Java int[] 的内容比较各怎么写？为什么 vector 的 (26, 0) 不能改成 {26, 0}？
