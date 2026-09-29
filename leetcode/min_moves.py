nums = [1,3,7,2,9,2]

def solve_min_moves(nums: list[int]) -> int
    sum = 0
    i = nums.index(min(nums))

    for j in range(len(nums)):

        if i == j:
            continue
        else:
            s = s + nums[j] - nums[i]

    return s

n = int(input())
numbers = []
for i in range (n):
    numbers.append(int(input))

