#include <unordered_map>
#include <vector>

class Solution {
public:
    int subarraySum(std::vector<int>& nums, int k) {
        int ans = 0;
        int prefix = 0;
        std::unordered_map<int, int> counts;
        // 空前缀保证从下标 0 开始的子数组也能被统计。
        counts[0] = 1;

        for (int num : nums) {
            prefix += num;
            int need = prefix - k;
            if (counts.find(need) != counts.end()) {
                ans += counts[need];
            }
            // 必须先查后存；不存在的 int 值会先初始化为 0。
            counts[prefix]++;
        }
        return ans;
    }
};
