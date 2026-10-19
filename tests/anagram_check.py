"""Cross-check LeetCode 438 sources with independent per-substring sorting."""
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import random
import shutil

from container_check import run

ROOT = Path(__file__).resolve().parents[1]
ANAGRAM = ROOT / "problems/sliding-window/0438-find-all-anagrams-in-a-string"


def brute(s, p):
    goal = sorted(p)
    return [i for i in range(len(s) - len(p) + 1)
            if sorted(s[i:i + len(p)]) == goal]


def anagram_cases():
    fixed = [
        ("cbaebabacd", "abc"), ("abab", "ab"), ("a", "a"), ("a", "b"),
        ("ab", "abc"), ("abc", "cba"), ("aaa", "aa"), ("aaaa", "aa"),
        ("baa", "aa"), ("aab", "ab"), ("abacbabc", "abc"), ("ab", "a"),
        ("zzzz", "zz"), ("aabb", "abb"),
    ]
    texts = ["".join(a) for n in range(1, 7) for a in product("ab", repeat=n)]
    patterns = ["".join(a) for n in range(1, 5) for a in product("ab", repeat=n)]
    inputs = fixed + [(s, p) for s in texts for p in patterns]
    rng = random.Random(438)
    inputs += [("".join(rng.choice("abcxyz") for _ in range(rng.randint(1, 40))),
                "".join(rng.choice("abcxyz") for _ in range(rng.randint(1, 12))))
               for _ in range(300)]
    cases = [(s, p, brute(s, p)) for s, p in inputs]
    cases += [
        ("a" * 30000, "a", list(range(30000))),
        ("a" * 30000, "a" * 30000, [0]),
        ("a" * 30000, "b", []),
        ("ab" * 15000, "ab", list(range(29999))),
        ("a" * 29999 + "z", "az", [29998]),
        ("z" * 29999, "z" * 30000, []),
    ]
    assert len(cases) == 4100
    return cases


def validate(s, p, expected, got):
    assert all(type(i) is int and 0 <= i <= len(s) - len(p) for i in got), got
    assert len(got) == len(set(got)), ("Duplicate starts", s[:30], p[:30], got)
    assert sorted(got) == expected, (s[:40], p[:40], expected[:20], got[:20])


def check_anagrams(temp, java_available, cpp_compiler):
    cases = anagram_cases()
    spec = spec_from_file_location("anagram_solution", ANAGRAM / "python/solution.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    solution = module.Solution()
    for s, p, expected in cases:
        got = solution.findAnagrams(s, p)
        validate(s, p, expected, got)
    print("PASS Python findAnagrams: " + str(len(cases)) + " cases")

    # Inputs are nonempty lowercase English strings under this problem's contract.
    stdin = "\n".join(s + " " + p for s, p, _ in cases) + "\n"

    def validate_output(output):
        lines = output.splitlines()
        assert len(lines) == len(cases), (len(lines), len(cases))
        for (s, p, expected), line in zip(cases, lines):
            numbers = list(map(int, line.split()))
            assert numbers and numbers[0] == len(numbers) - 1, line
            validate(s, p, expected, numbers[1:])

    if java_available:
        folder = temp / "anagram-java"
        folder.mkdir()
        shutil.copyfile(ANAGRAM / "java/Solution.java", folder / "Solution.java")
        harness = """
import java.util.List;
import java.util.Scanner;
class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        StringBuilder out = new StringBuilder();
        Solution solution = new Solution();
        while (sc.hasNext()) {
            String s = sc.next();
            String p = sc.next();
            List<Integer> answer = solution.findAnagrams(s, p);
            out.append(answer.size());
            for (int index : answer) out.append(' ').append(index);
            out.append('\\n');
        }
        System.out.print(out);
    }
}
"""
        (folder / "Main.java").write_text(harness, encoding="utf-8")
        run(["javac", "-encoding", "UTF-8", "Solution.java", "Main.java"], cwd=folder)
        validate_output(run(["java", "-cp", str(folder), "Main"], input=stdin))
        print("PASS Java findAnagrams: " + str(len(cases)) + " cases")

    if cpp_compiler:
        harness = """
#include <iostream>
#include "SOURCE"
int main() {
    std::string s, p;
    Solution solution;
    while (std::cin >> s >> p) {
        const auto originalS = s;
        const auto originalP = p;
        auto answer = solution.findAnagrams(s, p);
        if (s != originalS || p != originalP) return 2;
        std::cout << answer.size();
        for (int index : answer) std::cout << ' ' << index;
        std::cout << '\\n';
    }
}
""".replace("SOURCE", (ANAGRAM / "cpp/solution.cpp").as_posix())
        entry = temp / "anagram.cpp"
        entry.write_text(harness, encoding="utf-8")
        binary = temp / "anagram-check.exe"
        run([cpp_compiler, "-std=c++17", "-Wall", "-Wextra", "-Werror",
             "-pedantic", str(entry), "-o", str(binary)])
        validate_output(run([str(binary)], input=stdin))
        print("PASS C++ findAnagrams: " + str(len(cases)) + " cases")
