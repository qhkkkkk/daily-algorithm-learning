# LeetCode 3 · 无重复字符的最长子串

[返回首页](../../../README.md) · [滑动窗口分类](../../../categories/README.md#滑动窗口) · [力扣原题](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)

| 难度 | 主分类 | 标签 | 语言 |
| --- | --- | --- | --- |
| 中等 | 滑动窗口 | 字符串、双指针、哈希集合 | C++ / Java / Python 3 |

本题的核心不是背模板，而是理解：**当前窗口可以缩短，已经记住的最长答案不会变小；新字符与窗口任意位置重复，都要处理。**

## 目录

- [题意与例子](#题意与例子)
- [从朴素思路到主要解法](#从朴素思路到主要解法)
- [关键变量与执行顺序](#关键变量与执行顺序)
- [逐步推演](#逐步推演)
- [为什么正确](#为什么正确)
- [三种语言源码](#三种语言源码)
- [本次困惑与解答](#本次困惑与解答)
- [语言差别与常用接口](#语言差别与常用接口)
- [复杂度与边界](#复杂度与边界)
- [补充讲解](#补充讲解)
- [实际验证](#实际验证)
- [复习自测](#复习自测)

## 题意与例子

在字符串中找一段**连续、内部没有重复字符**的片段，返回其最大长度，而不是返回片段本身。空字符串返回 0；原字符串不需要修改。

| 输入 | 返回 | 理解 |
| --- | ---: | --- |
| `abcabcbb` | 3 | `abc`、`bca`、`cab` 都是长度为 3 的合法片段 |
| `bbbbb` | 1 | 任意两个相邻字符都重复，只能取一个 `b` |
| `pwwkew` | 3 | 可以取 `wke`；`pwke` 跳过了字符，不是连续子串 |
| 空字符串 | 0 | 没有字符可选 |

本题长度范围是 0～50000，字符包含英文字母、数字、符号和空格。空格也要参与判重，`A` 与 `a` 是不同字符。

## 从朴素思路到主要解法

### 先枚举每一个起点

固定起点，从它向右逐个加入字符；用一个集合记录是否重复。一旦重复，继续向右也无法修复这段已有的重复，可以换下一个起点。所有起点都试过后，取最大长度。

这个方法容易理解，但同一段内容会从不同起点重复扫描。平均常数时间的集合操作下，最坏需要 O(n²) 次扫描。若枚举每个子串后再从头检查，朴素实现甚至会达到 O(n³)。

### 复用已经检查过的窗口

使用 `left` 和 `right` 表示连续区间。右边遇到新字符时，复用当前集合；如果冲突，就从左端逐个移出，直到旧的同字符离开窗口，再加入新字符。

这样两个边界都只向右移动，不重新从头扫描。主分类选**滑动窗口**：解法一直维护一个满足条件的连续区间；双指针是位置表示，哈希集合是辅助查询工具。

```text
右边读到一个候选字符
        ↓
它已经在当前窗口的集合里吗？
  是 → 删除左端对应字符，left 加 1，继续检查
  否 → 加入候选字符，记录当前长度，扫描下一个位置
```

“读到”表示准备处理，不代表已经执行集合的插入。下面三份源码统一采用**先解除冲突、再插入新字符**的顺序。

## 关键变量与执行顺序

| 变量 | 表示什么 | 容易混淆的地方 |
| --- | --- | --- |
| `s` | 原字符串 | 不需要真的删除其中的字符 |
| `right` | 正准备加入的字符下标 | 从 0 开始，每轮前进一步 |
| `left` | 当前窗口的左边界 | 遇到冲突时可能连续前进多步 |
| `seen` | 当前窗口中已有的字符集合 | 不是整个字符串的字符，也不是历史上出现过的全部字符 |
| `ans` | 到目前为止，合法窗口的最大长度 | 不是当前窗口长度，不随窗口缩短而缩小 |

每轮严格执行：

1. 查 `s[right]` 是否已经在 `seen` 中。
2. 如果在，删除 `s[left]`，然后让 `left` 加 1；继续检查同一个候选字符。
3. 冲突消失后，把 `s[right]` 放入集合。
4. 用 `right - left + 1` 更新最大值。

删除和移动要配对：**删谁，谁就离开窗口。** 所以先删除旧左端字符，再修改 `left`。本题右边界用普通整数下标表示，不涉及 C++ 指针类型。

## 逐步推演

### 一次完整扫描

字符串为 `abcabcbb`，初始 `left = 0`、`ans = 0`、`seen` 为空。下表的窗口和答案均为本轮插入新字符之后的状态：

| right | 新字符 | while 依次移出的字符 | 最终 left | 当前窗口 | ans |
| ---: | --- | --- | ---: | --- | ---: |
| 0 | a | 无 | 0 | a | 1 |
| 1 | b | 无 | 0 | ab | 2 |
| 2 | c | 无 | 0 | abc | 3 |
| 3 | a | 下标 0 的 a | 1 | bca | 3 |
| 4 | b | 下标 1 的 b | 2 | cab | 3 |
| 5 | c | 下标 2 的 c | 3 | abc | 3 |
| 6 | b | 下标 3 的 a、下标 4 的 b | 5 | cb | 3 |
| 7 | b | 下标 5 的 c、下标 6 的 b | 7 | b | 3 |

最后窗口只有一个字符，但最终答案仍是 3。`ans` 已保存此前的最佳结果。

### 为什么中间重复也要移动

重点看 `right = 6`，候选字符为 `b`：

```text
下标：3 4 5 6
字符：a b c b
      ↑     ↑
     left  right
```

先看候选区间 `abcb`，重复的两个 `b` 不在左端。可是区间仍然不合法，不能当作答案。

按源码的集合顺序：

| 操作 | 集合内容 | 候选 b 是否仍在集合里 |
| --- | --- | --- |
| 新 b 尚未插入 | a、b、c | 是 |
| 删除左端 a，left 从 3 到 4 | b、c | 是，继续循环 |
| 删除旧 b，left 从 4 到 5 | c | 否，循环结束 |
| 插入新 b | c、b | 窗口成为下标 5～6 的 `cb` |

集合展示的顺序只是为了读起来方便，算法不依赖集合迭代顺序。不能只抠掉中间的旧 `b`，保留 `acb`：那样跳过了一个位置，不再是连续子串。

## 为什么正确

用一个不变量描述每轮开始时的状态：**`seen` 恰好保存区间 `[left, right)` 的字符，并且这个区间没有重复。** 右端不包含 `right`，因为新字符还没有插入。

初始区间为空，不变量成立。新字符若不在集合中，直接加入也不会重复。若已经在集合中，由于旧窗口无重复，其中恰好有一个旧的同字符；不断移走左端字符，最终一定会把它移出去，然后才能加入新字符。

为什么不漏掉更长答案？比当前左边界更早的起点，要么此前已经因重复而失效，要么仍会包含新旧两个相同字符。追加新字符不会消除旧区间里的重复，因此这些起点不可能构成当前右端对应的更长合法子串。解除冲突后得到的就是**以当前 right 结尾的最长合法窗口**。

每个非空子串都有一个右端。遍历全部右端并维护最大长度，就覆盖了全局最优答案。空串没有循环，初值 0 正好是答案。

## 三种语言源码

三种实现采用同一个集合滑动窗口流程，没有排序，也不修改原字符串。完整代码块由实际源文件生成，测试会检查一致性。

### C++

[完整源码](cpp/solution.cpp)。C++17，头文件分别提供最大值函数、字符串和哈希集合。

```cpp
#include <algorithm>
#include <string>
#include <unordered_set>

class Solution {
public:
    int lengthOfLongestSubstring(std::string s) {
        std::unordered_set<char> seen;  // 只记录当前窗口内的字符
        int left = 0;
        int ans = 0;  // 历史最大长度，不随窗口缩短而减小
        const int n = static_cast<int>(s.size());

        for (int right = 0; right < n; ++right) {
            // 新字符尚未加入；先移出左端字符，直到不再冲突。
            while (seen.count(s[right]) > 0) {
                seen.erase(s[left]);
                ++left;
            }
            seen.insert(s[right]);
            ans = std::max(ans, right - left + 1);
        }
        return ans;
    }
};
```

### Java

[完整源码](java/Solution.java)。兼容 Java 8，`Set` 是接口，`HashSet` 是实现，泛型元素使用 `Character`。

```java
import java.util.HashSet;
import java.util.Set;

class Solution {
    public int lengthOfLongestSubstring(String s) {
        Set<Character> seen = new HashSet<>();
        int left = 0;
        int ans = 0;  // 单独保存历史最大长度

        for (int right = 0; right < s.length(); right++) {
            // String 通过 charAt 取字符；冲突可能需要多次移动才能解除。
            while (seen.contains(s.charAt(right))) {
                seen.remove(s.charAt(left));
                left++;
            }
            seen.add(s.charAt(right));
            ans = Math.max(ans, right - left + 1);
        }
        return ans;
    }
}
```

### Python 3

[完整源码](python/solution.py)。`set()` 创建空集合，`in` 检查成员，冒号后的缩进表示代码块。

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()  # 当前窗口中的字符，不保存重复元素
        left = 0
        ans = 0  # 已找到的最大长度

        for right in range(len(s)):
            # 先解决新字符与窗口的冲突，再将它加入集合。
            while s[right] in seen:
                seen.remove(s[left])
                left += 1

            seen.add(s[right])
            ans = max(ans, right - left + 1)

        return ans
```

## 本次困惑与解答

以下只记录本次对话中真实出现的理解障碍、提问和截图代码。额外知识放在[补充讲解](#补充讲解)，没有把它写成已经提出过的问题。

### 遍历是等到下一个字符为空才结束吗

最初把结束理解为右边界的下一个位置为空。实际字符串有明确长度：有效下标是 0 到 n−1，处理完最后一个字符即可结束，不靠读取一个额外的空字符判断。

Java/Python 访问越界会抛异常，C++ 也不能靠越界读取寻找结束。这里统一使用 `right < n`、`right < s.length()` 或 `range(len(s))`。单独遇到重复只是缩小窗口，并不是结束整个遍历。

### 只有新字符与左边界相同才能移动吗

当时的想法是：新字符和中间字符重复时不能移动左边界。问题在于，题目要求的是**窗口整体没有重复**，而不是首尾不同。

例如 `abc` 后面来一个 `b`，`abcb` 的重复发生在中间，也必须处理。连续区间只能从左端缩小，因此先移出 a，再移出旧 b，才能保留 `cb`。这也是 `while` 比只移动一次的 `if` 更合适的原因。

### 窗口变短以后之前的长度不就丢了吗

这一点在无法理解移动规则时，通过区分“当前尝试”和“历史答案”说明。它是对当时理解障碍的拆解，不是一次额外的原话提问。

```text
当前窗口：abc → 候选 abcb → 候选 bcb → 合法 cb
历史最大： 3          3           3          3
```

`ans = max(ans, 当前长度)` 只会保留或增大答案。缩小当前尝试，是为了继续处理后面的字符。

### Python的seen等于set是什么写法

`seen = set()` 分为赋值与构造：`set()` 调用内置集合类型创建空集合，`seen` 是自己起的变量名。重复添加同一元素，不会增加第二份。

```python
seen = set()
seen.add("a")
seen.add("a")
print(len(seen))     # 1
print("a" in seen)  # True
```

`{}` 是空字典，不是空集合。在本题中 `seen` 只存当前窗口的字符，删除旧字符后也要同步更新它。通用定义和返回值见[集合与成员判断](../../../docs/language-cheatsheet.md#集合与成员判断)。

### C++字符串怎样添加删除和查看长度

本次询问了字符串的增删和长度。常用操作为：

```cpp
std::string s = "abc";
s.push_back('d');       // abcd：尾部添加一个字符
s += "ef";             // abcdef：追加字符串
if (!s.empty()) {
    s.pop_back();      // abcde：删除尾部一个字符
}
s.erase(0, 1);         // bcde：从下标 0 开始删除 1 个字符
int n = static_cast<int>(s.size());  // 4；length() 也能读长度
```

但本题不需要删除原字符串；移动 `left` 就能表示字符离开窗口。字符串的 `erase(位置, 数量)` 与集合的 `erase(元素)` 属于不同类，参数含义不同。见[字符串与窗口长度](../../../docs/language-cheatsheet.md#字符串与窗口长度)。

### 怎样判断右端字符在集合里以及count返回什么

`s[right]` 取得当前候选字符，`seen.count(s[right]) > 0` 判断它是否已在集合中。

```cpp
std::unordered_set<char> seen = {'a', 'b'};
seen.count('a');  // 1，存在
seen.count('c');  // 0，不存在
```

这里讨论的是 `unordered_set`，它的元素唯一，计数只会是 0 或 1；不是询问这个字符在原字符串里共出现多少次，也不是返回下标。正式返回类型是容器的 `size_type`。完整接口对照见[集合与成员判断](../../../docs/language-cheatsheet.md#集合与成员判断)。

### C++删除了right字符却只让left前进

截图中曾写成：

```cpp
while (seen.count(s[right]) > 0) {
    seen.erase(s[right]);  // 错误：删除了候选字符的值
    left++;
}
```

这样只是在集合中抹去了某个值，实际窗口左端却是另一个字符，集合与窗口不再对应。应改为 `seen.erase(s[left]);`，然后再执行 `left++`。

例如单独保留这处错误、其余逻辑正确时，`abcbde` 会误得到 5，正确答案是 4。到新 b 时，错误做法删掉集合里的 b，却把左端 a 移出；随后集合保留了已经离开的 a，也无法表示实际区间里的两个 b，后面就会把不合法区间当作答案。

### C++长度公式减了1以及旧提交从1开始

截图中曾写 `right - left - 1`，应改为 `right - left + 1`。闭区间要包含左右两个端点：下标 0～2 共三个字符，长度为 2−0+1。

同一张截图左侧的旧提交还使用 `right = 1`，会漏掉第一个字符；右侧当时已改成 0。单字符输入 `a` 就能暴露从 1 开始的问题：循环不执行，会返回 0，而答案应为 1。

这些是独立问题，不能仅凭修正其中一处就判断整份代码正确。

### Java集合如何定义

```java
Set<Character> seen = new HashSet<>();
```

`Set` 是不重复元素集合的接口，`HashSet` 提供具体实现；`new` 创建对象，`<>` 让编译器推断泛型参数。Java 泛型使用引用类型，所以写包装类 `Character`，不是基本类型 `char`。完整源码补齐了 `java.util.Set` 和 `java.util.HashSet` 的导入。

添加、删除、查询分别是 `add`、`remove`、`contains`。`contains` 直接返回 boolean，不需要像 C++ 的 `count` 一样与 0 比较。

### Java为什么报找不到length和需要数组

当时的代码是：

```java
for (int right = 0; right < s.length; right++) {
    while (seen.contains(s[right])) {
        seen.remove(s[left]);
        left++;
    }
    seen.add(s[right]);
}
```

截图报错包括 `cannot find symbol: variable length` 和 `array required, but String found`。因为 `s` 的类型是 String：长度通过方法 `s.length()` 取得，字符通过 `s.charAt(i)` 取得。方括号是数组访问写法，不能直接用在 Java String 上。

```java
s.length();        // 字符串长度
s.charAt(right);   // 右端字符
s.charAt(left);    // 左端字符
```

Java 数组使用 `arr.length`，Java 字符串使用 `s.length()`，集合使用 `seen.size()`。它们的对象类型与接口不同，不能混用。

### Java为什么Max和Max点max都找不到

两次截图中先出现了 `Max(ans, right - left + 1)`，之后写成了 `Max.max(ans, right - left + 1)`。第二次报错明确指向找不到变量 `Max`。

```java
ans = Math.max(ans, right - left + 1);
```

`Math` 是 `java.lang` 包中的数学工具类，`max` 是其中的静态方法；`Math` 的 M 大写，`max` 的 m 小写，名称都是固定拼写。这个类默认可用，不需要额外 import。见[最值函数与导入](../../../docs/language-cheatsheet.md#最值函数与导入)。

## 语言差别与常用接口

| 目的 | C++17 | Java 8 | Python 3 |
| --- | --- | --- | --- |
| 创建字符集合 | `std::unordered_set<char> seen;` | `Set<Character> seen = new HashSet<>();` | `seen = set()` |
| 取得字符 | `s[right]` | `s.charAt(right)` | `s[right]` |
| 字符串长度 | `s.size()` 或 `s.length()` | `s.length()` | `len(s)` |
| 判断成员 | `seen.count(c) > 0` | `seen.contains(c)` | `c in seen` |
| 添加 | `seen.insert(c)` | `seen.add(c)` | `seen.add(c)` |
| 删除 | `seen.erase(c)` | `seen.remove(c)` | `seen.remove(c)` |
| 按下标遍历 | `for (int right = 0; right < n; ++right)` | `for (int right = 0; right < s.length(); right++)` | `for right in range(len(s)):` |
| 重复处理条件 | `while (条件) { ... }` | 同 C++ | `while 条件:` 后缩进 |
| 最大值 | `std::max(a, b)` | `Math.max(a, b)` | `max(a, b)` |
| 返回类型 | `int` | `int` | `-> int` 是类型注解，实际 `return ans` |

传参区别：C++ 这份接口的 `std::string s` 按值传入，通常会复制传来的左值字符串；Java 传递 String 引用的值；Python 把参数名绑定到传入的字符串对象。Java/Python 字符串不可变，三份代码都只读取它们。具体空间区别见下一节。

补充讲解：本题不能靠排序后去重求答案，因为排序会改变原来的相邻关系。一般排序接口及“修改输入还是产生新结果”的区别见[排序与二维结果](../../../docs/language-cheatsheet.md#排序与二维结果)；不能把其他题的排序模板直接搬来。

接口的所属类、参数、返回值详见[集合与成员判断](../../../docs/language-cheatsheet.md#集合与成员判断)、[字符串与窗口长度](../../../docs/language-cheatsheet.md#字符串与窗口长度)。例如 Java 的 `contains(待查元素)` 返回真假，`add(待加元素)` 返回集合是否新增了元素；C++ 按键 `erase(待删元素)` 返回实际删除数量；Python `set.add` 和 `set.remove` 执行后返回 None。本题不依赖添加或删除的返回值。

## 复杂度与边界

令 n 为输入长度，Σ 为可能出现的字符种类数，k = min(n, Σ)。在集合操作平均 O(1) 的前提下，时间为 **O(n)**：右边界走 n 次，左边界在全部 while 循环中总共最多走 n 次。两个循环嵌套不等于自动变成 O(n²)。哈希退化时不能保证每次操作都为常数时间，O(n) 是这里的平均复杂度结论。

窗口算法的辅助空间为 **O(k)**，用于保存当前字符集合；几个整数是 O(1)，返回的一个长度也是 O(1)，没有创建输出子串。三种源码都不会每轮切片复制窗口。

需要单独计算 C++ 按值形参：保留 `std::string s` 接口时，若调用方传入一个左值字符串，通常另有 O(n) 的复制时间和空间，因此这份 C++ 调用的额外峰值空间可达 O(n + k)。Java/Python 这里不复制整个输入字符串。受控的 C++ 本地接口可以使用 `const std::string&` 避免该复制；本文保留常见提交接口并明确成本。

| 输入 | 预期长度 | 检查点 |
| --- | ---: | --- |
| 空字符串 | 0 | 循环不进入 |
| `a` | 1 | 扫描必须从 0 开始，长度公式必须加 1 |
| `bbbbb` | 1 | 连续相同字符 |
| `abcabcbb` | 3 | 当前窗口缩短但历史答案不变 |
| `abcbde` | 4 | 重复在中间，不能只移动一次或删除 right |
| `abba` | 2 | 中间连续重复，之后又遇到较早字符 |
| `dvdf` | 3 | 不能遇到重复就清空所有已收集内容 |
| `Aa` | 2 | 大小写不同 |
| 一个空格 | 1 | 空格不是“没有字符” |
| `a a` | 2 | 空格与字符共同参与判重 |

## 补充讲解

以下不是本次实际提问：

- 集合只回答“某字符是否存在”，并不记录它出现在哪个下标；区间连续性由 left/right 维护，不靠集合的排列。
- `unordered_set`、`HashSet`、`set` 都是这里的哈希集合选型。不要将 C++ 的 `std::set` 与 Python 的 `set` 当作同一实现；前者是有序集合，查询为 O(log k)。
- 若想一次跳过旧字符，可以维护字符到最近下标的映射，但必须防止左边界后退。先掌握本篇逐个移出的版本，再学习这种优化；它不是本次提交源码。
- 通用 Unicode 文本需要重新约定“字符”：C++ string 常按字节索引，Java charAt 返回 UTF-16 代码单元，Python str 按 Unicode 码点索引。本题限定范围内三种实现一致，本次跨语言测试使用 ASCII 范围；没有声称验证任意 Unicode 字符或字形簇。

## 实际验证

2026-10-18 本地实测：Python 3.11.7、Java 8u481、GCC/G++ 13.1.0。实际调用三份源码，各通过 **3604 组**用例；Java 完成编译和运行，C++17 使用 `-Wall -Wextra -Werror -pedantic` 编译并运行。统一执行 `python tests/verify.py --require-all`，通过参数指定可用的 GCC/G++ 路径，没有语言跳过项；原有四道题的回归检查也全部通过。链接、内部锚点和完整代码块与源文件的一致性检查通过。

测试入口：[substring_check.py](../../../tests/substring_check.py)，由 [verify.py](../../../tests/verify.py) 统一运行；测试只生成调用入口，算法来自上面的真实源文件。小字符串与独立枚举所有子串、检查唯一性的参考实现对照。长度 50000 的大输入使用可直接推导的预期值，不调用高复杂度参考。

本题每种语言使用 3604 组用例：20 组固定样例、字符集 abc 上长度 0～7 的全部 3280 种字符串、300 组固定随机种子的大小写/数字/空格/符号样本、4 组长度 50000 的输入。测试传输用字符编码保存字符串，避免把空串或空格错误地读丢。

本次对话没有提供最终力扣通过截图，以上是本地源码验证，不等于力扣 AC 记录，也不是性能排名。

## 复习自测

1. 子串为什么必须连续？`pwwkew` 为什么不能取 `pwke`？
2. 对窗口 abc 和候选 b，为什么要依次移出 a、旧 b？能否只比较首尾？
3. `seen`、`left`、`right`、`ans` 分别负责什么？窗口缩短为什么不丢答案？
4. 为什么删除的是 `s[left]`，并且先删除再移动 left？为什么用 while？
5. 不看源码，分别写出三种语言的集合定义、成员判断和取字符方式。
6. `s.length`、`s.length()`、`s.size()`、`len(s)`、`Math.max()` 分别属于哪种类型或语言？
