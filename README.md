# daily-algorithm-learning · 力扣刷题与复习

按算法分类整理题解，记录从“写不出来”到理解代码的过程。主要使用 **C++、Java、Python 3**；两数之和另保留 C 语言专题。

## 分类导航

- [哈希表](#哈希表)
- [双指针](#双指针)
- [语言与基础知识](#语言与基础知识)
- [如何使用与维护](#如何使用与维护)

目前已整理 **2 道题 · 2 个类别**。每个类别在下面单独列出，点击题名进入题解。

---

## 哈希表

记录出现过的值、次数或位置，用快速查询减少重复遍历。

| 状态 | 题目 | 难度 |
| --- | --- | --- |
| ✅ 已整理 | [1. 两数之和](problems/hash-table/0001-two-sum/README.md) | 🟢 简单 |

源码：[C++](problems/hash-table/0001-two-sum/cpp/hash.cpp) · [Java](problems/hash-table/0001-two-sum/java/hash/Solution.java) · [Python](problems/hash-table/0001-two-sum/python/hash.py) · [C](problems/hash-table/0001-two-sum/c/hash.c)

[查看哈希表分类](categories/README.md#哈希表)

---

## 双指针

用两个位置协同扫描；移动零使用快慢指针，一个找非零，一个记录放置位置。

| 状态 | 题目 | 难度 |
| --- | --- | --- |
| ✅ 已整理 | [283. 移动零](problems/two-pointers/0283-move-zeroes/README.md) | 🟢 简单 |

源码：[C++](problems/two-pointers/0283-move-zeroes/cpp/solution.cpp) · [Java](problems/two-pointers/0283-move-zeroes/java/Solution.java) · [Python](problems/two-pointers/0283-move-zeroes/python/solution.py)

[查看双指针分类](categories/README.md#双指针)

---

其他分类的适用场景见[分类指南](categories/README.md)。新增题目时放进对应类别；新类别另开区块。

## 语言与基础知识

- [三种语言语法与常用接口对照](docs/language-cheatsheet.md)：循环、数组、交换、哈希表、返回值、传参。
- [双指针入门](docs/two-pointers.md)：快慢指针与左右指针的区别。
- [C 语言与哈希表学习补充](docs/c-and-hashing.md)：返回数组、内存、取模、冲突与线性探测。

## 如何使用与维护

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
```

每次新增题解同时更新首页和分类目录。个人困惑只记录实际出现过的问题，补充讲解单独标明，方便其他学习者阅读。详细规则见 [AGENTS.md](AGENTS.md)。

验证全部源码（Python 3、JDK、GCC、G++）：

```bash
python tests/verify.py --require-all
```

没有 C/C++ 编译器时可运行 `python tests/verify.py`，报告会明确列出跳过项。各题解的代码块与源码由同一内容整理，测试还会检查二者一致。这里的验证是本地测试，不代表已提交力扣判题。
