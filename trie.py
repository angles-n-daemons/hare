from typing import List


class TrieNode:
    """
    Our trie node implementation. Very basic. but does the job
    """

    def __init__(self, char: str, parent: any = None):
        self.char = char
        self.children = {}
        self.parent = parent
        self.in_vocab = False

    def value(self):
        node = self

        value_list = []
        while node is not None:
            value_list.append(node.char)
            node = node.parent
        return ''.join(reversed(value_list))


class Trie:
    def __init__(self):
        self.root = TrieNode('')
        self.node_count = 1

    def add(self, phrase: str):
        """
        Adding a word in the trie structure
        """
        node = self.root
        for char in phrase:
            if char not in node.children:
                new_node = TrieNode(char, node)
                node.children[char] = new_node
                self.node_count += 1

            node = node.children[char]

        node.in_vocab = True

    def search(self, prefix: str) -> List[str]:
        if not prefix:
            raise Exception('give me a prefix man')

        node = self.root
        for char in prefix:
            if char not in node.children:
                return None

            node = node.children[char]

        candidates = [node]
        matches = []
        while candidates:
            node = candidates.pop()
            for child in node.children.values():
                candidates.append(child)
            if node.in_vocab:
                matches.append(node)

        return [match.value() for match in matches]
