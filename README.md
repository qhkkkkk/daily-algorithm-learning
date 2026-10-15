# daily-algorithm-learning · 力扣刷题与复习

按算法分类整理题解，记录从“写不出来”到理解代码的过程。主要使用 **C++、Java、Python 3**；两数之和另保留 C 语言专题。

## 目录

- [按算法分类](#按算法分类)
- [全部题目](#全部题目)
- [语言与基础知识](#语言与基础知识)
- [如何使用与维护](#如何使用与维护)

## 按算法分类

每道题只设一个主目录，其他知识点以标签记录，避免同一篇题解复制多份。

| 分类 | 已整理题数 | 题目 |
| --- | ---: | --- |
| [哈希表](categories/README.md#哈希表) | 1 | [0001 两数之和](problems/hash-table/0001-two-sum/README.md) |
| [双指针](categories/README.md#双指针) | 1 | [0283 移动零](problems/two-pointers/0283-move-zeroes/README.md) |

其他分类的适用场景见[分类指南](categories/README.md)。只在收录题目时建立对应源码目录。

## 全部题目

| 题号 | 题目 | 难度 | 主分类 | 其他标签 | 解法与复杂度 | 源码 |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | [两数之和](problems/hash-table/0001-two-sum/README.md) | 简单 | 哈希表 | 数组、枚举、空间换时间 | 暴力 O(n²)；哈希平均 O(n) | [C++](problems/hash-table/0001-two-sum/cpp/hash.cpp) · [Java](problems/hash-table/0001-two-sum/java/hash/Solution.java) · [Python](problems/hash-table/0001-two-sum/python/hash.py) · [C](problems/hash-table/0001-two-sum/c/hash.c) |
| 283 | [移动零](problems/two-pointers/0283-move-zeroes/README.md) | 简单 | 双指针 | 数组、快慢指针、原地修改 | O(n) 时间，O(1) 额外空间 | [C++](problems/two-pointers/0283-move-zeroes/cpp/solution.cpp) · [Java](problems/two-pointers/0283-move-zeroes/java/Solution.java) · [Python](problems/two-pointers/0283-move-zeroes/python/solution.py) |

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
