# coding=utf-8
from __future__ import unicode_literals
"""
This file transforms the word list obtained from Brihat Nepali Shabdakosh, courtesy of Dr. Nobal Bikram Niraula
"""

hyphen = "–"
nepali_numbers = "१२३४५६७८९"
slash = "/"


def process_word(word):
    # some word has number in it, i.e. खापा२
    if word[-1] in nepali_numbers:
        word = word[:-1]
    # some words have suffix indicators.. खाप्–नु
    if hyphen in word:
        # word = word.replace(hyphen, "")
        word = word[:word.find(hyphen)]

    # some root have aliases, i.e. खान्की/खान्गी, give two independent words
    if slash in word:
        return word.split(slash)
    return [word]


def extract_words_from_brihat(filename):
    with open(filename, "r") as root_file:
        words = root_file.read().decode("utf-8").splitlines()
        words_list = map(process_word, words)
        return list(set([w for words in words_list for w in words]))

def extract_words_from_contemporary(filename):
    with open(filename, "r") as root_file:
        words = root_file.read().decode("utf-8").splitlines()
        words_list = map(lambda line: line.partition("|")[0], words)
        return words_list

if __name__ == "__main__":
    words = extract_words_from_brihat("../files/shabdakosh-words.txt")
    words_2 = extract_words_from_contemporary("../files/root")
    print len(words_2)
    print len(set(words).intersection(set(words_2)))
    print len(set(words) - set(words_2))

    # print "\n".join(words[:20])