# Your list
lst = [('mabahes_1', 'mabahes_2'), ('mabahes_1', 'jabr'), ('mabahes_1', 'kargah_barname_nevisi'), ('mabahes_2', 'jabr'), ('mabahes_2', 'kargah_barname_nevisi'), ('jabr', 'kargah_barname_nevisi')]

# Create a new list without tuples containing 'mabahes_1'
new_lst = [t for t in lst if 'mabahes_1' not in t]

# Print the new list
print(new_lst)
