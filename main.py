# I decided to John Carmack up and not ask AI this time.
from collections import defaultdict

def reconstruct_matrix(s: str) -> list[list[int]]:
    n = len(s)
    end = n - 1
    matrix: list[list[int | None]] = [[None for _ in range(n)] for _ in range(n)]

    for i in range(0, end):
        ss1 = s[i:end]
        for j in range(0, end):
            if not matrix[i][j] is None:
                continue

            ss2 = s[j:end]

            if len(ss1) > len(ss2):
                ss1, ss2 = ss2, ss1

            k = 0

            while k < len(ss1) - 1:
                if not ss1[k] == ss2[k]:
                    break
                k += 1

            matrix[i][j] = k
            # An LCP matrix is symmetrical along the diagonal line
            # from top left to bottom right (line where i == j).
            if not i == j:
                matrix[j][i] = k

    return matrix


def generate_equal_char_indexes(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)

    # I decided to use an undirected adjacency list to represent indexes of
    # equal characters, where a path is a sequence of indexes of equal characters.
    indexes_of_equal_chars = defaultdict(list)

    # These ranges will be "sublimated" into individual indexes as more
    # is learned from iterating through the "signal" part of the matrix.
    # The key of the list of RangePairs is the number of characters in each range.
    Range = tuple[int, int]
    RangePair = tuple[Range, Range]
    ranges_of_equal_chars: dict[int, list[RangePair]] = defaultdict(list)

    # The "signal" part of the matrix is the top-right half above the diagonal line.
    # The values on the diagonal line are noise, and the bottom-left is a reflection.
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            lcp = matrix[i][j]
            if lcp <= 0:
                continue  # also noise

            if lcp == 1:
                indexes_of_equal_chars[i].append(j)
                indexes_of_equal_chars[j].append(i)

                # sublimate relevant two-character ranges
                if ranges_of_equal_chars[2]:
                    for pair_of_range_tuples in ranges_of_equal_chars[2]:
                        (a, b), (c, d) = pair_of_range_tuples
                        sublimated = False

                        if i == a and j == c:
                            indexes_of_equal_chars[b].append(d)
                            indexes_of_equal_chars[d].append(b)
                            sublimated = True
                        elif i == b and j == d:
                            indexes_of_equal_chars[a].append(c)
                            indexes_of_equal_chars[c].append(a)
                            sublimated = True

                        if sublimated:
                            ranges_of_equal_chars[2].remove(pair_of_range_tuples)
            else:
                if lcp > n - i or lcp > n - j:
                    raise ValueError("LCP out of range")

                new_ranges = ((i, i + lcp - 1), (j, j + lcp - 1))
                ranges_of_equal_chars[lcp].append(new_ranges)

                # sublimate relevant ranges of +1 size
                if (lcp + 1) in ranges_of_equal_chars:
                    for pair_of_range_tuples in ranges_of_equal_chars[lcp + 1]:
                        (a, b), (c, d) = pair_of_range_tuples
                        (e, f), (g, h) = new_ranges  # singing the alphabet song
                        sublimated = False

                        if a == e and c == g:
                            indexes_of_equal_chars[b].append(d)
                            indexes_of_equal_chars[d].append(b)
                            sublimated = True
                        elif b == f and d == h:
                            indexes_of_equal_chars[a].append(c)
                            indexes_of_equal_chars[c].append(a)
                            sublimated = True

                        if sublimated:
                            ranges_of_equal_chars[lcp + 1].remove(pair_of_range_tuples)

    def find_components(graph: dict[int, list[int]]) -> list[list[int]]:
        visited: set[int] = set()
        components: list[list[int]] = []

        def dfs(node: int, component: list[int]):
            visited.add(node)
            component.append(node)

            for neighbour in graph[node]:
                if neighbour not in visited:
                    dfs(neighbour, component)

        for node in graph:
            if node not in visited:
                component = []
                dfs(node, component)
                components.append(component)

        return components

    return find_components(indexes_of_equal_chars)

print(generate_equal_char_indexes([[4,0,2,0],[0,3,0,1],[2,0,2,0],[0,1,0,1]]))
print(generate_equal_char_indexes([[4, 3, 2, 1], [3, 3, 2, 1], [2, 2, 2, 1], [1, 1, 1, 1]]))


class Solution:
    def findTheString(self, matrix: list[list[int]]) -> str:
        pass
