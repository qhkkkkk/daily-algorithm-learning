#include <unordered_map>
#include <vector>

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& nums, int target) {
        std::unordered_map<int, int> seen;  // 数值 -> 下标
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            int need = target - nums[i];
            auto it = seen.find(need);  // find 不会插入不存在的键
            if (it != seen.end()) {
                return {it->second, i};
            }
            seen[nums[i]] = i;  // 先查，后存
        }
        return {};
    }
};
