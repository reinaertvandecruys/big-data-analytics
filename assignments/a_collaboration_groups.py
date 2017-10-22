from itertools import combinations
from pprint import pformat

from _dblp import dblpparser


next_item_id = 0
items = []
item_ids = {}
item_supports = []
baskets = []


def process_record(record):
    global next_item_id, items, item_ids, baskets
    _, _, data = record
    basket = set()

    for author in data['author']:
        item, _ = author

        if item not in item_ids:
            items.append(item)
            item_supports.append(0)
            item_ids[item] = next_item_id
            next_item_id += 1

        item_id = item_ids[item]
        basket.add(item_id)
        item_supports[item_id] += 1

    baskets.append(basket)


dblpparser.Parser().parse(on_record=process_record, use_snap=True, silent=False)


itemset_size = 2
support_threshold = max(item_supports)

while support_threshold >= 2:
    frequent_items = {item for item in range(len(item_supports))
                      if item_supports[item] >= support_threshold}

    if len(frequent_items) < itemset_size:
        support_threshold -= 1
        continue

    itemset_supports = {}

    for basket in baskets:
        basket = {item for item in basket if item in frequent_items}

        for basket_subset in combinations(basket, itemset_size):
            if basket_subset not in itemset_supports:
                itemset_supports[basket_subset] = 0

            itemset_supports[basket_subset] += 1

    maximal_frequent_itemsets = {itemset for itemset, support in itemset_supports.items()
                                 if support >= support_threshold}

    if len(maximal_frequent_itemsets) == 0:
        support_threshold -= 1
        continue

    print('----------------------------------------------------------------')
    print(' Group size: %i    Highest support: %i    Number of groups: %i' %
          (itemset_size, support_threshold, len(maximal_frequent_itemsets)))
    print('----------------------------------------------------------------', end='')

    author_groups = sorted([sorted([items[item] for item in itemset])
                           for itemset in maximal_frequent_itemsets])
    max_name_length = [max([len(name) for name in (itemset[i] for itemset in author_groups)])
                       for i in range(itemset_size)]

    for author_group in author_groups:
        print()

        for i in range(len(author_group)):
            name = author_group[i]
            print(' - %s' % name.ljust(max_name_length[i]), end='')

    print('\n\n')

    itemset_size += 1
