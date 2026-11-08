# -*- coding: utf-8 -*-
"""
常用算法工具库
==============
包含以下经典算法实现：
    1. 快速排序（Quick Sort）
    2. 二分查找（Binary Search）
    3. 冒泡排序（Bubble Sort）
    4. 归并排序（Merge Sort）

每个算法均附带中文注释，说明其原理、时间复杂度与空间复杂度。
"""


# ---------------------------------------------------------------------------
# 1. 快速排序（Quick Sort）
# ---------------------------------------------------------------------------
def quick_sort(arr):
    """
    快速排序（原地排序版本，返回新的已排序列表，不修改原列表）。

    原理：
        采用"分治法"（Divide and Conquer）思想：
        1. 从数组中选取一个元素作为"基准"（pivot，这里取中间位置的元素）；
        2. 分区（partition）：将小于基准的元素移到左边，大于基准的移到右边；
        3. 对左右两个子区间递归执行上述过程，直到区间长度为 1。

    时间复杂度：
        - 平均情况：O(n log n)
        - 最坏情况：O(n^2)（每次分区都极不平衡，例如已排序数组且固定取首元素为基准）
    空间复杂度：
        - O(log n)（递归调用栈的深度，平均情况）
    稳定性：
        - 不稳定（相等元素的相对顺序可能在交换后改变）
    """
    # 复制一份数据，避免修改调用方传入的原始列表
    data = list(arr)
    _quick_sort_inplace(data, 0, len(data) - 1)
    return data


def _quick_sort_inplace(data, left, right):
    """快速排序的递归主体：对 data[left..right] 区间原地排序。"""
    # 递归终止条件：区间长度小于等于 1 时无序无需排序
    if left >= right:
        return

    # 分区操作：选定基准并把数组划分为两部分，返回基准最终所在的下标
    pivot_index = _partition(data, left, right)

    # 递归排序基准左侧的子区间
    _quick_sort_inplace(data, left, pivot_index - 1)
    # 递归排序基准右侧的子区间
    _quick_sort_inplace(data, pivot_index + 1, right)


def _partition(data, left, right):
    """
    Lomuto 分区方案：
    取区间中间位置的元素作为基准（避免在近乎有序的数组上退化），
    将其交换到区间末尾，然后遍历区间，把所有小于基准的元素交换到左边。
    返回基准元素最终所在的下标。
    """
    # ---------- 第 1 步：选基准并放到末尾 ----------
    # 取区间中间位置的元素作为基准（pivot）。
    # 但 Lomuto 方案要求基准必须在区间末尾，所以先把基准和 data[right] 交换，
    # 这样后面遍历时基准不会碍事，最后再放回正确位置即可。
    mid = (left + right) // 2
    data[mid], data[right] = data[right], data[mid]
    pivot = data[right]  # 此时基准元素存放在区间末尾

    # ---------- 第 2 步：一趟扫描，把小于基准的元素全部挪到左边 ----------
    # 整个区间被隐式地分成三个区域（基准所在的末尾位置除外）：
    #   [left .. store_index-1]  已确认"小于基准"的元素区
    #   [store_index .. i-1]     已确认"大于等于基准"的元素区
    #   [i .. right-1]           还没检查的元素
    # store_index 的含义：下一个"小于基准的元素"应该放置的位置。
    store_index = left  # 一开始"小于区"为空，所以指向区间最左端
    for i in range(left, right):  # 注意：不含 right，因为末尾是基准本身
        if data[i] < pivot:
            # data[i] 小于基准，但它当前位于"大于等于区"里，位置不对。
            # 把它与 store_index 处的元素交换：
            #   - data[i] 进入左边的"小于区"（放到 store_index 位置）；
            #   - 原来 store_index 处的元素（必然 >= 基准）换到 i 位置，
            #     归入右边的"大于等于区"，不影响正确性。
            data[store_index], data[i] = data[i], data[store_index]
            store_index += 1  # "小于区"扩大一格，下一个小数放在新位置
        # 如果 data[i] >= 基准：什么都不做，i 继续前进，
        # 它自然留在"大于等于区"中。

    # ---------- 第 3 步：把基准放回分界点 ----------
    # 扫描结束后：store_index 左边的元素全部 < 基准，
    # [store_index, right-1] 的元素全部 >= 基准，基准还暂存在 right。
    # 把基准与 store_index 处的元素（第一个 >= 基准的元素）交换，
    # 基准就落到了最终位置：左边都 <= 它，右边都 > 它。
    data[store_index], data[right] = data[right], data[store_index]

    # 返回基准的最终下标，供调用方据此对左右两个子区间分别递归排序
    return store_index


# ---------------------------------------------------------------------------
# 2. 二分查找（Binary Search）
# ---------------------------------------------------------------------------
def binary_search(arr, target):
    """
    二分查找（迭代版本）。

    前提条件：
        输入数组 arr 必须是"已按升序排列"的有序数组。

    原理：
        利用有序性，每次将搜索区间对半缩小：
        1. 取区间中点 mid，比较 arr[mid] 与目标值 target；
        2. 若相等，查找成功，返回下标；
        3. 若 arr[mid] < target，说明目标只可能在右半区间，令 left = mid + 1；
        4. 若 arr[mid] > target，说明目标只可能在左半区间，令 right = mid - 1；
        5. 重复上述过程，直到找到目标或区间为空（left > right）。

    时间复杂度：
        - 最好情况：O(1)（中点恰好命中目标）
        - 平均 / 最坏情况：O(log n)（每轮比较后搜索规模减半）
    空间复杂度：
        - O(1)（迭代实现，只使用常数个指针变量）
    """
    left, right = 0, len(arr) - 1  # 搜索区间为闭区间 [left, right]

    while left <= right:
        # 用位运算求中点，等价于 (left + right) // 2，可避免大数相加溢出（在其他语言中更重要）
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid            # 命中目标，返回其下标
        elif arr[mid] < target:
            left = mid + 1        # 目标在右半区间
        else:
            right = mid - 1       # 目标在左半区间

    return -1  # 区间为空仍未找到，返回 -1 表示目标不存在


# ---------------------------------------------------------------------------
# 3. 冒泡排序（Bubble Sort）
# ---------------------------------------------------------------------------
def bubble_sort(arr):
    """
    冒泡排序（返回新的已排序列表，不修改原列表）。

    原理：
        重复地遍历数组，每次比较相邻的两个元素，
        如果顺序错误（前者大于后者）就交换它们。
        每一轮遍历都会把当前未排序部分中的"最大值"像气泡一样
        "浮"到数组末尾，因此称为冒泡排序。
        优化：若某一轮遍历中没有发生任何交换，说明数组已经有序，
        可以提前结束排序。

    时间复杂度：
        - 最好情况：O(n)（数组本身已经有序，一轮扫描后无交换即退出）
        - 平均 / 最坏情况：O(n^2)（双重循环）
    空间复杂度：
        - O(1)（原地排序，只用到常数个临时变量）
    稳定性：
        - 稳定（相等元素不会交换，相对顺序保持不变）
    """
    data = list(arr)  # 复制一份，避免修改原始列表
    n = len(data)

    for i in range(n - 1):
        swapped = False  # 标记本轮是否发生过交换

        # 每轮结束后，末尾的 i 个元素已经就位，无需再比较
        for j in range(n - 1 - i):
            if data[j] > data[j + 1]:
                # 相邻元素顺序错误，交换它们
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True

        # 本轮没有任何交换，说明数组已经有序，提前退出
        if not swapped:
            break

    return data


# ---------------------------------------------------------------------------
# 4. 归并排序（Merge Sort）
# ---------------------------------------------------------------------------
def merge_sort(arr):
    """
    归并排序（返回新的已排序列表，不修改原列表）。

    原理：
        同样采用"分治法"（Divide and Conquer）思想，但策略与快排相反——
        快排是"先分区、后递归"，归并是"先递归、后合并"：
        1. 分解（divide）：把数组从中间一分为二，得到左右两个子数组；
        2. 递归（conquer）：分别对左右子数组递归执行归并排序；
        3. 合并（merge）：把两个"各自已有序"的子数组合成一个有序数组。
           合并时利用两个子数组已有序的性质，用双指针从头比较，
           每次把较小的元素放入结果，直到所有元素归位。
        递归终止条件：子数组长度小于等于 1，天然有序，无需再分。

    时间复杂度：
        - 最好 / 平均 / 最坏情况均为 O(n log n)
          （每层合并共处理 n 个元素，递归深度为 log n，与数据分布无关）
    空间复杂度：
        - O(n)（合并过程需要临时数组存放结果）
    稳定性：
        - 稳定（合并时相等元素优先取左侧的，相对顺序保持不变）
    """
    data = list(arr)  # 复制一份，避免修改调用方传入的原始列表

    # 递归终止：长度为 0 或 1 的数组已经有序
    if len(data) <= 1:
        return data

    # 1. 分解：从中间位置把数组切成左右两半
    mid = len(data) // 2
    left_half = merge_sort(data[:mid])    # 2. 递归：左半部分排好序
    right_half = merge_sort(data[mid:])   # 2. 递归：右半部分排好序

    # 3. 合并：把两个有序子数组归并成一个有序数组
    return _merge(left_half, right_half)


def _merge(left, right):
    """
    合并两个升序数组，返回一个新的升序数组。

    双指针 i、j 分别指向 left 和 right 的当前位置：
    每轮比较两个指针所指的元素，把较小者（相等时取左侧，保证稳定性）
    追加到结果数组，并移动对应指针；
    某一侧耗尽后，把另一侧剩余元素直接拼到结果末尾。
    """
    result = []
    i, j = 0, 0  # i 指向 left 的当前元素，j 指向 right 的当前元素

    # 两侧都还有元素时，逐个比较、取较小者放入结果
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # "<=" 中的等号使相等元素优先取左侧，保证排序稳定
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 把尚未耗尽的一侧剩余元素全部追加到末尾
    # （剩余元素本身已有序，且都不小于 result 中已有元素）
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# 简单自测
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample = [64, 25, 12, 22, 11, 90, 1, 55, 33]
    print("原始数组:        ", sample)
    print("快速排序结果:    ", quick_sort(sample))
    print("冒泡排序结果:    ", bubble_sort(sample))
    print("归并排序结果:    ", merge_sort(sample))

    sorted_arr = quick_sort(sample)
    target = 33
    index = binary_search(sorted_arr, target)
    print(f"二分查找 {target}:  下标 = {index}")

    missing = binary_search(sorted_arr, 100)
    print(f"二分查找 100: 下标 = {missing}（-1 表示不存在）")
