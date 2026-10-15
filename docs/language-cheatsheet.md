# C++ / Java / Python 刷题语法速查

[返回首页](../README.md)

## 目录

- [变量与代码块](#变量与代码块)
- [数组与循环](#数组与循环)
- [交换与返回值](#交换与返回值)
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

## 常用官方参考

用于继续查阅语法和接口：

- [Python：数据结构](https://docs.python.org/3/tutorial/datastructures.html)
- [Python：控制流程](https://docs.python.org/3/tutorial/controlflow.html)
- [Java 8：HashMap](https://docs.oracle.com/javase/8/docs/api/java/util/HashMap.html)
- [Java：数组入门](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/arrays.html)
