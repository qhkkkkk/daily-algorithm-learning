#include <algorithm>
#include <string>
#include <unordered_set>

class Solution {
public:
    int lengthOfLongestSubstring(std::string s) {
        std::unordered_set<char> seen;  // 只记录当前窗口内的字符
        int left = 0;
        int ans = 0;  // 历史最大长度，不随窗口缩短而减小
        const int n = static_cast<int>(s.size());

        for (int right = 0; right < n; ++right) {
            // 新字符尚未加入；先移出左端字符，直到不再冲突。
            while (seen.count(s[right]) > 0) {
                seen.erase(s[left]);
                ++left;
            }
            seen.insert(s[right]);
            ans = std::max(ans, right - left + 1);
        }
        return ans;
    }
};
