import os
import time

from search import KeywordFinder

from fuzzysearch import find_near_matches

import tqdm

filename = '/tmp/english-words/words.txt'

kwsmall = KeywordFinder()
kwmedium = KeywordFinder()
kwlarge = KeywordFinder()

vocabsmall = []
vocabmedium = []
vocablarge = []

with tqdm.tqdm(os.path.getsize(filename)) as pbar:
    with open(filename, 'r') as f:
        count = 0
        for line in f:
            line = line.replace('\n', '')
            pbar.update(len(line))

            if count < 25:
                kwsmall.trie.add(line)
                vocabsmall.append(line)

            if count < 2000:
                kwmedium.trie.add(line)
                vocabmedium.append(line)

            kwlarge.trie.add(line)
            vocablarge.append(line)

            count += 1


short_search_phrase = 'i caught a phone with my ear'
medium_search_phrase = 'Only way would be to write a small amount of data to a tempfile in your chosen encoding, and then measure that tempfile size, calculate the character-to-byte ratio. I could be wrong, but this is the only way to ensure it works in a platform independent way, and at all times'
long_search_phrase = """
Note: This article has been updated after bug fixes were done the day after I reported this on the mailing list. Please refer to the update at the bottom.
A well known method for indexing and retrieval of full text is the suffix tree, otherwise known as a patricia trie or radix trie. Among the many potential applications of the trie and suffix trie/tree they are especially useful in bioinformatics for efficient searching with mismatches. Being in a proteomics lab, suffix tries are a perfect data structure for indexing and searching proteomes today. Desktop computers can be equipped with 32gb of memory for little cost, which happens to be just enough to store a fast index of the entire proteome in memory. This allows for a one-time indexing and subsequent constant time searches.
Since I use mostly python in my scientific work, I set out to find a python library to use to create a suffix trie for my proteome. Pure python implementations of suffix tries are not memory-efficient enough, so most trie libraries are C/C++ with python wrappers. I recently came across a blog of several advanced data structure implementaions in python and decided to take the time to replace my suffix array implementation with a suffix trie. Here is a collection of tries that I attempted to use and the results.
BioPython For some reason, this implementation serializes to disk fine, but throws an exception on loading. Also, there’s a bug in the with_prefix function which I need to search the suffix trie with. I’m working on patching this myself.
CharTrie This library only supports strings as keys and ints as values. I mapped proteins to ints so that I could use this library. I couldn’t get my proteome to fit in memory with this library.
DATrie Insertions into this trie was too slow. For some reason when I got to the 3rd sequence, it took a few minutes to insert all suffixes. This would amount to months before the trie would finish building.
Marisa-Trie Difficult to build the trie since it’s read-only. This requires reading the entire proteome into memory, generating all suffixes and inserting them one by one into the trie with the correct sequence to protein mappings. There’s no point in pursuing this since it requires generating a suffix array and then inserting it into the trie.
Py-Radix Isn’t general purpose, only useful for IPv4/6 addresses."""

print('small text', len(short_search_phrase))
print('medium text', len(medium_search_phrase))
print('large text', len(long_search_phrase))


for phrase in [short_search_phrase, medium_search_phrase, long_search_phrase]:
    print('\n\n\n\n')
    print('using phrase ', phrase)
    for kw, vocab in [(kwsmall, vocabsmall), (kwmedium, vocabmedium), (kwlarge, vocablarge)]:
        print('\n')
        # exact match
        match_count = 0
        start = time.time()
        for word in vocab:
            if phrase.find(word) != -1:
                match_count += 1

        end = time.time()
        print(f'exact matching took {end-start} to find {match_count} matches')

        # fuzzysearch lib
        match_count = 0
        start = time.time()
        for word in vocab:
            matches = find_near_matches(word, phrase, max_l_dist=1)
            match_count += len(matches)
        end = time.time()
        print(f'fuzzy search lib took {end-start} to find {match_count} matches')

        # kw finder
        start = time.time()
        matches = kw.search('after school my dad and bob the buolder and me played cach wiht our catd')
        end = time.time()
        
        leventrie_results = ((end - start), len(matches))
        print(f'my trie guy took {end-start} to find {len(matches)} matches')
