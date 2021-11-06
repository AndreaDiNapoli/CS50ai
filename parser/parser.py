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
    # Loop through every word
    for word in words_list:
        isAlpha = False
        # Check if there are alphabetic char in the word, otherwise flag the word to be removed
        for char in word:
            if char.isalpha():
                isAlpha = True
                break
        if not isAlpha:
            wToRemove.append(word)
    # Clean the wordlist and return it
    words_list = [x for x in words_list if (x not in wToRemove)]
    return words_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    chunk = []
    isMainTree = True
    # Loop through every subtree element
    for subtree in tree.subtrees():
        # If the label of the subtree is NP, see if there is a "son" with NP, otherwise add it to the chunk list
        if subtree.label() == "NP":
           # A trick to skip the first subtree (which is the main tree itself) 
            isMainTree = True
            hasNPsub = False
            for sub in subtree.subtrees():
                if isMainTree:
                    isMainTree = False
                elif sub.label() == "NP":
                    hasNPsub = True
            # If no subtree "leaves" with NP label is found, add the subtree to the chunk list
            if hasNPsub == False:
                chunk.append(subtree)
                
    # Return the list           
    return chunk

if __name__ == "__main__":
    main()
