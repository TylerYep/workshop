def longest_common_subsequence(s1: str, s2: str) -> int:
    """
    Build L[m+1][n+1] from the bottom up.
    Note: L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1]
    """
    m, n = len(s1), len(s2)
    L = [[0] * (n + 1) for i in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L[m][n]
