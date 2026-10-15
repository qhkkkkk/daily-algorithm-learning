#include <stdlib.h>

typedef struct {
    int key;
    int index;
    int used;  /* 单独标记占用，因为 0 也是合法的值和下标 */
} HashNode;

static int hashIndex(int key, int capacity) {
    int index = key % capacity;
    return index < 0 ? index + capacity : index;
}

/* 本实现面向本题约束：numsSize <= 10000，数值和 target 在 +/-10^9 内。 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    *returnSize = 0;
    int capacity = 2 * numsSize + 1;  /* 留足空槽，线性探测能遇到未用位置 */
    HashNode* table = calloc((size_t)capacity, sizeof(*table));
    if (table == NULL) return NULL;

    for (int i = 0; i < numsSize; ++i) {
        int need = target - nums[i];
        int slot = hashIndex(need, capacity);

        /* 冲突只表示槽位相同，必须继续比较原始 key。 */
        while (table[slot].used) {
            if (table[slot].key == need) {
                int* result = malloc(2 * sizeof(*result));
                if (result == NULL) {
                    free(table);
                    return NULL;
                }
                result[0] = table[slot].index;
                result[1] = i;
                *returnSize = 2;
                free(table);  /* 哈希表不再需要；结果留给调用方释放 */
                return result;
            }
            slot = (slot + 1) % capacity;
        }

        /* 先查后存。重复 key 可更新下标，不需要增加一个重复槽位。 */
        slot = hashIndex(nums[i], capacity);
        while (table[slot].used && table[slot].key != nums[i]) {
            slot = (slot + 1) % capacity;
        }
        table[slot].key = nums[i];
        table[slot].index = i;
        table[slot].used = 1;
    }
    free(table);
    return NULL;
}
