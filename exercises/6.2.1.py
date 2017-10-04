num_items = 20

target_index = 100


i = 0
index = 0

while index <= target_index:
    i += 1
    index += num_items - i

j = num_items - (index - target_index)

print('\ni: %i\nj: %i\n' % (i, j))
