import java.util.HashMap;
import java.util.Map;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            if (seen.containsKey(need)) {  // 先判断存在，再获取下标
                return new int[]{seen.get(need), i};
            }
            seen.put(nums[i], i);  // 先查，后存
        }
        return new int[0];
    }
}
