"""Verify LeetCode 53 against enumeration of all nonempty contiguous intervals."""
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import random
import shutil

from container_check import run

ROOT = Path(__file__).resolve().parents[1]
MAXIMUM = ROOT / "problems/dynamic-programming/0053-maximum-subarray"


def brute(nums):
    best = nums[0]
    for left in range(len(nums)):
        total = 0
        for right in range(left, len(nums)):
            total += nums[right]
            best = max(best, total)
    return best


def maximum_cases():
    fixed = [
        [-2, 1, -3, 4, -1, 2, 1, -5, 4],
        [1], [5, 4, -1, 7, 8], [-3, -2],
        [-2, -3, 4, -1, 2], [4, -1, 2, 1],
        [5, -10, 1], [1, 2, -10], [-5, 1, 2],
        [0], [0, 0, 0], [-1, 0, -2], [1, -1, 1, -1],
        [10000, -10000, 10000], [-10000], [10000],
    ]
    inputs = fixed + [
        list(values)
        for n in range(1, 6)
        for values in product((-2, -1, 0, 1, 2), repeat=n)
    ]
    rng = random.Random(53)
    inputs += [
        [rng.randint(-10000, 10000) for _ in range(rng.randint(1, 40))]
        for _ in range(300)
    ]
    cases = [(nums, brute(nums)) for nums in inputs]
    assert [expected for _, expected in cases[:9]] == [6, 1, 23, -2, 5, 6, 5, 3, 3]
    # Large cases have directly derivable answers; no quadratic oracle here.
    cases += [
        ([10000] * 100000, 1000000000),
        ([-10000] * 100000, -10000),
        ([0] * 100000, 0),
        ([1, -1] * 50000, 1),
        ([-1] * 99999 + [10000], 10000),
        ([10000] + [-1] * 99999, 10000),
    ]
    assert len(cases) == 4227
    return cases


def check_maximum_subarray(temp, java_available, cpp_compiler):
    cases = maximum_cases()
    spec = spec_from_file_location("maximum_solution", MAXIMUM / "python/solution.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    solution = module.Solution()
    for nums, expected in cases:
        data = nums.copy()
        got = solution.maxSubArray(data)
        assert type(got) is int and got == expected, (nums[:30], expected, got)
        assert data == nums, "Python maxSubArray modified its input"
    print("PASS Python maxSubArray: " + str(len(cases)) + " cases")

    stdin = "\n".join(str(len(nums)) + "\n" + " ".join(map(str, nums))
                      for nums, _ in cases) + "\n"

    def validate_output(output):
        lines = output.splitlines()
        assert len(lines) == len(cases), (len(lines), len(cases))
        for (nums, expected), line in zip(cases, lines):
            assert int(line) == expected, (nums[:30], expected, line)

    if java_available:
        folder = temp / "maximum-java"
        folder.mkdir()
        shutil.copyfile(MAXIMUM / "java/Solution.java", folder / "Solution.java")
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
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
            int[] original = nums.clone();
            out.append(solution.maxSubArray(nums)).append('\\n');
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
        print("PASS Java maxSubArray: " + str(len(cases)) + " cases")

    if cpp_compiler:
        harness = """
#include <iostream>
#include "SOURCE"
int main() {
    int n;
    Solution solution;
    while (std::cin >> n) {
        std::vector<int> nums(n);
        for (int& num : nums) std::cin >> num;
        const auto original = nums;
        std::cout << solution.maxSubArray(nums) << '\\n';
        if (nums != original) return 2;
    }
}
""".replace("SOURCE", (MAXIMUM / "cpp/solution.cpp").as_posix())
        entry = temp / "maximum.cpp"
        entry.write_text(harness, encoding="utf-8")
        binary = temp / "maximum-check.exe"
        run([cpp_compiler, "-std=c++17", "-Wall", "-Wextra", "-Werror",
             "-pedantic", str(entry), "-o", str(binary)])
        validate_output(run([str(binary)], input=stdin))
        print("PASS C++ maxSubArray: " + str(len(cases)) + " cases")
