"""Verify LeetCode 15 triplets, multiplicity, completeness and duplicate suppression."""
from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
from pathlib import Path
import random
import shutil

from container_check import run

ROOT = Path(__file__).resolve().parents[1]
THREE = ROOT / "problems/two-pointers/0015-3sum"


def three_sum_cases():
    fixed = [
        [-1, 0, 1, 2, -1, -4], [0, 1, 1], [0, 0, 0], [0, 0, 0, 0],
        [-1, -1, -1, 0, 1, 2], [-2, 0, 0, 2, 2],
        [-2, -2, 0, 0, 2, 2], [-4, -2, -2, 0, 2, 2, 4],
        [1, 2, 3], [-3, -2, -1], [-100000, 0, 100000],
        [-100000, -100000, 100000], [-1, -1, 2], [-2, 1, 1],
        [-3, -1, 0, 1, 2, 3],
    ]
    inputs = fixed + [list(a) for n in range(3, 7)
                      for a in product((-1, 0, 1), repeat=n)]
    rng = random.Random(15)
    inputs += [[rng.randint(-20, 20) for _ in range(rng.randint(3, 35))]
               for _ in range(400)]
    cases = [(a, {tuple(sorted(t)) for t in combinations(a, 3) if sum(t) == 0})
             for a in inputs]
    cases += [
        ([0] * 3000, {(0, 0, 0)}),
        ([1] * 3000, set()),
        ([-1] * 3000, set()),
        ([-1] * 1000 + [0] * 1000 + [1] * 1000, {(-1, 0, 1), (0, 0, 0)}),
        ([-100000] + [0] * 2998 + [100000],
         {(-100000, 0, 100000), (0, 0, 0)}),
    ]
    return cases


def validate(values, expected, got):
    available = Counter(values)
    normalized = []
    for triple in got:
        assert len(triple) == 3 and sum(triple) == 0, triple
        used = Counter(triple)
        assert all(count <= available[value] for value, count in used.items()), triple
        normalized.append(tuple(sorted(triple)))
    assert len(normalized) == len(set(normalized)), ("Duplicate triplets", got)
    assert set(normalized) == expected, (values[:40], expected, got)


def check_three_sum(temp, java_available, cpp_compiler):
    cases = three_sum_cases()
    spec = spec_from_file_location("three_sum_solution", THREE / "python/solution.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    solution = module.Solution()
    for values, expected in cases:
        data = values.copy()
        got = solution.threeSum(data)
        validate(values, expected, got)
        assert data == sorted(values), "Documented input sorting did not occur"
    print("PASS Python threeSum: " + str(len(cases)) + " cases")

    stdin = "\n".join(str(len(a)) + "\n" + " ".join(map(str, a))
                      for a, _ in cases) + "\n"

    def validate_output(output):
        lines = output.splitlines()
        assert len(lines) == len(cases), (len(lines), len(cases))
        for (values, expected), line in zip(cases, lines):
            numbers = list(map(int, line.split()))
            assert numbers and len(numbers) == 1 + numbers[0] * 3, line
            got = [numbers[i:i + 3] for i in range(1, len(numbers), 3)]
            validate(values, expected, got)

    if java_available:
        folder = temp / "three-sum-java"
        folder.mkdir()
        shutil.copyfile(THREE / "java/Solution.java", folder / "Solution.java")
        harness = """
import java.util.List;
import java.util.Scanner;
class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        StringBuilder out = new StringBuilder();
        while (sc.hasNextInt()) {
            int n = sc.nextInt();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = sc.nextInt();
            List<List<Integer>> answer = new Solution().threeSum(a);
            out.append(answer.size());
            for (List<Integer> triple : answer) {
                if (triple.size() != 3) throw new AssertionError("Invalid triple");
                for (int value : triple) out.append(' ').append(value);
            }
            out.append('\\n');
        }
        System.out.print(out);
    }
}
"""
        (folder / "Main.java").write_text(harness, encoding="utf-8")
        run(["javac", "-encoding", "UTF-8", "Solution.java", "Main.java"], cwd=folder)
        validate_output(run(["java", "-cp", str(folder), "Main"], input=stdin))
        print("PASS Java threeSum: " + str(len(cases)) + " cases")

    if cpp_compiler:
        harness = """
#include <iostream>
#include "SOURCE"
int main() {
    int n;
    while (std::cin >> n) {
        std::vector<int> a(n);
        for (int& value : a) std::cin >> value;
        auto answer = Solution().threeSum(a);
        std::cout << answer.size();
        for (const auto& triple : answer) {
            if (triple.size() != 3) return 2;
            for (int value : triple) std::cout << ' ' << value;
        }
        std::cout << '\\n';
    }
}
""".replace("SOURCE", (THREE / "cpp/solution.cpp").as_posix())
        entry = temp / "three-sum.cpp"
        entry.write_text(harness, encoding="utf-8")
        binary = temp / "three-sum-check.exe"
        run([cpp_compiler, "-std=c++17", "-Wall", "-Wextra", "-Werror",
             "-pedantic", str(entry), "-o", str(binary)])
        validate_output(run([str(binary)], input=stdin))
        print("PASS C++ threeSum: " + str(len(cases)) + " cases")
