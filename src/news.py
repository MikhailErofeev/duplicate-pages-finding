import sys

import mincemeat
import text_processing
import hashes
import shingles
import document


__author__ = 'erofeev'


def map_document_to_lsh_keys(path, file_name):
    text = text_processing.get_main_text_from_probably_html(text_processing.get_text_from_file(path + file_name))
    data_set = shingles.Shingler(text, 4).get_int_shingles()
    doc = document.Document(data_set, file_name)
    for key in hashes.get_document_lsh_keys(30, 100, doc):
        yield str(key), doc


def reduce_documents_pairs(key, documents):
    pairs = list()
    for itemA, itemB in document.combinations(documents):
        pairs.append(tuple([itemA, itemB]))
    return pairs


def map_to_process_into_comparsion_reduce(pair_name, documents_pair):
    yield pair_name, documents_pair


def compare_documents(pair_name, documents_pairs):
    shingles1 = (documents_pairs[0][0]).shingles
    shingles2 = (documents_pairs[0][1]).shingles
    return hashes.get_similarity(shingles1, shingles2)


files = "../data/"
if len(sys.argv) >= 2:
    files = sys.argv[1]

#TODO args handling (see mincemeat solution)
password = "changeme"
server = "localhost"

s = mincemeat.Server()
s.map_input = mincemeat.FileNameMapInput(files)
s.mapfn = map_document_to_lsh_keys
s.reducefn = reduce_documents_pairs
results = s.run_server(password)

#FIXME bottleneck  - aggregate all documents on 1 server memory. disc writing? MP with chaining jobs?
pairs = dict()
for pairs_list in results.values():
    for pair in pairs_list:
        documents_name = pair[0].name + "\t" + pair[1].name
        documents_pair = tuple([pair[0], pair[1]])
        pairs[documents_name] = documents_pair

s = mincemeat.Server()
s.map_input = mincemeat.DictMapInput(pairs)
s.mapfn = map_to_process_into_comparsion_reduce
s.reducefn = compare_documents
results = s.run_server(password)

results = sorted(results.iteritems(), key=lambda (k, v): (v, k), reverse=True)
for ret in results:
    print ret[0] + "\t" + str(ret[1])