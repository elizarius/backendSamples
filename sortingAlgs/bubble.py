#!/usr/bin/env python3

def print_list(num_list):
    print(num_list)

def bubble_sort(arr):
    n = len(arr)
  
    # Traverse through all array elements
    for i in range(n):
  
        # Last i elements are already in place
        for j in range(0, n-i-1):
  
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        print('UnSorted till index: ', n-i-1)
        print_list(arr)



num_list = [10, 11, 5, 7, 2, 8, 3, 9, 6, 1, 4]
print('\n***** Bubble sorting by own function ***** \n')
bubble_sort(num_list)
