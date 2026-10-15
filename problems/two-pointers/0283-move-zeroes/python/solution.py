class Solution:
    def moveZeroes(self, nums):
        pos = 0  # 下一个非零元素应该放的位置
        for i in range(len(nums)):
            if nums[i] != 0:
                nums[pos], nums[i] = nums[i], nums[pos]
                pos += 1
        # 原地修改，不需要 return nums
