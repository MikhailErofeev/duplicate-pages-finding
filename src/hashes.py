import sys

import scipy


__author__ = 'erofeev'

MAX_32_INT = sys.maxint
FUNCTIONS_COUNT = 500


def get_similarity(shingles1, shingles2):
    sig1 = signature(shingles1)
    sig2 = signature(shingles2)
    return hamming_similarity(sig1, sig2)


def signature(shingles):
    ret = scipy.zeros(FUNCTIONS_COUNT)
    for function_id in xrange(FUNCTIONS_COUNT):
        ret[function_id] = min_hash(shingles, function_id)
    return ret


def min_hash(shingles, function_id):
    min_hash = MAX_32_INT
    for shingle in shingles:
        hash_value = hash_function(shingle, function_id)
        if hash_value < min_hash:
            min_hash = hash_value
    return min_hash


def hash_function(shingle, function_id):
    return hash(shingle * function_id * function_id)


def hamming_similarity(sig1, sig2):
    return (sig1 == sig2).sum() / float(FUNCTIONS_COUNT)


def get_key_for_stripe(stripe_id, functions_by_buckets, document):
    stripe_key = MAX_32_INT
    start_function = functions_by_buckets * (stripe_id - 1)
    for function_id in xrange(start_function, start_function + functions_by_buckets):
        hash_value = min_hash(document.shingles, function_id)
        if hash_value < stripe_key:
            stripe_key = hash_value
    return stripe_key


def get_document_lsh_keys(stripes_count, functions_count, document):
    functions_by_stripe = functions_count / stripes_count
    i = 0
    stripe_id = 0
    ret = set()
    for function_id in xrange(functions_count + 1):
        if i % functions_by_stripe == 0 and i > 0:
            stripe_id += 1
            ret.add(get_key_for_stripe(stripe_id, functions_by_stripe, document))
        i += 1
    return ret