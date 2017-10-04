from itertools import combinations
from pprint import pformat, pprint


items = list(range(1, 101))

baskets = [{item for item in items if basket % item == 0}
           for basket in range(1, 101)]

support_threshold = 5


print('\n(a) If the support threshold is 5, which items are frequent?\n')

supports = {item: sum(item in basket for basket in baskets) for item in items}
frequent_items = {item: supports[item] for item in supports
                  if supports[item] >= support_threshold}

print('%s\n' % pformat(frequent_items))


print('\n(b) If the support threshold is 5, which pairs of items are frequent?\n')

pair_supports = {pair: sum(set(pair).issubset(basket) for basket in baskets)
                 for pair in combinations(items, 2)}
frequent_pairs = {pair: pair_supports[pair] for pair in pair_supports
                  if pair_supports[pair] >= support_threshold}

print('%s\n' % pformat(frequent_pairs))


print('\n(c) What is the sum of the sizes of all the baskets?\n')

sum_basket_sizes = sum(len(basket) for basket in baskets)

print('%i\n' % sum_basket_sizes)
