class Solution:
    def maxArea(self, height):
        left = 0
        right = len(height) - 1  # 长度减一，才是最后一个合法下标
        ans = 0

        while left < right:
            area = min(height[left], height[right]) * (right - left)
            ans = max(ans, area)

            # 换掉较矮的一侧，才有机会提高限制水位的高度
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1  # 右边向左走，不能写 += 1

        return ans
