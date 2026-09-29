
locations = [0,2,1,2,1,3,1]

def min_fountains(locations: list[int]) -> int:
    n = len(locations)
    if n == 0:
        return 0

    max_reach = [0] * n

    for i in range(n):
        left = max(0, i - locations[i])
        right = min(n - 1, i + locations[i])
        max_reach[left] = max(max_reach[left], right)

    activated = 0
    current_end = 0
    furthest = 0

    for i in range(n):
        furthest = max(furthest, max_reach[i])

        if i == current_end:
            if furthest <= i:
                return -1
            activated += 1
            current_end = furthest
            if current_end >= n - 1:
                return activated

    return activated


print(min_fountains(locations))
