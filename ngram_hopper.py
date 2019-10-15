from bs4 import BeautifulSoup
from urllib import request
from nltk import word_tokenize
import random

def get_iliad_book(num):
    if num < 1 or num > 24:
        raise Exception('Book number requested out of bounds. Give a number between 1 and 24, incl.')
    b = str(num).zfill(2)
    url = "https://www.sacred-texts.com/cla/homer/greek/ili" + b + ".htm"
    html = request.urlopen(url).read().decode('utf8')
    raw = BeautifulSoup(html, 'html.parser').get_text()
    raw = raw.split("\n")
    for i in range(len(raw)):
        if "The Iliad, Book " in raw[i]:
            raw = raw[i+1:]
            break
    else:
        raise Exception("Could not find title line.")
    while '\xa0' in raw:
        raw.remove('\xa0')
    for i in range(len(raw)-1, -1, -1):
        if "Next: " in raw[i]:
            raw = raw[:i]
            break
    else:
        raise Exception("Could not find end line.")
    while raw[-1] == '':
        del raw[-1]
    book = []
    for line in raw:
        t = word_tokenize(line)
        if t[-1][0] in "0123456789":
            del t[-1]
        book.extend(t)
    return book

def get_iliad():
    """ returns the entire iliad text """
    t = []
    for n in range(1, 25):
        t.extend(get_iliad_book(n))
    return t

def ngram_dict(t, n):
    """ inputs a text (line of string "tokens") and returns a dictionary of n-grams (n=2: bigrams; n=3: trigrams, etc.) """
    ngrams = dict()
    for i in range(len(t) - (2*n-1)):
        gram = ()
        for _ in range(n):
            gram += t[i+_],
        ngrams.setdefault(gram, [])
        next_gram = ()
        for _ in range(n):
            next_gram += t[i+n+_],
        ngrams[gram].append(next_gram)
    return ngrams

def random_text(ngram_dict, length):
    """ given an ngram dictionary and a specified length, returns text created by hopping through ngrams that are attested to follow each other in the text. """
    t = []
    gram = random.choice(list(ngram_dict.keys()))
    while len(t) < length:
        t.extend(gram)
        gram = random.choice(ngram_dict[gram])
    return ' '.join(t)

if __name__ == "__main__":

    n_i = ngram_dict(get_iliad(), 3)
    for _ in range(5):
        print(random_text(n_i, 10))
    
    s = open('silmarillion.txt', encoding='utf8').read()
    s = word_tokenize(s)
    n_s = ngram_dict(s, 2)
    for _ in range(5):
        print(random_text(n_s, 10))
