class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()  # 当前窗口中的字符，不保存重复元素
        left = 0
        ans = 0  # 已找到的最大长度

        for right in range(len(s)):
            # 先解决新字符与窗口的冲突，再将它加入集合。
            while s[right] in seen:
                seen.remove(s[left])
                left += 1

            seen.add(s[right])
            ans = max(ans, right - left + 1)

        return ans
