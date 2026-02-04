import nltk
import sys
import string

from nltk.tokenize import word_tokenize
from nltk.tree import Tree


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
VP -> V | V NP | V PP | V NP PP | Adv VP
NP -> N | Det N | Det AdjP N | NP PP
AdjP -> Adj | Adj AdjP
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()
    else:
        s = input("Sentence: ")

    s = preprocess(s)

    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
  
    tokens = word_tokenize(sentence.lower())
    words = []

    for token in tokens:
        if any(c.isalpha() for c in token):
            words.append(token)

    return words


def np_chunk(tree):

    chunks = []

    for subtree in tree.subtrees(lambda t: t.label() == "NP"):
        inner_nps = list(
            subtree.subtrees(lambda t: t.label() == "NP")
        )
        if len(inner_nps) == 1:
            chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    main()
