import sys

sys.setrecursionlimit(10**5)

m = 0

n = 0

mat = [0 * 10 for _ in range (0, 10)]
dp = {}

def solve():

    def is_valid(i, j):
        if i < 0 or j < 0 or i >= n or j >= m:
            return False
        if mat[i][j] == -1:
            return False
        return True

    def find_max_path(i, j, x):

        y = i + j - x

        if not is_valid(i,j) or not is_valid(x,y):
            return -float('inf')

        if i == n-1 and j == m-1 and x == n-1 and y == m-1:
            if mat[i][j] == 1:
                return 1
            else:
                return 0
            
        state = (i,j,x)
        
        if state in dp:            
            return dp[state]
        
        curr = 0

        if i == x and j == y:
            if mat[i][j] == 1:
                curr = 1
        
        else:
            if mat[i][j] == 1:
                curr += 1
            if mat[x][y] == 1:
                curr += 1
        
        op1 = find_max_path(i+1, j, x +1)
        op2 = find_max_path(i, j+1, x)
        op3 = find_max_path(i+1, j, x)
        op4 = find_max_path(i, j+1, x+1)

        ans = curr + max(op1,op2,op3,op4)

        dp[state] = ans
        return ans
    
    ans = find_max_path(0,0,0)
    print(ans if ans >=0 else -1)

if __name__ == '__main__':
    solve()
    

