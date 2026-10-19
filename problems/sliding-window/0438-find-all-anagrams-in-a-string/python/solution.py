class Solution:
    def findAnagrams(self, s, p):
        m = len(p)
        n = len(s)
        ans = []
        if m > n:
            return ans

        target = [0] * 26
        window = [0] * 26

        for ch in p:
            index = ord(ch) - ord('a')
            target[index] += 1

        # 先统计第一个窗口 s[0:m]
        for i in range(m):
            index = ord(s[i]) - ord('a')
            window[index] += 1

        if window == target:
            ans.append(0)

        # right 是新进入窗口的字符下标，从 m 开始
        for right in range(m, n):
            old_index = ord(s[right - m]) - ord('a')
            window[old_index] -= 1
            new_index = ord(s[right]) - ord('a')
            window[new_index] += 1
            if window == target:
                ans.append(right - m + 1)

        return ans
