#!/usr/bin/env python3

def print_list(num_list):
    print(num_list)

def selection_sort(original_list):
    length = len(original_list)
    for i in range(length):
        min_value_index = i
        for j in range(i + 1, length):
            if original_list[min_value_index] > original_list[j]:
                min_value_index = j
        original_list[i], original_list[min_value_index] = original_list[min_value_index], original_list[i]
        print('Sorted till index: ', i)
        print_list(original_list)
    print('Sorted list: ')
    print_list(original_list)




num_list = [10, 11, 5, 7, 2, 8, 3, 9, 6, 1, 4]
print('\n***** Selection sorting by own function ***** \n')
selection_sort(num_list)

print('\n***** Selection sorting by SORTED ***** ')
num_list = [10, 11, 5, 7, 2, 8, 3, 9, 6, 1, 4]
print(sorted(num_list))

print('\n***** Selection sorting by list.sort ***** ')
num_list = [10, 11, 5, 7, 2, 8, 3, 9, 6, 1, 4]
num_list.sort()
print(num_list)





