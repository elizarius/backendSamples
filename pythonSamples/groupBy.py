
from itertools import groupby

# Example usage of groupby iterator
nums = [1,1,2,2,3,4,4,5]
for key, val in groupby(nums):
    print(key, list(val))
