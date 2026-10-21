# daily-algorithm-learning · 力扣刷题与复习

按算法分类整理题解，记录从“写不出来”到理解代码的过程。主要使用 **C++、Java、Python 3**；两数之和另保留 C 语言专题。

## 分类导航

- [哈希表](#哈希表)
- [双指针](#双指针)
- [滑动窗口](#滑动窗口)
- [前缀和](#前缀和)
- [语言与基础知识](#语言与基础知识)
- [归纳与上传提示词](PROMPTS.md)
- [如何使用与维护](#如何使用与维护)

目前已整理 **7 道题 · 4 个类别**。每个类别在下面单独列出，点击题名进入题解。

---

## 哈希表

记录出现过的值、次数或位置，用快速查询减少重复遍历。本类收录 **1 道题**。

| 状态 | 题目 | 难度 |
| --- | --- | --- |
| ✅ 已整理 | [1. 两数之和](problems/hash-table/0001-two-sum/README.md) | 🟢 简单 |

源码：[C++](problems/hash-table/0001-two-sum/cpp/hash.cpp) · [Java](problems/hash-table/0001-two-sum/java/hash/Solution.java) · [Python](problems/hash-table/0001-two-sum/python/hash.py) · [C](problems/hash-table/0001-two-sum/c/hash.c)

[查看哈希表分类](categories/README.md#哈希表)

---

## 双指针

用两个位置协同处理：盛最多水的容器和三数之和使用左右指针；移动零使用快慢指针同向扫描与整理。本类收录 **3 道题**。

| 状态 | 题目 | 难度 |
| --- | --- | --- |
| ✅ 已整理 | [11. 盛最多水的容器](problems/two-pointers/0011-container-with-most-water/README.md) | 🟠 中等 |
| ✅ 已整理 | [15. 三数之和](problems/two-pointers/0015-3sum/README.md) | 🟠 中等 |
| ✅ 已整理 | [283. 移动零](problems/two-pointers/0283-move-zeroes/README.md) | 🟢 简单 |

- 盛最多水的容器源码：[C++](problems/two-pointers/0011-container-with-most-water/cpp/solution.cpp) · [Java](problems/two-pointers/0011-container-with-most-water/java/Solution.java) · [Python](problems/two-pointers/0011-container-with-most-water/python/solution.py)
- 三数之和源码：[C++](problems/two-pointers/0015-3sum/cpp/solution.cpp) · [Java](problems/two-pointers/0015-3sum/java/Solution.java) · [Python](problems/two-pointers/0015-3sum/python/solution.py)
- 移动零源码：[C++](problems/two-pointers/0283-move-zeroes/cpp/solution.cpp) · [Java](problems/two-pointers/0283-move-zeroes/java/Solution.java) · [Python](problems/two-pointers/0283-move-zeroes/python/solution.py)

[查看双指针分类](categories/README.md#双指针)

---

## 滑动窗口

维护连续区间并复用信息：无重复字符题维护可变长度窗口，字母异位词题维护固定长度窗口与计数。本类收录 **2 道题**。

| 状态 | 题目 | 难度 |
| --- | --- | --- |
| ✅ 已整理 | [3. 无重复字符的最长子串](problems/sliding-window/0003-longest-substring-without-repeating-characters/README.md) | 🟠 中等 |
| ✅ 已整理 | [438. 找到字符串中所有字母异位词](problems/sliding-window/0438-find-all-anagrams-in-a-string/README.md) | 🟠 中等 |

- 无重复字符的最长子串源码：[C++](problems/sliding-window/0003-longest-substring-without-repeating-characters/cpp/solution.cpp) · [Java](problems/sliding-window/0003-longest-substring-without-repeating-characters/java/Solution.java) · [Python 3](problems/sliding-window/0003-longest-substring-without-repeating-characters/python/solution.py)
- 找到字符串中所有字母异位词源码：[C++](problems/sliding-window/0438-find-all-anagrams-in-a-string/cpp/solution.cpp) · [Java](problems/sliding-window/0438-find-all-anagrams-in-a-string/java/Solution.java) · [Python 3](problems/sliding-window/0438-find-all-anagrams-in-a-string/python/solution.py)

[查看滑动窗口分类](categories/README.md#滑动窗口) · [固定与可变窗口入门](docs/sliding-window.md)

---

## 前缀和

用两个前缀和之差表示连续区间的和；结合哈希表频次统计满足条件的子数组。本类收录 **1 道题**。

| 状态 | 题目 | 难度 |
| --- | --- | --- |
| ✅ 已整理 | [560. 和为 K 的子数组](problems/prefix-sum/0560-subarray-sum-equals-k/README.md) | 🟠 中等 |

源码：[C++](problems/prefix-sum/0560-subarray-sum-equals-k/cpp/solution.cpp) · [Java](problems/prefix-sum/0560-subarray-sum-equals-k/java/Solution.java) · [Python 3](problems/prefix-sum/0560-subarray-sum-equals-k/python/solution.py)

[查看前缀和分类](categories/README.md#前缀和) · [前缀和入门](docs/prefix-sum.md)

---

其他分类的适用场景见[分类指南](categories/README.md)。新增题目时放进对应类别；新类别另开区块。

## 语言与基础知识

- [三种语言语法与常用接口对照](docs/language-cheatsheet.md)：循环、字符串、集合、哈希表、最值函数、返回值、传参。
- [前缀和入门](docs/prefix-sum.md)：连续区间、频次计数、空前缀与先查后存。
- [滑动窗口入门](docs/sliding-window.md)：可变与固定长度窗口、历史答案、边界与计数同步。
- [双指针入门](docs/two-pointers.md)：快慢指针与左右指针的区别。
- [C 语言与哈希表学习补充](docs/c-and-hashing.md)：返回数组、内存、取模、冲突与线性探测。

## 如何使用与维护

常用入口：[归纳与上传提示词](PROMPTS.md) · [长期维护规则](AGENTS.md) · [题解模板](templates/problem.md)。提示词页面包含日常简短指令、完整版和换新聊天的使用说明。

建议先读题解中的手动推演，再看一种熟悉的语言，最后对照另外两种语言。源码使用力扣的 Solution 接口，可复制到对应语言编辑器；本地运行需要测试入口。

仓库结构：

```text
categories/README.md                  分类指南
problems/<算法分类>/<四位题号-英文名>/
    README.md                         题解、困惑、推演、复习问题
    cpp/                              C++ 源码
    java/                             Java 源码
    python/                           Python 3 源码
    c/                                可选的 C 语言补充
docs/                                 跨题通用知识
templates/problem.md                  新题模板
tests/verify.py                       源码与文档检查
AGENTS.md                             后续归纳与维护约定
PROMPTS.md                            可复制的归纳与上传提示词
```

每次新增题解同时更新首页和分类目录。个人困惑只记录实际出现过的问题，补充讲解单独标明，方便其他学习者阅读。详细规则见 [AGENTS.md](AGENTS.md)。

验证全部源码（Python 3、JDK、GCC、G++）：

```bash
python tests/verify.py --require-all
```

没有 C/C++ 编译器时可运行 `python tests/verify.py`，报告会明确列出跳过项。各题解的代码块与源码由同一内容整理，测试还会检查二者一致。这里的验证是本地测试，不代表已提交力扣判题。
