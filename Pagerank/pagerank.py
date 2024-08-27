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


    #do I have to chagnge the line below?
    if len(corpus[page]) == 0:
        divisor = len(corpus)
        probDict = {key: 1/divisor for key in corpus}
        return probDict

    probDict = {key: 0 for key in corpus}
    
    #adding probability of picking any page at random
    divisor = len(probDict)
    for key in probDict:
        probDict[key] += (1-damping_factor)/divisor
    
    #adding probability to the distribution
    nextLink = corpus[page]
    divisor = len(nextLink)
    for link in nextLink:
        probDict[link] += damping_factor/divisor

    return probDict


def sample_pagerank(corpus, damping_factor, n):

    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probDict = {key: 0 for key in corpus}
    pageRankAdd = 1/n

    keysList = [key for key in corpus]
    nextPage = keysList[random.randrange(len(corpus))]
    probDict[nextPage] += pageRankAdd
    
    for i in range(1,n):
        tranModel = transition_model(corpus, nextPage, damping_factor) 
        listPage = [key for key in tranModel]
        listPercent = [tranModel[key]*100 for key in listPage]
        nextPage = random.choices(listPage, listPercent, k=1)[0]
        probDict[nextPage] += pageRankAdd
    
    return probDict

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageCount = len(corpus)
    probDict = {page: 1/pageCount for page in corpus}
    convergenceThreshold = 0.001

    while True:

        newRank = {page: (1-damping_factor)/pageCount for page in corpus}
        for p in probDict:
            count = 0

            for i in corpus:
                if p in corpus[i]:
                    count += probDict[i]/len(corpus[i])
                elif not corpus[i]:
                    count += probDict[i]/pageCount

            newRank[p] += damping_factor * count

        if all(abs(probDict[page] - newRank[page]) < convergenceThreshold for page in corpus):
            break
        else:
            probDict = newRank

    return probDict



if __name__ == "__main__":
    main()



        # page p in `pagerank_dict`
    for p in pagerank_dict:
        summation = 0
  # consider each possible page
        for i in corpus:

            # if `i` links to page `p`
            if p in corpus[i]:

                # number of links on page `i`
                num_links_i = len(corpus[i])

                # page `i` has its own PageRank
                pr_i = pagerank_dict[i]

                # since from page i we travel to any of that page’s links with equal probability,
                # we divide PR(i) by the number of links NumLinks(i)
                page_prob = pr_i / num_links_i

                summation += page_prob

            # else if page has no links at all
            elif not corpus[i]:

                # page `i` has its own PageRank
                pr_i = pagerank_dict[i]

                # A page that has no links at all should be interpreted as having one link
                # for every page in the corpus (including itself).
                page_prob = pr_i / corpus_len

                summation += page_prob