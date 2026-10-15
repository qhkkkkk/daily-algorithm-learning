#include <utility>
#include <vector>

class Solution {
public:
    void moveZeroes(std::vector<int>& nums) {
        int pos = 0;  // 慢指针：下一个非零元素的放置位置
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            if (nums[i] != 0) {
                std::swap(nums[pos], nums[i]);
                ++pos;
            }
        }
    }
};
