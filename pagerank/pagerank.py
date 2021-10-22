import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Declare an empty dictionary
    distr_probability = {}

    # Check if the input page have any link. If no, then return an evenly distribution for each page in the corpus (random selection)
    if corpus[page] == None:
        for pages in corpus:
            distr_probability[pages] = 1/len(corpus)
        return distr_probability

    # Calculate the probability for each link in the page, as pr_randomlink = P(link | Damping_factor)
    pr_randomlink = ( ( 1/len(corpus[page]) ) + damping_factor ) / damping_factor

    # Calculate the probability for each page in the corpus, as pr_randompage = P(page | (1-Damping_factor))
    pr_randompage = ( ( 1/len(corpus) ) + (1 - damping_factor ) ) / (1 - damping_factor ) 

    # Loop for every page and build the dictionary
    for pages in corpus:
        if pages in corpus[page]:
            distr_probability[pages] = pr_randomlink + pr_randompage
        else:
            distr_probability[pages] = pr_randompage
    # Return the solution
    return distr_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Declare an empty dict
    pageranks = {}

    # Declare an empty list
    samples = []

    # Create a first sample by random and add it to a list
    sample = random.choice(corpus)
    samples.append(sample)

    # Loop for n-1 samples
    for i in range(n - 1):
        # Call the transition model for the current sample and check the probability distribution
        distr_probability = transition_model(corpus, sample, damping_factor)
        # Extract a random page from the corpus, accordingly to the probability distribution
        sample = random.choice(distr_probability, list(distr_probability.values()))
        # Add the page to the list
        samples.append(sample)

    # Loop through the list and count every page, adding 1 to the dictionary
    for sample in samples:
        if sample in pageranks:
            pageranks[sample] +=1
        else:
            pageranks[sample] = 1

    # Normalize the solution
    for page in pageranks:
        pageranks[page] = pageranks[page] / n
    # Return the solution
    return pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
