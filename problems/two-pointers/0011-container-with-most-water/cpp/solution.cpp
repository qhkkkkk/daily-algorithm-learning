#include <algorithm>
#include <vector>

class Solution {
public:
    int maxArea(std::vector<int>& height) {
        int left = 0;
        int right = static_cast<int>(height.size()) - 1;
        int ans = 0;

        while (left < right) {
            int area = std::min(height[left], height[right]) * (right - left);
            ans = std::max(ans, area);

            // 保留短边、只移动长边，不可能让面积超过当前值
            if (height[left] < height[right]) {
                ++left;
            } else {
                --right;
            }
        }
        return ans;
    }
};
