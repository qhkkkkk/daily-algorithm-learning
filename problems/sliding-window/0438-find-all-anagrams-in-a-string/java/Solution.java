import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        int m = p.length();
        int n = s.length();
        List<Integer> ans = new ArrayList<>();
        if (m > n) {
            return ans;
        }

        int[] target = new int[26];
        int[] window = new int[26];
        for (int i = 0; i < m; i++) {
            int index = p.charAt(i) - 'a';
            target[index]++;
        }
        for (int i = 0; i < m; i++) {
            int index = s.charAt(i) - 'a';
            window[index]++;
        }
        if (Arrays.equals(window, target)) {
            ans.add(0);
        }

        for (int right = m; right < n; right++) {
            int old_index = s.charAt(right - m) - 'a';
            window[old_index]--;
            int new_index = s.charAt(right) - 'a';
            window[new_index]++;
            // Java 数组比较内容用 Arrays.equals，不能用 ==
            if (Arrays.equals(window, target)) {
                ans.add(right - m + 1);
            }
        }
        return ans;
    }
}
