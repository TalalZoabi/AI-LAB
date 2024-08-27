
import time

# QuickSort implementation that counts comparisons and measures time
def quicksort(arr):
    comparisons = [0]  # List to hold the comparison count, so it's mutable
    start_time = time.perf_counter()  # Start timing

    def _quicksort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if count_comparison(x < pivot)]
        middle = [x for x in arr if count_comparison(x == pivot)]
        right = [x for x in arr if count_comparison(x > pivot)]
        return _quicksort(left) + middle + _quicksort(right)

    def count_comparison(condition):
        comparisons[0] += 1
        return condition

    sorted_array = _quicksort(arr)
    end_time = time.perf_counter()  # End timing
    time_taken_ms = (end_time - start_time) * 1000  # Convert to milliseconds

    return sorted_array, comparisons[0], time_taken_ms

