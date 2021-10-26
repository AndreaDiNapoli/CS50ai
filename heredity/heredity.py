import csv
import itertools
import sys
from functools import reduce

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Declare an empty list for storing the probabilities to "joint"
    probabilities = []

    # Declare some constant to simplify readability of further calculations
    # p for the gene mutating
    mutation = PROBS["mutation"]
    # p for the gene don't mutate
    no_mutation = (1 - mutation)
    # p for the current gene passing to son generation (0.5 - mutation)+(0 + mutation)
    passed = 0.5

    # Create a variable that store the probability distribution of all the combination of gene x parents genes
    gene_prob_distr ={
        # Probability for number of gene x combination of parents genes
        # You can refer to the probability as gene_prob_distr[number of genes][parents number of genes]
        # Ex. probability to have 1 gene if one parent have 0 gene and the other one 2 is p = gene_prob_distr[One][02]
            0:{
                "Unknown": PROBS["gene"][0],
                "00": no_mutation * no_mutation,
                "01": no_mutation * passed,
                "10": passed * no_mutation,
                "11": passed * passed,
                "20": (mutation) * no_mutation, 
                "02": no_mutation * (mutation), 
                "21": (mutation) * passed,
                "12": passed * (mutation),
                "22": (mutation) * (mutation),
            },
            1: {
                "Unknown": PROBS["gene"][1],
                "00": (no_mutation * mutation) + (mutation * no_mutation),
                "01": (no_mutation * passed) + (mutation * passed),
                "10": (mutation * passed) + (no_mutation * passed),
                "11": 2 * (passed * mutation),
                "20": (no_mutation * no_mutation) + (mutation * mutation),
                "02": (mutation * mutation) + (no_mutation * no_mutation),
                "21": (no_mutation * passed) + (mutation * passed),
                "12": (passed * mutation) + (passed * no_mutation),
                "22": 2 * (mutation * no_mutation),
            },
            2: {
                "Unknown": PROBS["gene"][2],
                "00": mutation * mutation,
                "01": mutation * passed,
                "10": passed * mutation,
                "11": passed * passed,
                "20": no_mutation * mutation,
                "02": mutation * no_mutation,
                "21": no_mutation * passed,
                "12": passed * no_mutation,
                "22": no_mutation * no_mutation,
            },
    }

    # Loop through every person and calculate the gene probability accordingly to the set in which is contained
    for person in people:

        # Look for the number of genes needed
        if person in one_gene:
            n_gene= 1
        elif person in two_genes:
            n_gene = 2
        else:
            n_gene = 0
        
        # Look for the parents info
        if not person["mother"] and not person["father"]:
            parents_genes = "Unknown"
        else:
            if person["mother"] in one_gene:
                m_gene = 1
            elif person["mother"] in two_genes:
                m_gene = 2
            else:
                m_gene = 0

            if person["father"] in one_gene:
                f_gene = 1
            elif person["father"] in two_genes:
                f_gene = 2
            else:
                f_gene = 0
    
            parents_genes = str(m_gene + f_gene)

        # Calculate the probability and add it to the list
        probabilities.append(gene_prob_distr[n_gene][parents_genes])

        # Loop through every person and calculate the gene probability accordingly to the set in which is contained
        # Since n_gene store info about the number of gene the person has and PROBS is built such as traits is encoded as True and False you can directly acces to such info
        probabilities.append(PROBS["trait"][n_gene][person in have_trait])

    # Calculate joint probability and return
    # It could be done as a simple loop, but I've discovered functools so let's give it a try!
    j_prob = 1 * reduce(lambda x,y : x*y, probabilities)

    return j_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
