n = 5


def hourglass_pattern(n: int) -> list[list[str]]:
    """Return an hourglass pattern as a list of lists where each inner list
    contains a single string (the row).

    The function returns 2*n-1 rows. Example for n=3 (rows = 5):
      ['******',  # i=0: 2*n stars
       '**.**',
       '*...*',  # middle row
       '**.**',
       '******']

    Only odd `n` are supported. The width of every row is 2*n - 1.
    """

    if n % 2 == 0:
        raise ValueError("n must be odd")

    pattern: list[list[str]] = []

    # build top half including middle row (i from 0 to n-1)
    for i in range(n-1):
        left_stars = n - i
        middle_dots = 2 * i - 1

        if middle_dots > 0:
            row = '*' * left_stars + '.' * middle_dots + '*' * left_stars
        else:
            # when middle_dots <= 0 we just have the two star blocks
            row = '*' * left_stars + '*' * left_stars

        pattern.append([row])

    # mirror the top half except the middle row to form the bottom half
    for i in range(n - 2, -1, -1):
        # append a copy of the row as a new inner list
        pattern.append([pattern[i][0]])

    return pattern


print(hourglass_pattern(5))



