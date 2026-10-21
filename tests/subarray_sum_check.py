"""Cross-check LeetCode 560 using independent continuous-interval enumeration."""
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import random
import shutil

from container_check import run

ROOT = Path(__file__).resolve().parents[1]
SUBARRAY = ROOT / "problems/prefix-sum/0560-subarray-sum-equals-k"


def brute(nums, k):
    answer = 0
    for left in range(len(nums)):
        total = 0
        for right in range(left, len(nums)):
            total += nums[right]
            if total == k:
                answer += 1
    return answer


def subarray_cases():
    fixed = [
        ([1, 1, 1], 2), ([1, 2, 3], 3), ([2, 3], 5),
        ([1], 0), ([0], 0), ([0, 0, 0], 0),
        ([1, -1, 1], 1), ([-1, -1, 1], -1), ([2, -1], 1),
        ([3], 3), ([-3], -3), ([1000, -1000, 1000], 0),
        ([1, 2], 10000000), ([-1, -2], -10000000),
    ]
    inputs = fixed + [
        (list(values), k)
        for n in range(1, 6)
        for values in product((-1, 0, 1), repeat=n)
        for k in range(-3, 4)
    ]
    rng = random.Random(560)
    inputs += [
        ([rng.randint(-10, 10) for _ in range(rng.randint(1, 35))],
         rng.randint(-30, 30))
        for _ in range(300)
    ]
    cases = [(a, k, brute(a, k)) for a, k in inputs]
    assert [expected for _, _, expected in cases[:9]] == [2, 2, 1, 0, 1, 6, 3, 3, 1]
    cases += [
        ([0] * 20000, 0, 200010000),
        ([1] * 20000, 1, 20000),
        ([1] * 20000, 2, 19999),
        ([1] * 20000, 0, 0),
        ([1, -1] * 10000, 0, 100000000),
        ([1000] * 20000, 10000000, 10001),
        ([-1000] * 20000, -10000000, 10001),
    ]
    assert len(cases) == 2862
    return cases


def check_subarray_sum(temp, java_available, cpp_compiler):
    cases = subarray_cases()
    spec = spec_from_file_location("subarray_solution", SUBARRAY / "python/solution.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    solution = module.Solution()
    for nums, k, expected in cases:
        data = nums.copy()
        got = solution.subarraySum(data, k)
        assert type(got) is int and got == expected, (nums[:30], k, expected, got)
        assert data == nums, "Python subarraySum modified its input"
    print("PASS Python subarraySum: " + str(len(cases)) + " cases")

    stdin = "\n".join(str(len(a)) + " " + str(k) + "\n" + " ".join(map(str, a))
                      for a, k, _ in cases) + "\n"

    def validate_output(output):
        lines = output.splitlines()
        assert len(lines) == len(cases), (len(lines), len(cases))
        for (nums, k, expected), line in zip(cases, lines):
            assert int(line) == expected, (nums[:30], k, expected, line)

    if java_available:
        folder = temp / "subarray-java"
        folder.mkdir()
        shutil.copyfile(SUBARRAY / "java/Solution.java", folder / "Solution.java")
        harness = """
import java.util.Arrays;
import java.util.Scanner;
class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        StringBuilder out = new StringBuilder();
        Solution solution = new Solution();
        while (sc.hasNextInt()) {
            int n = sc.nextInt();
            int k = sc.nextInt();
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
            int[] original = nums.clone();
            out.append(solution.subarraySum(nums, k)).append('\\n');
            if (!Arrays.equals(nums, original)) {
                throw new AssertionError("Input modified");
            }
        }
        System.out.print(out);
    }
}
"""
        (folder / "Main.java").write_text(harness, encoding="utf-8")
        run(["javac", "-encoding", "UTF-8", "Solution.java", "Main.java"], cwd=folder)
        validate_output(run(["java", "-cp", str(folder), "Main"], input=stdin))
        print("PASS Java subarraySum: " + str(len(cases)) + " cases")

    if cpp_compiler:
        harness = """
#include <iostream>
#include "SOURCE"
int main() {
    int n, k;
    Solution solution;
    while (std::cin >> n >> k) {
        std::vector<int> nums(n);
        for (int& num : nums) std::cin >> num;
        const auto original = nums;
        std::cout << solution.subarraySum(nums, k) << '\\n';
        if (nums != original) return 2;
    }
}
""".replace("SOURCE", (SUBARRAY / "cpp/solution.cpp").as_posix())
        entry = temp / "subarray.cpp"
        entry.write_text(harness, encoding="utf-8")
        binary = temp / "subarray-check.exe"
        run([cpp_compiler, "-std=c++17", "-Wall", "-Wextra", "-Werror",
             "-pedantic", str(entry), "-o", str(binary)])
        validate_output(run([str(binary)], input=stdin))
        print("PASS C++ subarraySum: " + str(len(cases)) + " cases")
