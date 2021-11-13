def StairCase(n, X):
    if n == 0 or n == 1:
        return 1
    dp = [0] * (n+1)
    dp[0] = 1
    for i in range(1, n+1):
        for j in X:
            if i - j >= 0:
                dp[i] += dp[i-j]
    return dp[-1]

n = int(input())
x = list(map(int, input().split())) 
print(StairCase(n,x))