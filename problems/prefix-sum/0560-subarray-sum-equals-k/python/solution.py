from typing import List


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        ans = 0
        prefix = 0
        # 空前缀的和为 0，出现一次，用于统计从下标 0 开始的子数组。
        counts = {0: 1}

        for num in nums:
            prefix += num
            need = prefix - k

            # 只查询此前的前缀；每次出现都对应一个合法起点。
            if need in counts:
                ans += counts[need]

            # 查询后才记录当前前缀，避免把空子数组算进去。
            if prefix in counts:
                counts[prefix] += 1
            else:
                counts[prefix] = 1

        return ans
