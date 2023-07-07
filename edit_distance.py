import concurrent.futures
import numpy as np

# case insensitive edit distance
def edit_distance_optimized_np(s1: str, s2: str):
    s1 = s1.upper()
    s2 = s2.upper()

    m, n = len(s1), len(s2)
    matrix = np.zeros((m+1, n+1))

    for i in range(m+1):
        matrix[i, 0] = i
    for j in range(n+1):
        matrix[0, j] = j

    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                matrix[i, j] = matrix[i-1, j-1]
            else:
                matrix[i, j] = min(
                    matrix[i-1, j] + 1,      # deletion
                    matrix[i, j-1] + 1,      # insertion
                    matrix[i-1, j-1] + 1     # substitution
                )

    return matrix[m, n]

def compare_to_string(possible_matches, source_word: str, max_edit_distance: int = 2) -> dict:
    result = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_str = {executor.submit(edit_distance_optimized_np, s, source_word): s for s in possible_matches}
        for future in concurrent.futures.as_completed(future_to_str):
            s = future_to_str[future]
            try:
                edit_distance = future.result()
                if edit_distance <= max_edit_distance:
                    result[s] = edit_distance
            except Exception as exc:
                print('%r generated an exception: %s' % (s, exc))
    return result
