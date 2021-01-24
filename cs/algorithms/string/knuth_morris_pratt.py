from __future__ import annotations


def kmp_string_match(needle: str, haystack: str) -> int | None:
    """
    The Knuth-Morris-Pratt algorithm finds an occurrence of the specified needle string
    in the haystack string. To do this, we compute a failure table. Next, we iterate
    across the string, keeping track of a candidate start point and length matched so
    far. Whenever a match occurs, we update the length of the match we've made. On a
    failure, we update these values by trying to preserve the maximum proper border
    of the string we were able to manage by that point.

    kmp_string_match("0101", "0011001011") == 5
    """
    # Create the failure table, which for length zero is None.
    fail = [0]
    for i, ch in enumerate(needle):
        # Keep track of the size of the subproblem we're dealing with, which
        # starts off using the first i characters of the string.
        j = i
        while True:
            # If j hits zero, the recursion says that the resulting value is
            # zero since we're looking for the LPB of a single-character string.
            if j == 0:
                fail.append(0)
                break

            # Otherwise, if the character one step after the LPB matches the
            # next character in the sequence, then we can extend the LPB by one
            # character to get an LPB for the whole sequence.
            if needle[fail[j]] == ch:
                fail.append(fail[j] + 1)
                break

            # Finally, if neither of these hold, then we need to reduce the
            # subproblem to the LPB of the LPB.
            j = fail[j]

    # Keep track of the start index and next match position, both of which
    # start at zero since our candidate match is at the beginning and is trying
    # to match the first character.
    index, match = 0, 0
    while index + match < len(haystack):
        # If the current char matches the expected char, bump up the match index.
        if haystack[index + match] == needle[match]:
            match += 1
            if match == len(needle):
                return index

        # Otherwise, we need to look at the fail table to determine what to do next.
        else:
            # If we couldn't match the first character, then just advance the
            # start index.  We need to try again.
            if match == 0:
                index += 1

            # Otherwise, see how much we need to skip forward before we have
            # another feasible match.
            else:
                index += match - fail[match]
                match = fail[match]
    return None
