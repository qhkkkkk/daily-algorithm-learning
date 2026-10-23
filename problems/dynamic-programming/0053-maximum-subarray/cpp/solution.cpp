#include <algorithm>
#include <vector>

class Solution {
public:
    int maxSubArray(std::vector<int>& nums) {
        // 子数组必须非空，不能把全负数输入的答案初始化为 0。
        int current = nums[0];
        int ans = nums[0];
        int n = static_cast<int>(nums.size());

        for (int i = 1; i < n; ++i) {
            // current 是以当前位置结尾的最大和，不是历史最大值。
            current = std::max(nums[i], current + nums[i]);
            ans = std::max(ans, current);
        }
        return ans;
    }
};
