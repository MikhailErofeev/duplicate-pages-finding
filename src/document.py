__author__ = 'erofeev'


class Document:
    shingles = None
    name = None

    def __init__(self, shingles, name):
        self.shingles = shingles
        self.name = name

    def __repr__(self):
        return self.name


def combinations(documents):
    documents.sort(key=lambda document: document.name)
    ret = list()
    i = 0
    for it1 in documents:
        for it2 in documents[i + 1:]:
            ret.append([it1, it2])
        i += 1
    return ret