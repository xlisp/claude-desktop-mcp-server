#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速排序算法实现集合
包含多种快速排序的实现方式
"""

import random
import time
from typing import List, Callable


def quicksort_basic(arr: List[int]) -> List[int]:
    """
    基础快速排序实现
    使用递归方式，选择第一个元素作为基准
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]
    
    return quicksort_basic(left) + [pivot] + quicksort_basic(right)


def quicksort_inplace(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    原地快速排序实现
    直接在原数组上进行排序，节省空间
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # 分区操作
        pi = partition(arr, low, high)
        
        # 递归排序左右子数组
        quicksort_inplace(arr, low, pi - 1)
        quicksort_inplace(arr, pi + 1, high)


def partition(arr: List[int], low: int, high: int) -> int:
    """
    分区函数，用于原地快速排序
    选择最后一个元素作为基准
    """
    pivot = arr[high]
    i = low - 1  # 较小元素的索引
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_random_pivot(arr: List[int]) -> List[int]:
    """
    随机选择基准的快速排序
    通过随机化基准选择来避免最坏情况
    """
    if len(arr) <= 1:
        return arr
    
    # 随机选择基准
    pivot_index = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_index]
    
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort_random_pivot(left) + middle + quicksort_random_pivot(right)


def quicksort_three_way(arr: List[int]) -> List[int]:
    """
    三路快速排序
    适合处理有大量重复元素的数组
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    
    return quicksort_three_way(less) + equal + quicksort_three_way(greater)


def quicksort_iterative(arr: List[int]) -> List[int]:
    """
    迭代版本的快速排序
    使用栈来模拟递归过程
    """
    if len(arr) <= 1:
        return arr
    
    arr = arr.copy()  # 创建副本避免修改原数组
    stack = [(0, len(arr) - 1)]
    
    while stack:
        low, high = stack.pop()
        
        if low < high:
            pi = partition(arr, low, high)
            stack.append((low, pi - 1))
            stack.append((pi + 1, high))
    
    return arr


def median_of_three(arr: List[int], low: int, high: int) -> int:
    """
    三数取中法选择基准
    """
    mid = (low + high) // 2
    
    if arr[mid] < arr[low]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[high] < arr[low]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[high] < arr[mid]:
        arr[mid], arr[high] = arr[high], arr[mid]
    
    return mid


def quicksort_median_pivot(arr: List[int]) -> List[int]:
    """
    使用三数取中法选择基准的快速排序
    """
    if len(arr) <= 1:
        return arr
    
    arr = arr.copy()
    quicksort_median_inplace(arr, 0, len(arr) - 1)
    return arr


def quicksort_median_inplace(arr: List[int], low: int, high: int) -> None:
    """
    使用三数取中法的原地快速排序
    """
    if low < high:
        # 三数取中选择基准
        median_idx = median_of_three(arr, low, high)
        arr[median_idx], arr[high] = arr[high], arr[median_idx]
        
        pi = partition(arr, low, high)
        quicksort_median_inplace(arr, low, pi - 1)
        quicksort_median_inplace(arr, pi + 1, high)


def benchmark_algorithms():
    """
    性能测试函数
    比较不同快速排序算法的性能
    """
    algorithms = {
        "基础快速排序": quicksort_basic,
        "随机基准快速排序": quicksort_random_pivot,
        "三路快速排序": quicksort_three_way,
        "迭代快速排序": quicksort_iterative,
        "三数取中快速排序": quicksort_median_pivot
    }
    
    # 测试数据
    test_sizes = [100, 1000, 5000]
    
    for size in test_sizes:
        print(f"\n=== 测试数组大小: {size} ===")
        
        # 生成随机数组
        test_array = [random.randint(1, 1000) for _ in range(size)]
        
        for name, algorithm in algorithms.items():
            arr_copy = test_array.copy()
            
            start_time = time.time()
            
            if name == "原地快速排序":
                quicksort_inplace(arr_copy)
                result = arr_copy
            else:
                result = algorithm(arr_copy)
            
            end_time = time.time()
            
            # 验证排序结果
            is_sorted = all(result[i] <= result[i+1] for i in range(len(result)-1))
            
            print(f"{name}: {end_time - start_time:.6f}秒 - {'✓' if is_sorted else '✗'}")


def demo():
    """
    演示函数
    展示各种快速排序算法的使用
    """
    print("快速排序算法演示")
    print("=" * 50)
    
    # 测试数组
    test_array = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42]
    print(f"原始数组: {test_array}")
    print()
    
    # 测试各种算法
    algorithms = [
        ("基础快速排序", quicksort_basic),
        ("随机基准快速排序", quicksort_random_pivot),
        ("三路快速排序", quicksort_three_way),
        ("迭代快速排序", quicksort_iterative),
        ("三数取中快速排序", quicksort_median_pivot)
    ]
    
    for name, algorithm in algorithms:
        result = algorithm(test_array.copy())
        print(f"{name}: {result}")
    
    # 原地排序演示
    inplace_array = test_array.copy()
    quicksort_inplace(inplace_array)
    print(f"原地快速排序: {inplace_array}")
    
    print("\n" + "=" * 50)
    print("性能测试:")
    benchmark_algorithms()


if __name__ == "__main__":
    demo()
