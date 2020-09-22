def _longest_common_subsequence(s1: str, s2: str) -> int:
    """
    Let m and n be the lengths of two strings.
    Build L[m+1][n+1] from the bottom up.
    Note: L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1]

    Runtime: O(mn)
    Space Complexity: O(mn)
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


def longest_common_subsequence(s1: str, s2: str) -> int:
    """
    Space-optimized version of LCS.
    Let m and n be the lengths of two strings.

    Runtime: O(mn)
    Space Complexity: O(min(m, n))
    """
    m, n = len(s1), len(s2)
    if m < n:
        s1, s2 = s2, s1

    L = [0] * (n + 1)
    for a in s1:
        prev_row, prev_row_col = 0, 0
        for j, b in enumerate(s2):
            prev_row, prev_row_col = L[j + 1], prev_row
            if a == b:
                L[j + 1] = prev_row_col + 1
            else:
                L[j + 1] = max(L[j], prev_row)
    return L[-1]
