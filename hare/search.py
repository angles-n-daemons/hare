from dataclasses import dataclass
from typing import List

from trie import Trie, TrieNode


@dataclass
class Match:
    start: int
    end: int
    value: str
    matching: str
    distance: int


@dataclass
class MatchResult:
    length: int
    value: str
    matching: str
    distance: int


class KeywordFinder:
    def __init__(self):
        self.trie = Trie()

    def search(self, text) -> List[Match]:
        matches = {}

        for i in range(len(text)):
            for result in self._fuzzy_search_partial(text[i:]):
                existing_match = matches.get(result.value, None)

                if existing_match is None or existing_match.distance > result.distance:
                    matches[result.value] = Match(
                        start=i,
                        end=i+result.length,
                        value=result.value,
                        matching=result.matching,
                        distance=result.distance,
                    )
        return matches.values()

    def _fuzzy_search_partial(self, text: str, allowed_error: int = 1):
        matches = []
        search_count = 0
        for child in self.trie.root.children.values():
            new_matches, new_search_count = recursive_edit_distance_search(
                allowed_error,
                text,
                child,
                list(range(len(text) + 1)),
            )
            matches += new_matches
            search_count += new_search_count

        # print(f'search on "{text}" hit {search_count} nodes')
        return matches


def recursive_edit_distance_search(
    allowed_error: int,
    search_string: str,
    node: TrieNode,
    row: List[int],
) -> List[TrieNode]:
    new_row = [row[0] + 1]
    min_dist = row[0] + 1
    min_index = 0

    for i, char in enumerate(search_string):
        score_options = [
            row[i],
            row[i+1],
            new_row[i],
        ]
        modifier = 0 if node.char == char else 1

        score = min(score_options) + modifier
        if score < min_dist:
            min_dist = score
            min_index = i + 1

        new_row.append(score)

    values = []
    if min_dist <= allowed_error:
        if node.in_vocab:
            # add the index value of the word end in the search string
            values.append(MatchResult(
                length=min_index,
                value=node.value(),
                matching=search_string[0:min_index],
                distance=min_dist,
            ))

    node_count = 1
    if min_dist <= allowed_error:
        for child in node.children.values():
            new_values, new_node_count = recursive_edit_distance_search(
                allowed_error,
                search_string,
                child,
                new_row,
            )
            values += new_values
            node_count += new_node_count

    return values, node_count
