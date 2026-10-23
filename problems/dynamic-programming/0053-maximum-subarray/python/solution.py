class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        # 子数组必须非空，用首元素初始化，才能正确处理全负数。
        current = nums[0]
        ans = nums[0]

        for i in range(1, len(nums)):
            # 以当前位置结尾：重新开始，或接上前一段。
            current = max(nums[i], current + nums[i])
            ans = max(ans, current)

        return ans
