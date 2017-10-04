from itertools import combinations
from pprint import pformat, pprint


items = list(range(1, 7))

baskets = [
    {1, 2, 3},
    {1, 3, 5},
    {3, 5, 6},
    {2, 3, 4},
    {2, 4, 6},
    {1, 2, 4},
    {3, 4, 5},
    {1, 3, 4},
    {2, 3, 5},
    {4, 5, 6},
    {2, 4, 5},
    {3, 4, 6},
]

support_threshold = 4

num_buckets = 11


def hashed(pair):
    return (pair[0] * pair[1]) % num_buckets


print('\n(a) By any method, compute the support for each item and each pair of items.\n')

supports = {item: sum(item in basket for basket in baskets) for item in items}
pair_supports = {pair: sum(set(pair).issubset(basket) for basket in baskets)
                 for pair in combinations(items, 2)}

print('Supports:\n%s\n' % pformat(supports))
print('Pair supports:\n%s\n' % pformat(pair_supports))


print('\n(b) Which pairs hash to which buckets?\n')

buckets = [0] * num_buckets
bucket_map = {i: set() for i in range(num_buckets)}

for pair in combinations(items, 2):
    hashed_pair = hashed(pair)
    buckets[hashed_pair] += 1
    bucket_map[hashed_pair].add(pair)

print('%s\n' % pformat(bucket_map))


print('\n(c) Which buckets are frequent?\n')

frequent_buckets = {i: buckets[i] for i in range(num_buckets)
                    if buckets[i] >= support_threshold}

print('%s\n' % pformat(frequent_buckets))


print('\n(d) Which pairs are counted on the second pass of the PCY Algorithm?\n')

frequent_pair_candidates = {pair for pair in combinations(items, 2) if buckets[hashed(pair)] >= support_threshold}

print('%s\n' % pformat(frequent_pair_candidates))
