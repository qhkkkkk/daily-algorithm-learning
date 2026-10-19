#include <string>
#include <vector>

class Solution {
public:
    std::vector<int> findAnagrams(std::string s, std::string p) {
        int m = static_cast<int>(p.size());
        int n = static_cast<int>(s.size());
        std::vector<int> ans;
        if (m > n) {
            return ans;
        }

        std::vector<int> target(26, 0);
        std::vector<int> window(26, 0);
        for (char ch : p) {
            int index = ch - 'a';
            ++target[index];
        }
        for (int i = 0; i < m; ++i) {
            int index = s[i] - 'a';
            ++window[index];
        }
        if (window == target) {
            ans.push_back(0);
        }

        for (int right = m; right < n; ++right) {
            int old_index = s[right - m] - 'a';
            --window[old_index];
            int new_index = s[right] - 'a';
            ++window[new_index];
            // vector 的 == 比较长度与对应元素
            if (window == target) {
                ans.push_back(right - m + 1);
            }
        }
        return ans;
    }
};
