"""Run actual sources with shared deterministic cases and inspect Markdown links."""
import argparse
import importlib.util
import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SUM = ROOT / "problems/hash-table/0001-two-sum"
MOVE = ROOT / "problems/two-pointers/0283-move-zeroes"
CONTAINER = ROOT / "problems/two-pointers/0011-container-with-most-water"
THREE = ROOT / "problems/two-pointers/0015-3sum"
SUBSTRING = ROOT / "problems/sliding-window/0003-longest-substring-without-repeating-characters"
FENCE = chr(96) * 3
sys.dont_write_bytecode = True


def cases():
    rng = random.Random(283)
    sums = [
        ([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([3, 3], 6),
        ([0, 4, 3, 0], 0), ([-3, 4, 3, 90], 0),
        ([1, 12, 4, 8, 20], 28), ([-1000000000, 1000000000], 0),
        ([1000000000, -999999999], 1),
    ]
    # Keep exactly one answer, as required by the problem.
    while len(sums) < 308:
        a = [rng.randint(-100, 100) for _ in range(rng.randint(2, 25))]
        i, j = rng.sample(range(len(a)), 2)
        target = a[i] + a[j]
        pairs = [(x, y) for x in range(len(a)) for y in range(x + 1, len(a))
                 if a[x] + a[y] == target]
        if len(pairs) == 1:
            sums.append((a, target))
    moves = [[0], [1], [0, 0, 1], [1, 2, 3], [0, 0, 0],
             [0, 1, 0, 3, 12], [0, -1, 0, 2],
             [0, -2147483648, 0, 2147483647]]
    moves += [[rng.choice([0, 0, rng.randint(-50, 50)])
               for _ in range(rng.randint(1, 80))] for _ in range(300)]
    sums.append(([123, 456] + [1000000000] * 9998, 579))
    moves.append([0, 1, 0, -2] * 2500)
    return sums, moves


def validate_sum(a, target, result):
    assert len(result) == 2, (a, target, result)
    i, j = result
    assert 0 <= i < len(a) and 0 <= j < len(a) and i != j, result
    assert a[i] + a[j] == target, (a, target, result)


def expected_move(a):
    return [x for x in a if x != 0] + [0] * a.count(0)


def load_solution(path):
    spec = importlib.util.spec_from_file_location("candidate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Solution()


def check_python(sums, moves):
    for name in ("brute_force.py", "hash.py"):
        solution = load_solution(SUM / "python" / name)
        for a, target in sums:
            data = a.copy()
            validate_sum(a, target, solution.twoSum(data, target))
            assert data == a, "twoSum should preserve input"
        print("PASS Python twoSum/" + name)
    solution = load_solution(MOVE / "python/solution.py")
    for a in moves:
        data = a.copy()
        assert solution.moveZeroes(data) is None
        assert data == expected_move(a), (a, data)
    print("PASS Python moveZeroes")


def execute(command, **kwargs):
    result = subprocess.run(command, text=True, encoding="utf-8",
                            capture_output=True, timeout=90, **kwargs)
    if result.returncode:
        raise RuntimeError("Command failed: " + str(command)
                           + "\n" + result.stdout + "\n" + result.stderr)
    return result.stdout


def feed(sums, moves, is_sum):
    rows = []
    for item in (sums if is_sum else moves):
        a, target = item if is_sum else (item, None)
        rows.append(str(len(a)) + (" " + str(target) if is_sum else ""))
        rows.append(" ".join(map(str, a)))
    return "\n".join(rows) + "\n"


def validate_output(output, sums, moves, is_sum):
    lines = output.splitlines()
    items = sums if is_sum else moves
    assert len(lines) == len(items), (len(lines), len(items))
    for item, line in zip(items, lines):
        values = list(map(int, line.split()))
        if is_sum:
            validate_sum(*item, values)
        else:
            assert values == expected_move(item), (item, values)


def check_java(sums, moves, temp):
    for source, is_sum in [
        (SUM / "java/brute_force/Solution.java", True),
        (SUM / "java/hash/Solution.java", True),
        (MOVE / "java/Solution.java", False),
    ]:
        folder = temp / ("java-" + ("sum-" + source.parent.name if is_sum else "move"))
        folder.mkdir()
        shutil.copyfile(source, folder / "Solution.java")
        call = ("int[] r = new Solution().twoSum(a, target);" if is_sum else
                "new Solution().moveZeroes(a); int[] r = a;")
        target = "int target = sc.nextInt();" if is_sum else ""
        harness = """
import java.util.Scanner;
class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        StringBuilder out = new StringBuilder();
        while (sc.hasNextInt()) {
            int n = sc.nextInt();
            TARGET
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = sc.nextInt();
            CALL
            for (int x : r) out.append(x).append(' ');
            out.append('\\n');
        }
        System.out.print(out);
    }
}
""".replace("TARGET", target).replace("CALL", call)
        (folder / "Main.java").write_text(harness, encoding="utf-8")
        execute(["javac", "-encoding", "UTF-8", "Solution.java", "Main.java"], cwd=folder)
        output = execute(["java", "-cp", str(folder), "Main"],
                         input=feed(sums, moves, is_sum))
        validate_output(output, sums, moves, is_sum)
        print("PASS Java " + str(source.relative_to(ROOT)))


def check_native(sums, moves, temp, language, compiler):
    paths = [(SUM / language / ("brute_force." + language), True),
             (SUM / language / ("hash." + language), True)]
    if language == "cpp":
        paths.append((MOVE / "cpp/solution.cpp", False))
    for number, (source, is_sum) in enumerate(paths):
        if language == "cpp":
            call = ("auto r = Solution().twoSum(a, target);" if is_sum else
                    "Solution().moveZeroes(a); auto& r = a;")
            target = "int target; std::cin >> target;" if is_sum else ""
            harness = """
#include <iostream>
#include "SOURCE"
int main() {
    int n;
    while (std::cin >> n) {
        TARGET
        std::vector<int> a(n);
        for (int& x : a) std::cin >> x;
        CALL
        for (int x : r) std::cout << x << ' ';
        std::cout << '\\n';
    }
}
""".replace("SOURCE", source.as_posix()).replace("TARGET", target).replace("CALL", call)
            standard = "-std=c++17"
        else:
            harness = """
#include <stdio.h>
#include "SOURCE"
int main(void) {
    int n, target;
    while (scanf("%d%d", &n, &target) == 2) {
        int* a = malloc((size_t)n * sizeof(*a));
        if (!a) return 2;
        for (int i = 0; i < n; ++i) {
            if (scanf("%d", &a[i]) != 1) return 3;
        }
        int count = 0;
        int* r = twoSum(a, n, target, &count);
        if (count != 2 || !r) return 4;
        printf("%d %d\\n", r[0], r[1]);
        free(r);
        free(a);
    }
    /* Defensive extension outside the guaranteed-answer input contract. */
    int no_answer[] = {1, 2};
    int count = 99;
    int* r = twoSum(no_answer, 2, 99, &count);
    if (r != NULL || count != 0) { free(r); return 5; }
    return 0;
}
""".replace("SOURCE", source.as_posix())
            standard = "-std=c11"
        path = temp / (language + str(number) + "." + language)
        binary = temp / (language + str(number) + (".exe" if os.name == "nt" else ""))
        path.write_text(harness, encoding="utf-8")
        execute([compiler, standard, "-Wall", "-Wextra", "-Werror", "-pedantic",
                 str(path), "-o", str(binary)])
        output = execute([str(binary)], input=feed(sums, moves, is_sum))
        validate_output(output, sums, moves, is_sum)
        print("PASS " + language + " " + str(source.relative_to(ROOT)))


def markdown_text(path):
    return re.sub(FENCE + r".*?" + FENCE, "",
                  path.read_text(encoding="utf-8"), flags=re.S)


def anchors(path):
    result = set()
    counts = {}
    for title in re.findall(r"^#{1,6}\s+(.+)$", markdown_text(path), flags=re.M):
        title = re.sub(r"[*_]", "", title.replace(chr(96), "")).lower()
        slug = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
        number = counts.get(slug, 0)
        counts[slug] = number + 1
        result.add(slug if number == 0 else slug + "-" + str(number))
    return result


def check_docs():
    checked = 0
    for path in ROOT.rglob("*.md"):
        for link in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", markdown_text(path)):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link):
                continue
            target, _, fragment = unquote(link).partition("#")
            dest = (path.parent / target).resolve() if target else path
            assert dest.is_file(), (path, link, "missing file")
            if fragment and dest.suffix == ".md":
                assert fragment in anchors(dest), (path, link, "missing anchor")
            checked += 1
    for folder in (SUM, MOVE, CONTAINER, THREE, SUBSTRING):
        article = (folder / "README.md").read_text(encoding="utf-8")
        snippets = re.findall(FENCE + r"(?:cpp|java|python|c)\n(.*?)" + FENCE,
                              article, re.S)
        for source in folder.rglob("*"):
            if source.suffix not in (".cpp", ".java", ".py", ".c"):
                continue
            if folder == SUM and "brute_force" in str(source):
                if source.suffix != ".py":
                    continue  # Other brute force sources are linked only.
            assert source.read_text(encoding="utf-8").strip() in [
                s.strip() for s in snippets
            ], "Article/source mismatch: " + str(source)
    print("PASS Markdown links/anchors: " + str(checked))
    print("PASS Article/source consistency")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-all", action="store_true")
    parser.add_argument("--cc", default=os.environ.get("CC", "gcc"))
    parser.add_argument("--cxx", default=os.environ.get("CXX", "g++"))
    args = parser.parse_args()
    check_docs()
    sums, moves = cases()
    print("Cases per implementation: twoSum=" + str(len(sums))
          + ", moveZeroes=" + str(len(moves)))
    check_python(sums, moves)
    missing = []
    with tempfile.TemporaryDirectory(prefix="algorithm-check-") as name:
        temp = Path(name)
        if shutil.which("java") and shutil.which("javac"):
            check_java(sums, moves, temp)
        else:
            missing.append("Java (java + javac)")
        for language, command in (("c", args.cc), ("cpp", args.cxx)):
            compiler = shutil.which(command)
            if compiler:
                os.environ["PATH"] = str(Path(compiler).parent) + os.pathsep + os.environ.get("PATH", "")
                check_native(sums, moves, temp, language, compiler)
            else:
                missing.append(language + " (" + command + ")")
        from container_check import check_container
        check_container(temp, bool(shutil.which("java") and shutil.which("javac")),
                        shutil.which(args.cxx))
        from three_sum_check import check_three_sum
        check_three_sum(temp, bool(shutil.which("java") and shutil.which("javac")),
                        shutil.which(args.cxx))
        from substring_check import check_substring
        check_substring(temp, bool(shutil.which("java") and shutil.which("javac")),
                        shutil.which(args.cxx))
    for item in missing:
        print("SKIP " + item)
    if missing and args.require_all:
        raise SystemExit("Required compilers missing")
    print("PASS all available checks")


if __name__ == "__main__":
    main()
