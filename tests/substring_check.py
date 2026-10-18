"""Check the actual LeetCode 3 sources against an independent substring oracle."""
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import random
import shutil

from container_check import run

ROOT = Path(__file__).resolve().parents[1]
SUBSTRING = ROOT / "problems/sliding-window/0003-longest-substring-without-repeating-characters"


def brute(text):
    # Enumerate every substring independently, without the sliding-window rule.
    return max((end - start
                for start in range(len(text) + 1)
                for end in range(start, len(text) + 1)
                if len(set(text[start:end])) == end - start), default=0)


def substring_cases():
    fixed = [
        "", "a", " ", "bbbbb", "abcabcbb", "pwwkew", "abba", "abcb",
        "abcdc", "dvdf", "tmmzuxt", "au", "aab", "Aa", "aA1! a",
        "a a", "!!?!!", "abcdef", "abcda", "abcbde",
    ]
    texts = fixed + ["".join(chars) for n in range(8)
                     for chars in product("abc", repeat=n)]
    rng = random.Random(3)
    texts += ["".join(rng.choice("abAB01 !?\\\"")
                      for _ in range(rng.randint(0, 40)))
              for _ in range(300)]
    cases = [(text, brute(text)) for text in texts]
    printable = "".join(chr(code) for code in range(32, 127))
    cases += [
        ("a" * 50000, 1),
        ("ab" * 25000, 2),
        (("abc" * 16667)[:50000], 3),
        ((printable * 527)[:50000], len(printable)),
    ]
    assert len(cases) == 3604
    return cases


def check_substring(temp, java_available, cpp_compiler):
    cases = substring_cases()
    spec = spec_from_file_location("substring_solution", SUBSTRING / "python/solution.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    solution = module.Solution()
    for text, expected in cases:
        got = solution.lengthOfLongestSubstring(text)
        assert type(got) is int and got == expected, (text[:60], expected, got)
    print("PASS Python lengthOfLongestSubstring: " + str(len(cases)) + " cases")

    # Encode each string as its length followed by character codes. This retains
    # empty strings, spaces, quotes and backslashes in every language harness.
    stdin = "\n".join(str(len(text)) + "\n" + " ".join(str(ord(c)) for c in text)
                      for text, _ in cases) + "\n"

    def validate(output):
        values = list(map(int, output.split()))
        assert len(values) == len(cases), (len(values), len(cases))
        for (text, expected), got in zip(cases, values):
            assert got == expected, (text[:60], expected, got)

    if java_available:
        folder = temp / "substring-java"
        folder.mkdir()
        shutil.copyfile(SUBSTRING / "java/Solution.java", folder / "Solution.java")
        harness = """
import java.util.Scanner;
class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        StringBuilder out = new StringBuilder();
        Solution solution = new Solution();
        while (sc.hasNextInt()) {
            int n = sc.nextInt();
            StringBuilder input = new StringBuilder();
            for (int i = 0; i < n; i++) input.append((char) sc.nextInt());
            String text = input.toString();
            out.append(solution.lengthOfLongestSubstring(text)).append('\\n');
        }
        System.out.print(out);
    }
}
"""
        (folder / "Main.java").write_text(harness, encoding="utf-8")
        run(["javac", "-encoding", "UTF-8", "Solution.java", "Main.java"], cwd=folder)
        validate(run(["java", "-cp", str(folder), "Main"], input=stdin))
        print("PASS Java lengthOfLongestSubstring: " + str(len(cases)) + " cases")

    if cpp_compiler:
        harness = """
#include <iostream>
#include "SOURCE"
int main() {
    int n;
    Solution solution;
    while (std::cin >> n) {
        std::string text;
        for (int i = 0; i < n; ++i) {
            int code;
            std::cin >> code;
            text.push_back(static_cast<char>(code));
        }
        const auto original = text;
        int answer = solution.lengthOfLongestSubstring(text);
        if (text != original) return 2;
        std::cout << answer << '\\n';
    }
}
""".replace("SOURCE", (SUBSTRING / "cpp/solution.cpp").as_posix())
        entry = temp / "substring.cpp"
        entry.write_text(harness, encoding="utf-8")
        binary = temp / "substring-check.exe"
        run([cpp_compiler, "-std=c++17", "-Wall", "-Wextra", "-Werror",
             "-pedantic", str(entry), "-o", str(binary)])
        validate(run([str(binary)], input=stdin))
        print("PASS C++ lengthOfLongestSubstring: " + str(len(cases)) + " cases")
