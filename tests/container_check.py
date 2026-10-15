"""Cross-check LeetCode 11 actual sources against brute force on small inputs."""
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import random
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CONTAINER = ROOT / "problems/two-pointers/0011-container-with-most-water"


def area_cases():
    def brute(a):
        return max(min(a[i], a[j]) * (j - i)
                   for i in range(len(a)) for j in range(i + 1, len(a)))

    fixed = [
        [1, 8, 6, 2, 5, 4, 8, 3, 7], [1, 1], [0, 0], [0, 10000],
        [8, 8], [8, 1, 8], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1],
        [1, 100, 100, 1], [5, 5, 5, 5], [2, 3, 4, 5, 18, 17, 6],
    ]
    inputs = fixed + [list(a) for n in range(2, 6)
                      for a in product(range(4), repeat=n)]
    rng = random.Random(11)
    inputs += [[rng.randint(0, 10000) for _ in range(rng.randint(2, 35))]
               for _ in range(300)]
    result = [(a, brute(a)) for a in inputs]
    # Closed-form expectations avoid a quadratic oracle on maximum-size inputs.
    result += [
        ([10000] * 100000, 999990000),
        ([10000] + [0] * 99998 + [10000], 999990000),
        ([10000] + [0] * 99999, 0),
    ]
    return result


def run(command, **kwargs):
    result = subprocess.run(command, text=True, encoding="utf-8",
                            capture_output=True, timeout=90, **kwargs)
    if result.returncode:
        raise RuntimeError(str(command) + "\n" + result.stdout + "\n" + result.stderr)
    return result.stdout


def check_container(temp, java_available, cpp_compiler):
    cases = area_cases()
    spec = spec_from_file_location("container_solution", CONTAINER / "python/solution.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    solution = module.Solution()
    for values, expected in cases:
        data = values.copy()
        got = solution.maxArea(data)
        assert got == expected and data == values, (values[:40], expected, got)
    print("PASS Python maxArea: " + str(len(cases)) + " cases")

    # Stream cases through temporary entry points that invoke the real source.
    stdin = "\n".join(str(len(a)) + "\n" + " ".join(map(str, a))
                      for a, _ in cases) + "\n"

    def validate(output):
        results = list(map(int, output.split()))
        assert len(results) == len(cases), (len(results), len(cases))
        for (values, expected), got in zip(cases, results):
            assert got == expected, (values[:40], expected, got)

    if java_available:
        folder = temp / "container-java"
        folder.mkdir()
        shutil.copyfile(CONTAINER / "java/Solution.java", folder / "Solution.java")
        harness = """
import java.util.Arrays;
import java.util.Scanner;
class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        StringBuilder out = new StringBuilder();
        while (sc.hasNextInt()) {
            int n = sc.nextInt();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = sc.nextInt();
            int[] original = a.clone();
            int answer = new Solution().maxArea(a);
            if (!Arrays.equals(a, original)) throw new AssertionError("Input changed");
            out.append(answer).append('\\n');
        }
        System.out.print(out);
    }
}
"""
        (folder / "Main.java").write_text(harness, encoding="utf-8")
        run(["javac", "-encoding", "UTF-8", "Solution.java", "Main.java"], cwd=folder)
        validate(run(["java", "-cp", str(folder), "Main"], input=stdin))
        print("PASS Java maxArea: " + str(len(cases)) + " cases")

    if cpp_compiler:
        source = CONTAINER / "cpp/solution.cpp"
        harness = """
#include <iostream>
#include "SOURCE"
int main() {
    int n;
    while (std::cin >> n) {
        std::vector<int> a(n);
        for (int& value : a) std::cin >> value;
        const auto original = a;
        int answer = Solution().maxArea(a);
        if (a != original) return 2;
        std::cout << answer << '\\n';
    }
}
""".replace("SOURCE", source.as_posix())
        entry = temp / "container.cpp"
        entry.write_text(harness, encoding="utf-8")
        binary = temp / "container-check.exe"
        run([cpp_compiler, "-std=c++17", "-Wall", "-Wextra", "-Werror",
             "-pedantic", str(entry), "-o", str(binary)])
        validate(run([str(binary)], input=stdin))
        print("PASS C++ maxArea: " + str(len(cases)) + " cases")
