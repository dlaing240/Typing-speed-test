
with open("word_list.txt", "r") as word_file:
    word_list = word_file.read().splitlines()
    # Use weighting to make 5-letter words appear more frequently
    target_length = 5
    weights = [(1/(abs(len(word)-target_length)+1))**2 for word in word_list]

