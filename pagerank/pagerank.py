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
 
    pages = dict()

    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):

    total_pages = len(corpus)
    probabilities = dict()

    links =corpus[page]
    if links:
        for p in corpus:
            probabilities[p] = (1-damping_factor)/total_pages
        for linked_page in links:
            probabilities[linked_page] += damping_factor/len(links)
    else:
        for p in corpus:
            probabilities[p]=1/total_pages
        
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    pagerank = {page: 0 for page in corpus}
    
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        pagerank[current_page] += 1
        probabilities = transition_model(corpus, current_page, damping_factor)

        current_page = random.choices(
            population=list(probabilities.keys()),
            weights=list(probabilities.values()),
            k=1
        )[0]

    for page in pagerank:
        pagerank[page] /= n

    return pagerank




def iterate_pagerank(corpus, damping_factor):

    N = len(corpus)
    pagerank = {page: 1 / N for page in corpus}

    for page in corpus:
        if not corpus[page]:
            corpus[page] = set(corpus.keys())

    converged = False
    while not converged:
        new_pagerank = {}
        for page in corpus:
            total = 0
            for possible_page in corpus:
                if page in corpus[possible_page]:
                    total += pagerank[possible_page] / len(corpus[possible_page])
            new_pagerank[page] = (1 - damping_factor) / N + damping_factor * total

        converged = all(
            abs(new_pagerank[page] - pagerank[page]) < 0.001
            for page in pagerank
        )
        pagerank = new_pagerank

    total_rank = sum(pagerank.values())
    for page in pagerank:
        pagerank[page] /= total_rank

    return pagerank



if __name__ == "__main__":
    main()
