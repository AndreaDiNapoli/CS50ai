import nltk
import sys

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
S -> SS | SS Conj SS | SS Conj VP
SS -> NP VP 
VP -> V | V NP | Adv VP | VP Adv
NP -> ND | P ND | NP NP
ND -> NA | Det NA 
NA -> N | Adj NA
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Lowercase the sentence
    sentence = sentence.lower()
    # Create a list of tokens (1 token for 1 word)
    words_list = nltk.word_tokenize(sentence)
    wToRemove = []
    for word in words_list:
        isAlpha = False
        for char in word:
            if char.isalpha():
                isAlpha = True
                break
        if not isAlpha:
            wToRemove.append(word)
    words_list = [x for x in words_list if (x not in wToRemove)]
    print(words_list)
    return words_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Esplodi ogni ramo dell'albero fino a che non trovi un NP, se dentro c'è un altro NP continua a esplodere, altrimenti aggiungi l'NP alla lista
    chunk = []
    isMainTree = True
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            isMainTree = True
            hasNPsub = False
            for sub in subtree.subtrees():
                if isMainTree:
                    isMainTree = False
                elif sub.label() == "NP":
                    hasNPsub = True

            if hasNPsub == False:
                chunk.append(subtree)
                
    return chunk

if __name__ == "__main__":
    main()
