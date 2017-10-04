items = list(range(1, 101))

baskets = [{item for item in items if basket % item == 0}
           for basket in range(1, 101)]


print('\n(a) {5, 7} → 2.\n')

antecedent_baskets = [basket for basket in baskets if {5, 7}.issubset(basket)]
consequent_baskets = [basket for basket in antecedent_baskets if 2 in basket]

print('%f\n' % (len(consequent_baskets) / len(antecedent_baskets)))


print('\n(b) {2, 3, 4} → 5.\n')

antecedent_baskets = [basket for basket in baskets
                      if {2, 3, 4}.issubset(basket)]
consequent_baskets = [basket for basket in antecedent_baskets if 5 in basket]

print('%f\n' % (len(consequent_baskets) / len(antecedent_baskets)))
