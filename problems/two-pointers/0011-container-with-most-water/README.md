# LeetCode 11 · 盛最多水的容器

[返回首页](../../../README.md) · [双指针分类](../../../categories/README.md#双指针) · [力扣原题](https://leetcode.cn/problems/container-with-most-water/)

| 难度 | 主分类 | 标签 | 语言 |
| --- | --- | --- | --- |
| 中等 | 双指针 | 数组、左右指针、面积、贪心排除 | C++ / Java / Python 3 |

## 目录

- [题意与例子](#题意与例子)
- [从朴素思路到左右指针](#从朴素思路到左右指针)
- [逐步推演](#逐步推演)
- [为什么移动短边才正确](#为什么移动短边才正确)
- [三种语言源码](#三种语言源码)
- [本次困惑与解答](#本次困惑与解答)
- [语言差别与常用接口](#语言差别与常用接口)
- [复杂度与边界](#复杂度与边界)
- [复习自测](#复习自测)

## 题意与例子

数组 height 中，每个下标对应一条竖线的位置，元素值是该线的高度。选择两条不同的线作为容器两壁，返回能盛水的最大面积。这里只计算结果，不需要修改输入数组。

面积由两个因素共同决定：

```text
可盛水的高度 = min(height[left], height[right])
宽度         = right - left
面积         = 较矮的高度 × 宽度
```

两条线之间的距离由下标差决定，不是包含了几个数组元素。因此宽度不用加 1。

例子：

```text
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
下标   =  0  1  2  3  4  5  6  7  8
答案   = 49
```

### 为什么不选两个8

这是本次练习开始时的困惑。两个 8 可以选，只是面积小于 49：

| 选取的高度 | 两个下标 | 水位高度 | 宽度 | 面积 |
| --- | --- | ---: | ---: | ---: |
| 8 和 8 | 1、6 | 8 | 6 − 1 = 5 | 40 |
| 8 和 7 | 1、8 | 7 | 8 − 1 = 7 | **49** |

不能只看哪两条线更高；矮一点但距离更远，也可能装得更多。

补充讲解：本题把选中的两条线和 x 轴视作容器，中间的线不需要逐根扣除“占用面积”。它与“接雨水”逐位置计算积水的题意不同。

## 从朴素思路到左右指针

最容易想到的是枚举所有下标对：

```text
对每个 left：
    对每个 right > left：
        计算面积
        更新最大面积
```

共有 n(n−1)/2 对，时间 O(n²)。如果每次比较后能排除一整批不可能改善答案的组合，就能减少重复枚举。

左右指针的做法：

1. left = 0，right = n−1，从最宽的容器开始。
2. 计算当前面积，更新 ans。
3. 移动较矮的一侧：左边矮就 left += 1，否则 right -= 1。
4. 当 left 与 right 相遇，结束，返回 ans。

变量分工：

| 变量 | 含义 |
| --- | --- |
| left | 当前左壁的下标 |
| right | 当前右壁的下标 |
| area | 当前这一对线围出的面积 |
| ans | 到目前为止检查到的最大面积 |

这也是双指针，但与[移动零](../0283-move-zeroes/README.md)的快慢指针不同：本题两端向中间靠拢，移动零是两个位置同向扫描与整理。

## 逐步推演

对示例数组，按“左边严格更矮就动左边，否则动右边”的代码：

| left | right | 左高 | 右高 | 宽度 | area | ans | 接下来的移动 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 8 | 1 | 7 | 8 | 8 | 8 | left -> 1 |
| 1 | 8 | 8 | 7 | 7 | 49 | 49 | right -> 7 |
| 1 | 7 | 8 | 3 | 6 | 18 | 49 | right -> 6 |
| 1 | 6 | 8 | 8 | 5 | 40 | 49 | right -> 5 |
| 1 | 5 | 8 | 4 | 4 | 16 | 49 | right -> 4 |
| 1 | 4 | 8 | 5 | 3 | 15 | 49 | right -> 3 |
| 1 | 3 | 8 | 2 | 2 | 4 | 49 | right -> 2 |
| 1 | 2 | 8 | 6 | 1 | 6 | 49 | right -> 1 |

left == right 时结束。area 可以变小，但 ans 一直保存已经出现过的最大值。

## 为什么移动短边才正确

假设左边不高于右边：

```text
height[left] <= height[right]
当前面积 = height[left] × (right - left)
```

如果保留这个左端点，把右端点换成区间内部任意 j：

```text
新面积 = min(height[left], height[j]) × (j - left)
      <= height[left] × (j - left)
      <= height[left] × (right - left)
```

因为宽度缩小，而且可用高度不会超过仍保留的左边，所以新面积不会超过刚刚记录的面积。

因此，所有“保留这个左端点、右端点继续向内找”的组合，都不用再查了，可以安全排除当前左端点，执行 left += 1。

右边较矮时同理，执行 right -= 1。每次排除的一批组合都不会优于已经记录的答案，所以不会漏掉最大值。

两边等高时，按同样理由排除任意一侧都安全。本代码统一移动右侧。移动短边只是带来改善的机会，不保证下一步面积一定增大，因此必须持续维护 ans。

## 三种语言源码

### Python 3

[源码](python/solution.py)。先初始化、循环计算、更新答案，再移动短边；return 要放在循环外。

```python
class Solution:
    def maxArea(self, height):
        left = 0
        right = len(height) - 1  # 长度减一，才是最后一个合法下标
        ans = 0

        while left < right:
            area = min(height[left], height[right]) * (right - left)
            ans = max(ans, area)

            # 换掉较矮的一侧，才有机会提高限制水位的高度
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1  # 右边向左走，不能写 += 1

        return ans
```

### C++

[源码](cpp/solution.cpp)。显式包含头文件并写 std::，便于在本地编译，不依赖评测平台的额外设置。

```cpp
#include <algorithm>
#include <vector>

class Solution {
public:
    int maxArea(std::vector<int>& height) {
        int left = 0;
        int right = static_cast<int>(height.size()) - 1;
        int ans = 0;

        while (left < right) {
            int area = std::min(height[left], height[right]) * (right - left);
            ans = std::max(ans, area);

            // 保留短边、只移动长边，不可能让面积超过当前值
            if (height[left] < height[right]) {
                ++left;
            } else {
                --right;
            }
        }
        return ans;
    }
};
```

### Java

[源码](java/Solution.java)。使用数组的 length 属性与 Math 类的静态方法。

```java
class Solution {
    public int maxArea(int[] height) {
        int left = 0;
        int right = height.length - 1;
        int ans = 0;

        while (left < right) {
            int area = Math.min(height[left], height[right]) * (right - left);
            ans = Math.max(ans, area);

            // Math 属于 java.lang，不需要额外 import
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return ans;
    }
}
```

## 本次困惑与解答

以下记录本次实际遇到的问题。

### 为什么right要等于长度减一

长度表示元素个数，下标从 0 开始：

```python
height = [1, 8, 6, 2]
# 下标：   0  1  2  3

len(height)      # 4
len(height) - 1  # 3，最后一个合法下标
```

right 记录的是最右边的下标，所以要减一，不能直接取长度。

### 为什么Python出现IndexError

当时把右指针写成了：

```python
right += 1  # 错误：继续向数组右侧走
```

应为：

```python
right -= 1  # 正确：向中间靠拢
```

示例有 9 个元素，下标为 0～8。right 初始就是 8，再增加到 9，下一轮读取 height[9] 就越界。

错误行出现在“读取数组、计算面积”的位置，但错误的状态可能来自上一轮的指针更新。排错时需要一起检查初始化、循环条件和移动方向。

```text
left ->                 <- right
     += 1               -= 1
```

### 为什么C++提示mrea未声明

定义变量时写的是 area，使用时却拼成 mrea：

```cpp
int area = std::min(height[left], height[right]) * (right - left);
ans = std::max(ans, area);  // 必须与定义的变量名完全相同
```

“use of undeclared identifier” 表示用了未声明的名字。这里是拼写问题，不是面积公式错了。

### 为什么Java找不到min和max

Python 可以直接调用内置函数 min/max；Java 在这段代码中需要通过 Math 类调用：

```java
int area = Math.min(height[left], height[right]) * (right - left);
ans = Math.max(ans, area);
```

Math 的 M 要大写；它位于 java.lang 包中，不需要额外导入。min 与 max 都是静态方法，分别取较小值和较大值。参见 [Java Math 官方文档](https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html)。

### 为什么C++没写std也能通过

本次在力扣中直接写 min/max 可以编译，说明评测环境使这些名字在当前作用域可用。常见原因是平台预置了 using namespace std，或相关 using 声明；这不表示 C++ 自动省略所有 std::。

本地写完整程序时，可以显式包含头文件并写限定名：

```cpp
#include <algorithm>

int main() {
    int x = std::min(3, 5);
    return x == 3 ? 0 : 1;
}
```

也可以在作用域中明确引入所需名字：

```cpp
using std::min;
using std::max;
// 此后可直接写 min(a, b)、max(a, b)
```

std 是命名空间，std::min 是其中的函数；Java 的 Math 是类，Math.min 是类的静态方法，二者不能直接照搬语法。

### 为什么import Math不对

当时尝试写：

```java
// 错误示范
import Math;
```

Java 的普通类导入需要包路径，例如 import java.lang.Math。但 java.lang 中的类本来就自动可用，因此这行普通导入没有必要；而且普通导入类也不会让其静态方法自动变成当前作用域中的名字。

默认写法还是 Math.min(a, b)、Math.max(a, b)。

### 在IDEA里能直接写min吗

是否需要类名取决于 Java 代码的导入和声明，与使用 IDEA 还是力扣编辑器无关。

如果希望直接使用 min/max，可以在文件顶部、class 之前做静态导入：

```java
import static java.lang.Math.min;
import static java.lang.Math.max;

// 此后方法中可以写：
// int area = min(height[left], height[right]) * (right - left);
// ans = max(ans, area);
```

两种合法写法：

| 导入方式 | 调用方式 |
| --- | --- |
| 不加额外导入，或普通导入 java.lang.Math | Math.min(a, b) |
| import static java.lang.Math.min | min(a, b) |

静态导入的是类的静态成员。初学时优先写 Math.min，来源更直观；需要省略类名时，再显式静态导入。参见 [Java 静态导入说明](https://docs.oracle.com/javase/8/docs/technotes/guides/language/static-import.html)。

## 语言差别与常用接口

| 操作 | Python | C++ | Java |
| --- | --- | --- | --- |
| 长度 | len(height) | height.size() | height.length |
| 最右下标 | len(height) - 1 | 转为 int 后减 1 | height.length - 1 |
| 取较小值 | min(a, b) | std::min(a, b) | Math.min(a, b) |
| 更新最大值 | ans = max(ans, area) | ans = std::max(ans, area); | ans = Math.max(ans, area); |
| 循环 | while left < right: 加缩进 | while (left < right) 加花括号 | 同 C++ |
| 左侧向右走 | left += 1 | ++left; | left++; |
| 右侧向左走 | right -= 1 | --right; | right--; |
| 返回 | return ans | return ans; | return ans; |

补充讲解：C++ vector 的 size() 返回无符号大小类型。源码先转成 int 再减一；在本题 n <= 100000 的约束下转换安全，也便于统一指针变量的类型。

常用语法复习见[语言速查表](../../../docs/language-cheatsheet.md#最值函数与导入)。

## 复杂度与边界

每轮只移动一个端点，使 right−left 减少 1；长度为 n 时循环恰好执行 n−1 轮。

- 时间复杂度 O(n)。
- 辅助空间 O(1)，只保存几个整数。
- 返回一个面积整数，不返回下标，不修改输入。

按本题 n <= 100000、0 <= height[i] <= 10000，最大面积不超过 99999 × 10000 = 999990000，C++ 常见 32 位 int 和 Java int 能容纳。本实现针对题目有效输入，题目保证至少两条线。

| 输入 | 最大面积 | 检查点 |
| --- | ---: | --- |
| [1, 1] | 1 | 最少两个元素 |
| [0, 0] | 0 | 高度为零 |
| [8, 8] | 8 | 等高，距离只有 1 |
| [8, 1, 8] | 16 | 两端等高，中间线不扣除面积 |
| [1, 2, 3, 4, 5] | 6 | 单调递增 |
| [5, 4, 3, 2, 1] | 6 | 单调递减 |
| [1, 100, 100, 1] | 100 | 答案在内部，不能只看两端 |
| [1, 8, 6, 2, 5, 4, 8, 3, 7] | 49 | 本次练习的例子 |

验证会用枚举所有下标对的暴力参考检查小数组，再用可直接计算结果的长度 100000 输入检查边界。测试覆盖不等于穷尽全部输入；正确性依据是前面的排除证明。

## 复习自测

1. 为什么两个 8 只能得到 40，而 8 与 7 能得到 49？
2. 宽度为什么是 right−left，不是 right−left+1？
3. 为什么 right 从长度减一开始，为什么要减一移动？
4. 保留短边、只移动长边，为什么不可能超过当前面积？两边等高怎么办？
5. Java 普通导入 Math 与静态导入 min 有什么区别？换到 IDEA 是否改变这些规则？
6. 为什么 return ans 要放在 while 外面？请不看源码手写三种语言中的一种。
