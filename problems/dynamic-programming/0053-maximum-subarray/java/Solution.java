class Solution {
    public int maxSubArray(int[] nums) {
        // 子数组必须非空，用首元素初始化，才能正确处理全负数。
        int current = nums[0];
        int ans = nums[0];

        for (int i = 1; i < nums.length; i++) {
            // 以当前位置结尾：重新开始，或接上前一段。
            current = Math.max(nums[i], current + nums[i]);
            ans = Math.max(ans, current);
        }
        return ans;
    }
}
