class Solution:
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):  # 从 i 后面开始
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
