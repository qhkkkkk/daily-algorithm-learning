import java.util.HashMap;
import java.util.Map;

class Solution {
    public int subarraySum(int[] nums, int k) {
        int ans = 0;
        int prefix = 0;
        Map<Integer, Integer> counts = new HashMap<>();
        // 空前缀保证从下标 0 开始的子数组也能被统计。
        counts.put(0, 1);

        for (int num : nums) {
            prefix += num;
            int need = prefix - k;
            if (counts.containsKey(need)) {
                ans += counts.get(need);
            }
            // 先查后存；getOrDefault 只读取，put 才插入或更新。
            counts.put(prefix, counts.getOrDefault(prefix, 0) + 1);
        }
        return ans;
    }
}
