from .flatten import flatten


def get_keys_list(qset):
    flattened = []
    for doc in qset:
        f_doc = flatten(doc)
        for key in f_doc:
            flattened.append(key)
    return flattened


def count_key_occur(flattened_dict):
    freq = {}
    for item in flattened_dict:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    return freq


def all_keys_count(collection):
    return count_key_occur(get_keys_list(collection))

