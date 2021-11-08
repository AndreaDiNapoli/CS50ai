import nltk
import sys
import os
import string
import math

from nltk.tokenize import word_tokenize

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    loaded_files = {}

    file_list = next(os.walk(directory))[2]
    for file in file_list:
        fname = file
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as file:
            content = file.read()
        
        loaded_files[fname] = content
    return loaded_files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Get a list of token
    token_list = word_tokenize(document)
    words =[]
    # Process the list to remove punctuation, stopwords and by lowercasing everything
    for i in range(len(token_list)):
        token = token_list[i]
        token = token.lower()
        if token not in nltk.corpus.stopwords.words("english") and token not in string.punctuation:
            words.append(token)
  
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_idf = {}

    # Declare a dict that save maps every word found with an bool to rapresent the fact that the word has been yet counted for the current document
    wordLooked = {}

    # Loop through every document
    for document in documents.keys():

        # Reset the wordLooked indicator
        for w in wordLooked.keys():
            wordLooked[w] = False

        # Loop through every word in the document
        for word in documents[document]:
            # If the word is not been considered yet for the current dictionary, elaborate it
            if word not in wordLooked.keys() or wordLooked[word] == False:

                # If the word is not yet in the dictionary, add it with a value of 1
                if word not in word_idf.keys():
                    word_idf[word] = 1
                else:
                    word_idf[word] +=1
                wordLooked[word] = True
    
    # Update the dict calculating the IDF value
    for word in word_idf.keys():
        word_idf[word] = math.log(len(documents.keys())/word_idf[word])
    return word_idf



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    results = []
    doc_tfidfSum = {}

    # Loop through every document
    for document in files.keys():
        sum = 0
        # Loop through every word in query and count how many times it appear
        for word in query:
            count = files[document].count(word)
            
            # Calculate the tfidf of the word for that document
            if count > 0:
                tfidf = count * idfs[word]
                sum += tfidf
        # Sum togheter all the idf for the document and store it to a dict document:idfsum
        doc_tfidfSum[document] = sum

    # Order the dictionary by idfs value
    doc_tfidfSum = sorted(doc_tfidfSum.items(), key=lambda x: x[1], reverse=True)

    # For n times do this:
    for i in range(n):
        results.append(doc_tfidfSum[i][0])

    # Return results
    return results


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    results = []
    sentence_dict = {}
    for sentence in sentences:
        mwm = 0     # matching word measure
        qtd = 0     # query term density
        # Loop through every word in the query
        for word in query:
            # If the word is in the sentence, update mwm with idfs value and add 1 to the count of "query word in sentence"
            if word in sentences[sentence]:
                mwm += idfs[word]
                qtd +=1
        # Calculate query term density by dividing number of query word in sentence with number of word in sentence
        qtd = qtd / len(sentences[sentence])

        # Update the dictionary
        sentence_dict[sentence] = (mwm, qtd)
    
    # Order the dictionary by mwm and qtd
    sentence_dict = sorted(sentence_dict.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)

    # For n times do this:
    for i in range(n):
        results.append(sentence_dict[i][0])

    return results


if __name__ == "__main__":
    main()
