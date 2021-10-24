import os
import random
import re
import sys
import copy

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
    if not corpus[page]:
        for pages in corpus:
            distr_probability[pages] = 1/len(corpus)
        return distr_probability

    # Calculate the probability for each link in the page (df/number of possible links)
    pr_randomlink = damping_factor / len(corpus[page])

    # Calculate the probability for each page in the corpus (1-df/number of pages in corpus)
    pr_randompage = (1 - damping_factor) / len(corpus)

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
    pagelist = list(corpus.keys())
    sample = random.choice(pagelist)
    samples.append(sample)

    # Loop for n-1 samples
    for i in range(n - 1):
        # Call the transition model for the current sample and check the probability distribution
        distr_probability = transition_model(corpus, sample, damping_factor)
        # Extract a random page from the corpus, accordingly to the probability distribution
        page_keys = list(distr_probability.keys())
        sample = random.choices(page_keys, weights = list(distr_probability.values()), k=1)[0]
        # Add the page to the list
        samples.append(sample)

    # Loop through the list and count every page, adding 1 to the dictionary
    for sample in samples:
        if sample in pageranks:
            pageranks[sample] += 1
        else:
            pageranks[sample] = 1

    # Normalize the solution
    for page in pageranks:
        pageranks[page] = pageranks[page] / n
    # Return the solution
    return pageranks

def pagerankFormula(pagerank, damping_factor, corpus):
    """
    Applicate the pagerank formula
    """
    # Create e deepcopy of the dictionary
    new_pagerank = copy.deepcopy(pagerank)

    # Loop for every page in the corpus and calculate a new value of the pagerank using the formula, store them in the new dictionary copy
    for page in new_pagerank:
        # Calculate the summatory of pr(i)/numlink(i), where i is every page that link to the page considered in this loop step
        sum = 0
        for i in corpus:
            if page in corpus[i]:
                sum += ( pagerank[i] / len(corpus[i]) )
        # Applicate the formula and update the value
        new_pagerank[page] = ( (1 - damping_factor)/len(corpus) ) + (damping_factor * sum)
    
    return new_pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Declare an empty dictionary
    pageranks2 = {}
    # Loop for every page in the corpus, and create a dict key for that page, with a starting pagerank value of 1/pages
    for page in corpus:
        pageranks2[page] = 1/len(corpus)

    # Declare a controller value
    delta_controller = False

    while delta_controller == False:

        # Calculate the pageranks using the iterative formula until convergence
        new_pageranks2 = pagerankFormula(pageranks2, damping_factor, corpus)

        # Loop throug every page in the dictionary and calculate the delta from the old dict values
        delta = []
        for page in new_pageranks2:
            # Calculate the difference in value (and turn to positive)
            delta.append(abs(pageranks2[page] - new_pageranks2[page]))
    
        pageranks2 = new_pageranks2

        # Check if all the delta is under 0.001, if yes, set the controller to true
        if all(i < 0.001 for i in delta):
            delta_controller = True
    
    return new_pageranks2


if __name__ == "__main__":
    main()
