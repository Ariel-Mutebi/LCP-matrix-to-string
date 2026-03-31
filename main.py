from collections import defaultdict
from string import ascii_lowercase


def find_components(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Returns a list mapping each node to its component representative."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int):
        parent[find(x)] = find(y)

    for a, b in edges:
        union(a, b)

    return [find(i) for i in range(n)]


def reconstruct_matrix(s: str) -> list[list[int]]:
    n = len(s)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            k = 0
            while i + k < n and j + k < n and s[i + k] == s[j + k]:
                k += 1
            matrix[i][j] = matrix[j][i] = k
    return matrix


class Solution:
    def findTheString(self, lcp: list[list[int]]) -> str:
        n = len(lcp)

        # Collect union constraints: lcp[i][j] >= k means char[i+k] == char[j+k]
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(lcp[i][j]):
                    if i + k >= n or j + k >= n:
                        return ""  # lcp value is out of range
                    edges.append((i + k, j + k))

        # Find connected components; assign letters in order of first appearance
        component = find_components(n, edges)
        rep_to_letter: dict[int, str] = {}
        letter_idx = 0
        result = []

        for i in range(n):
            rep = component[i]
            if rep not in rep_to_letter:
                if letter_idx >= 26:
                    return ""  # more unique chars than alphabet allows
                rep_to_letter[rep] = ascii_lowercase[letter_idx]
                letter_idx += 1
            result.append(rep_to_letter[rep])

        word = "".join(result)
        return word if reconstruct_matrix(word) == lcp else ""