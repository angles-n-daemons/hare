from search import KeywordFinder

finder = KeywordFinder()
for keyword in ['coffee', 'water bottle', 'wallet']:
    finder.trie.add(keyword)

# search with misspellings
print(finder.search('have you seen my walket recently?'))

# search with missing space
print(finder.search('i brought my waterbottle to the gym'))
