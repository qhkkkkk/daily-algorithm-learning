# C++ / Java / Python 刷题语法速查

[返回首页](../README.md)

## 目录

- [变量与代码块](#变量与代码块)
- [数组与循环](#数组与循环)
- [字符串与窗口长度](#字符串与窗口长度)
- [排序与二维结果](#排序与二维结果)
- [交换与返回值](#交换与返回值)
- [最值函数与导入](#最值函数与导入)
- [集合与成员判断](#集合与成员判断)
- [哈希表操作](#哈希表操作)
- [哈希表遍历](#哈希表遍历)
- [其他常见容器](#其他常见容器)
- [传参与原地修改](#传参与原地修改)
- [常用官方参考](#常用官方参考)

## 变量与代码块

| 内容 | C++ | Java | Python 3 |
| --- | --- | --- | --- |
| 整数变量 | `int x = 1;` | `int x = 1;` | `x = 1` |
| 赋值 | `x = 2;` | `x = 2;` | `x = 2` |
| 相等 / 不等 | `==` / `!=` | `==` / `!=` | `==` / `!=` |
| 自增 | `x++;` 或 `++x;` | `x++;` 或 `++x;` | `x += 1` |
| 逻辑与 / 或 / 非 | `&&` / `\|\|` / `!` | 同 C++ | `and` / `or` / `not` |
| 代码块 | 花括号 | 花括号 | 冒号后缩进 |
| 注释 | `//` | `//` | `#` |

这里的相等比较针对数值。Java 对象内容比较常用 equals，不要把数值规则无条件推广到字符串。

Python 不要求给变量声明类型，一般不写分号；变量可绑定不同类型的对象。`class Solution:` 定义类，`def method(self, ...):` 定义实例方法，self 表示当前实例。刷题时先保持平台给定接口。

## 数组与循环

| 操作 | C++ vector | Java int[] | Python list |
| --- | --- | --- | --- |
| 创建示例 | `std::vector<int> a = {1, 2};` | `int[] a = {1, 2};` | `a = [1, 2]` |
| 访问 / 修改 | `a[i]` / `a[i] = x;` | 同 C++ | `a[i]` / `a[i] = x` |
| 长度 | `a.size()` | `a.length` | `len(a)` |
| 添加末尾 | `a.push_back(x);` | 固定长度，不支持追加 | `a.append(x)` |
| 删除末尾 | `a.pop_back();` | 固定长度，不支持删除 | `a.pop()` |

C++ 示例需要 `#include <vector>`。Java 动态长度容器用 ArrayList，不是把 int[] 当作 ArrayList。

按下标遍历：

```cpp
for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
    // nums[i]
}
```

```java
for (int i = 0; i < nums.length; i++) {
    // nums[i]
}
```

```python
for i in range(len(nums)):
    # nums[i]
    pass
```

只要元素时：

```cpp
for (int value : nums) { /* value */ }
```

```java
for (int value : nums) { /* value */ }
```

```python
for value in nums:
    pass
```

Python 同时要下标和值时：

```python
for i, value in enumerate(nums):
    pass
```

range(a, b) 包含 a，不包含 b。range(n) 从 0 到 n−1。range 提供下一个值，所以在 for 中写 i += 1 不能改变后续由 range 提供的遍历序列。

## 字符串与窗口长度

| 操作 | C++ string | Java String | Python str |
| --- | --- | --- | --- |
| 示例定义 | `std::string s = "abc";` | `String s = "abc";` | `s = "abc"` |
| 长度 | `s.size()` 或 `s.length()` | `s.length()` | `len(s)` |
| 第 i 个字符 | `s[i]` | `s.charAt(i)` | `s[i]` |
| 尾部加字符 | `s.push_back('d')` | `s += "d"` 产生新字符串并赋值 | `s += "d"` 产生新字符串并重新绑定 |
| 尾部加字符串 | `s += "de"` | `s += "de"` | `s += "de"` |
| 去掉尾部字符 | 非空时 `s.pop_back()` | `s = s.substring(0, s.length() - 1)` | `s = s[:-1]` |
| 去掉开头字符 | `s.erase(0, 1)` | `s = s.substring(1)` | `s = s[1:]` |

C++ 需要 `<string>`。本表的 Java 删除示例要求非空；Python 对空串切片仍得到空串。Java/Python 字符串不可变，以上拼接、切片会产生新对象；滑动窗口通常只移动下标，不需要每轮修改原字符串。

### 长度方法与数组属性

Java 的 `arr.length` 是数组属性；`s.length()` 是 String 方法；`seen.size()` 是集合方法。String 不是数组，所以 `s[i]` 会报 `array required, but String found`；`s.length` 会查找不存在的字段。

Java `String.length()` 无参数，返回 int；`charAt(i)` 接收下标，返回 char。Python `len(s)` 是内置函数，返回长度整数；字符串下标得到长度为 1 的字符串。C++ size/length 无参数，返回 string 的 `size_type`，是无符号整数类型。

当输入长度在 int 范围内，可用 `int n = static_cast<int>(s.size());` 明确转换，避免与 int 下标比较时产生有符号/无符号警告。static_cast 是 C++ 转换语法，不是容器方法。

闭区间 `[left, right]` 长度为 `right - left + 1`；半开区间 `[left, right)` 长度为 `right - left`。下标 0～2 共有三个字符。

### C++字符串增删接口

| 名称与所属类型 | 参数 | 作用与返回值 |
| --- | --- | --- |
| `std::string::push_back(c)` | 一个 char | 尾部追加字符，返回 void |
| `std::string::pop_back()` | 无 | 删除尾部字符，调用前须非空，返回 void |
| `std::string::erase(pos, count)` | 起点下标、删除数量 | 从 pos 开始删除至多 count 个字符，返回该字符串的引用 |
| `std::string::size()` / `length()` | 无 | 返回字符单元数量，不是最后一个下标 |

`string::erase(0, 1)` 的 0 是位置，`unordered_set<char>::erase('a')` 的 'a' 是元素值；同名方法的参数含义取决于所属类型。

实例见[无重复字符的最长子串](../problems/sliding-window/0003-longest-substring-without-repeating-characters/README.md#本次困惑与解答)。接口参考：[Java String](https://docs.oracle.com/javase/8/docs/api/java/lang/String.html)。

## 排序与二维结果

| 操作 | Python | C++ | Java |
| --- | --- | --- | --- |
| 排序 | `nums.sort()` | `std::sort(nums.begin(), nums.end())` | `Arrays.sort(nums)` |
| 定义二维答案 | `ans = []` | `std::vector<std::vector<int>> ans;` | `List<List<Integer>> ans = new ArrayList<>();` |
| 添加一组三个值 | `ans.append([a, b, c])` | `ans.push_back({a, b, c});` | `ans.add(Arrays.asList(a, b, c));` |

这三种排序写法直接修改输入。Python 的 list.sort() 返回 None，不要写 nums = nums.sort()。这里的排序接口可直接用于刷题，不需要自己实现快速排序，也不应把接口名称与某一种具体排序算法等同。

C++ 的 sort 来自 `<algorithm>`，vector 来自 `<vector>`；begin() 是起始迭代器，end() 是尾后迭代器，sort 处理的是 [begin, end) 区间。

### C++的大括号与push_back

二维 vector 中的每个元素是一个 `vector<int>`。因此：

```cpp
ans.push_back({a, b, c});
```

可以拆成：

```cpp
std::vector<int> group = {a, b, c};
ans.push_back(group);
```

这里的大括号是列表初始化，初始化一个内层 vector；不是 Python 的字典或集合语法。push_back 的拼写固定，括号中传入要添加的单个元素；这个元素本身也可以是一个容器。

### Java的Arrays与ArrayList

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

// 以下写在方法内：
List<List<Integer>> ans = new ArrayList<>();
List<Integer> group = Arrays.asList(a, b, c);
ans.add(group);
```

List 是接口，ArrayList 是动态列表实现，Arrays 是数组工具类。泛型使用 Integer 包装类型，不能写 `List<int>`。a、b、c 是 int 时会自动装箱。

Arrays.asList 是固定的方法名；它把参数组织成列表。ans.add 负责把该列表放进外层答案。这不是必须组合使用的唯一方案，也可以 new 一个内层 ArrayList，再分别 add 三个数。

asList 返回的列表长度固定，不能追加或删除元素，允许替换已有位置的值；不等于不可修改列表。若之后需要改变长度，可写 `new ArrayList<>(Arrays.asList(a, b, c))`。参见 [Arrays 官方文档](https://docs.oracle.com/javase/8/docs/api/java/util/Arrays.html#asList-T...-)。

本题传入三个数的表达式，不是传整个 int[]。Arrays.asList(intArray) 不会逐个装箱 int，而会把这个基本类型数组视为一个元素。

### 条件与循环排错

Python 用 if / elif / else，C++ 和 Java 用 if / else if / else。互斥分支不要改成多个独立 if，以免移动指针后同一轮继续判断其他分支。

Python and、C++/Java && 都从左到右短路求值，常用来先保护下标：

```java
if (i > 0 && nums[i] == nums[i - 1]) {
    continue;
}
```

每层 while 只在自己每轮开始时检查条件，内部修改变量后不会自动跳出当前外层循环体。嵌套去重循环要自己检查 left < right，并保证能推进指针。

完整例子和本次错误分析见[三数之和题解](../problems/two-pointers/0015-3sum/README.md)。

## 交换与返回值

```cpp
std::swap(a, b);  // #include <utility>
```

```java
int temp = a;
a = b;
b = temp;
```

```python
a, b = b, a
```

Python 先算右侧旧值，再依次给左侧赋值。数组位置同样适用：

```python
nums[pos], nums[i] = nums[i], nums[pos]
```

单独的 `nums[i] = nums[i]` 是自身赋值，没有交换效果。

| 目的 | C++ | Java | Python |
| --- | --- | --- | --- |
| 返回两个下标 | `return {i, j};`，返回类型为 vector<int> | `return new int[]{i, j};` | `return [i, j]` |
| 空结果 | `return {};` | `return new int[0];` | `return []` |
| 无返回值方法 | `void` | `void` | 无显式 return 时返回 None |

## 最值函数与导入

| 操作 | Python | C++ | Java |
| --- | --- | --- | --- |
| 较小值 | `min(a, b)` | `std::min(a, b)` | `Math.min(a, b)` |
| 较大值 | `max(a, b)` | `std::max(a, b)` | `Math.max(a, b)` |

C++ 使用 `<algorithm>`，std 是命名空间；若已有 `using std::min;` 或 `using namespace std;` 等声明，可以省略相应的 std::。平台中能省略前缀，并不保证复制到独立程序后也能省略。

Java 的 Math 是 java.lang 包中的类，默认可用；min/max 是其静态方法。通常不写 import，直接调用 `Math.min`、`Math.max`。这在 IDEA 和力扣中遵循同样的 Java 规则。[Math 官方文档](https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html)。

`Max(...)` 和 `Max.max(...)` 都不是这里的标准调用。固定拼写为 `Math.max(a, b)`，参数 a、b 是待比较的两个数；本题传两个 int，返回较大的 int。Python 内置 max(a, b) 和 C++ `<algorithm>` 中的 std::max(a, b) 用途相同，所属名称不同。

`import Math;` 不合法；`import java.lang.Math;` 是普通类导入，本来就可以省略，而且不会让 min/max 自动变为未限定的方法名。

要直接写 min/max，需要静态导入：

```java
import static java.lang.Math.min;
import static java.lang.Math.max;

// 放在文件顶部、class 之前；此后方法中可写：
// int smaller = min(3, 5);
// int bigger = max(3, 5);
```

普通导入类与静态导入成员作用不同。初学时写 Math.min 更直观，静态导入作为可选语法。参见 [Java 静态导入说明](https://docs.oracle.com/javase/8/docs/technotes/guides/language/static-import.html)。

具体面积公式、越界排错与三种语言完整解法见[盛最多水的容器](../problems/two-pointers/0011-container-with-most-water/README.md)。

## 集合与成员判断

集合只保存元素，不保存“键到值”的映射，也不保留重复元素。它与下一节的哈希映射是两种用途。下面创建空的哈希集合：

```cpp
#include <unordered_set>
std::unordered_set<char> seen;
```

```java
import java.util.HashSet;
import java.util.Set;

// 放在方法或类中：
Set<Character> seen = new HashSet<>();
```

```python
seen = set()
```

`seen` 是变量名；Python `set()` 调用内置集合类型创建空集合，`=` 完成赋值。`{}` 是空字典，`{"a", "b"}` 则是含两个字符串元素的集合。

Java Set 是接口，HashSet 是实现；泛型 `<Character>` 表示字符包装类型，不能写 `<char>`。传入 char 时会自动装箱；`new HashSet<>()` 创建对象，右边尖括号的类型由左边推断。这些集合不按下标访问，算法不应依赖其迭代顺序。

| 目的 | C++ unordered_set | Java HashSet | Python set |
| --- | --- | --- | --- |
| 添加元素 c | `seen.insert(c)` | `seen.add(c)` | `seen.add(c)` |
| 判断存在 | `seen.count(c) > 0` | `seen.contains(c)` | `c in seen` |
| 删除元素 c | `seen.erase(c)` | `seen.remove(c)` | `seen.remove(c)` |
| 数量 | `seen.size()` | `seen.size()` | `len(seen)` |
| 清空 | `seen.clear()` | `seen.clear()` | `seen.clear()` |

### 参数和返回值

下面指单个元素的常见重载，c 是要处理的元素，不是位置：

| 接口归属 | 名称 | 返回值与作用 |
| --- | --- | --- |
| C++ `<unordered_set>` | `count(c)` | 返回 size_type 计数，元素唯一，所以只有 0 或 1，不是下标 |
| C++ `<unordered_set>` | `insert(c)` | 返回包含迭代器和 bool 的 pair；bool 表示是否新插入，已有元素不会再增加一份 |
| C++ `<unordered_set>` | `erase(c)` | 按键删除，返回实际删除数量，这里为 0 或 1，缺失时不报错 |
| Java `java.util.Set` / `HashSet` | `contains(c)` | 返回 boolean，表示元素是否存在 |
| Java `java.util.Set` / `HashSet` | `add(c)` | 新增成功返回 true，已有元素返回 false |
| Java `java.util.Set` / `HashSet` | `remove(c)` | 找到并删除返回 true，不存在返回 false |
| Python 内置 `set` | `add(c)` | 添加元素，返回 None，已有时不重复添加 |
| Python 内置 `set` | `remove(c)` | 删除元素，返回 None，不存在则抛 KeyError |
| Python 运算符 | `c in seen` | 返回 bool，判断是否存在 |

C++ 的 `seen = {'a', 'b'}` 中 count('a') 为 1，count('c') 为 0；这不是统计 a 在原字符串中共出现几次。换成允许重复元素的 multiset 时，计数范围不同，不要把 0/1 推广到所有 count 方法。

补充接口：Python `discard(c)` 在元素不存在时也可调用。本题维护了集合与窗口的一致性，源码使用 remove 即可。三种语言的 size/len 返回数量；clear 清空原集合，本题没有使用它。

### 用集合维护字符串窗口

```cpp
while (seen.count(s[right]) > 0) {
    seen.erase(s[left]);
    ++left;
}
seen.insert(s[right]);
```

```java
while (seen.contains(s.charAt(right))) {
    seen.remove(s.charAt(left));
    left++;
}
seen.add(s.charAt(right));
```

```python
while s[right] in seen:
    seen.remove(s[left])
    left += 1
seen.add(s[right])
```

条件查询右端候选字符，删除的是实际离开窗口的左端字符。本模板先解决冲突再插入；不能先插入候选字符，再原样照搬这个成员判断条件。

完整推演见[第 3 题](../problems/sliding-window/0003-longest-substring-without-repeating-characters/README.md)。接口依据：[Java Set](https://docs.oracle.com/javase/8/docs/api/java/util/Set.html)、[Python 集合类型](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)、[C++ 标准草案 unordered_set](https://eel.is/c++draft/unord.set)。

## 哈希表操作

以下 seen 均为“键 -> 值”的映射。C++ 用 unordered_map，Java 用 HashMap，Python 用 dict。

| 操作 | C++ | Java | Python |
| --- | --- | --- | --- |
| 创建 | `std::unordered_map<int, int> seen;` | `Map<Integer, Integer> seen = new HashMap<>();` | `seen = {}` |
| 插入 / 更新 | `seen[k] = v;` | `seen.put(k, v);` | `seen[k] = v` |
| 判断存在 | `seen.find(k) != seen.end()` 或 `seen.count(k) > 0` | `seen.containsKey(k)` | `k in seen` |
| 读取 | `seen.at(k)` 或迭代器的 second | `seen.get(k)` | `seen[k]` |
| 删除 | `seen.erase(k);` | `seen.remove(k);` | `del seen[k]` 或 `seen.pop(k)` |
| 清空 | `seen.clear();` | `seen.clear();` | `seen.clear()` |
| 数量 | `seen.size()` | `seen.size()` | `len(seen)` |
| 空判断 | `seen.empty()` | `seen.isEmpty()` | `not seen` |

缺失键的差别：

- C++ `seen[k]` 会插入默认值，int 默认值为 0；`at(k)` 会抛异常；`find(k)` 返回 end。
- Java `get(k)` 返回 null，若立即拆箱为 int 会抛 NullPointerException。
- Python `seen[k]` 抛 KeyError；`seen.get(k)` 默认返回 None。del 和不带默认值的 pop 也要求键存在。

两数之和需要区分“键不存在”和“下标恰好是 0”，所以不能拿读取值的真假当作存在判断。`in` 对字典检查 key，对列表则检查元素；列表中的查找通常是 O(n)，不能因为同样写 in 就认为都是平均 O(1)。

## 哈希表遍历

```cpp
for (const auto& item : seen) {
    int key = item.first;
    int value = item.second;
}
```

auto 是编译期类型推断，不是动态类型。这里用引用避免复制每个键值对。

```java
for (Map.Entry<Integer, Integer> entry : seen.entrySet()) {
    int key = entry.getKey();
    int value = entry.getValue();
}
```

entrySet 提供键值对视图；Map.Entry 表示一组 key/value。

```python
for key, value in seen.items():
    print(key, value)

for key in seen:
    print(key)
```

items 提供键值对视图。Python 3 的 dict 保持插入顺序，但不自动按键排序；C++ unordered_map 和 Java HashMap 不保证迭代顺序。算法不要依赖未约定的顺序。

## 其他常见容器

| 用途 | C++ | Java | Python |
| --- | --- | --- | --- |
| 动态数组 | vector | ArrayList | list |
| 哈希映射 | unordered_map | HashMap | dict |
| 哈希集合 | unordered_set | HashSet | set |
| 按键排序的映射 | map | TreeMap | 无内置直接对应；按需排序 |
| 按值排序的集合 | set | TreeSet | 无内置直接对应；按需排序 |

Map 存“键 -> 值”，Set 只保存元素。C++ map 通常由平衡树实现，查找 O(log n)；unordered_map 使用哈希，平均 O(1)。Java HashMap/TreeMap 对应的选择思路类似。

## 传参与原地修改

| 语言 | 本题参数 | 修改元素 | 仅让参数名改指向新对象 |
| --- | --- | --- | --- |
| C++ | `std::vector<int>& nums` | 修改原 vector | 对引用变量赋值会修改被引用对象，并非重绑定 |
| Java | `int[] nums` | 修改调用方可见的数组 | `nums = new int[]{…}` 不改变调用方变量 |
| Python | `nums` | 修改调用方可见的列表 | `nums = [...]` 不改变调用方变量 |

Java 是按值传递，数组参数传递的是引用的值；不能笼统称为 C++ 式引用传递。Python 可理解为参数名与调用方暂时绑定同一个对象。移动零采用下标修改，三种语言均能满足原地要求。

字符串另作区分：C++ `std::string s` 按值传参，通常复制传入的左值字符串；`const std::string& s` 是只读引用，可避免该复制。Java `String s` 传引用的值，Python 参数名绑定字符串对象；两种语言的字符串不可变。本题源码只读输入，返回一个长度整数，不返回新子串。计算空间时，应将 C++ 按值形参可能产生的副本与窗口集合分开说明。

## 常用官方参考

用于继续查阅语法和接口：

- [Python：数据结构](https://docs.python.org/3/tutorial/datastructures.html)
- [Python：控制流程](https://docs.python.org/3/tutorial/controlflow.html)
- [Java 8：HashMap](https://docs.oracle.com/javase/8/docs/api/java/util/HashMap.html)
- [Java：数组入门](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/arrays.html)
