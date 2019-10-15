from bs4 import BeautifulSoup
from urllib import request
from nltk import word_tokenize
import string

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
    """ generates the entire iliad text """
    t = []
    for n in range(1, 25):
        t.extend(get_iliad_book(n))
    return t

def ngram_freq(t, n):
    """ inputs a text (line of string "tokens") and returns a directory of counts of n-gram (n=2: bigrams; n=3: trigrams, etc.) occurrences. """
    ngrams = dict()
    for i in range(len(t) - (n-1)):
        gram = ()
        for _ in range(n):
            gram += t[i+_],
        ngrams[gram] = ngrams.get(gram, 0) + 1
    return ngrams

def filter_punctuation(ngrams):
    """ filter out ngrams where at least one element is a punctuation mark. """
    for key in list(ngrams.keys()):
        for element in key:
            if element in string.punctuation:
                del ngrams[key]
                break
    return None

def filter_length(ngrams, length):
    """ filter out ngrams where the length of at least one element is shorter than a specified threshold. """
    for key in list(ngrams.keys()):
        for element in key:
            if len(element) < length:
                del ngrams[key]
                break
    return None

def filter_freq(ngrams, freq):
    """ filter out ngrams whose number of occurrences is lower than a specified threshold. """
    for key in list(ngrams.keys()):
        if ngrams[key] < freq:
            del ngrams[key]
    return None

def sort_dict(ngrams):
    """ returns sorted dictionary. """
    t = []
    for key in ngrams:
        t.append((ngrams[key], key))
    t.sort(reverse = True)
    new_dict = dict()
    for val, key in t:
        new_dict[key] = val
    return new_dict

def print_tuple(tup):
    for i in tup:
        print(i, end=' ')
    return None

def print_dict(d):
    """ print dictionary with one entry per line """
    for key in d:
        print_tuple(key)
        print(':\t', d[key])
    return None

if __name__ == "__main__":

    n = ngram_freq(get_iliad(), 2)
    filter_punctuation(n)
    filter_length(n, 4) # disregard ngrams with elements shorter than 4 characters
    filter_freq(n, 15) # disregard ngrams that occur fewer than 10 times
    n = sort_dict(n)
    print_dict(n)