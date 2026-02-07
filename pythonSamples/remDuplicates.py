def removeDuplicates(nums: list[int]) -> int:
    myset = set(nums)
    nums = list(myset)
    return len(nums), nums

nums = [1,1,2,2,3,4,4,5]
k,zz = removeDuplicates(nums)
print(k, zz)