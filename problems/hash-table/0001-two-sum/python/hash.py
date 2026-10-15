class Solution:
    def twoSum(self, nums, target):
        seen = {}  # 数值 -> 已经遍历过的下标
        for i, value in enumerate(nums):
            need = target - value
            if need in seen:  # 先查，再存，避免同一个元素使用两次
                return [seen[need], i]
            seen[value] = i
        return []
