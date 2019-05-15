def break_words(stuff):
    """This function will break up words for us."""
    words = stuff.split(' ')
    return words

def sort_words(words):
    """Sorts the words."""
    return sorted(words)

def print_first_word(words):
    """Prints the first word after popping it off."""
    word = words.pop(0)
    print word

def print_first_and_last(sentence):
    """Prints the first and last words of the sentence."""
    words = break_words(sentence)
    print_first_word(words)
    print_last_word(words)

def print_first_and_last_sorted(sentence):
    """Sorts the words then prints the first and last one."""
    words = sort_sentence(sentence)
    print_first_word(words)
    print_last_word(words)


sent = "All good things come to those who wait."

words = break_words(sent)
print "AELZ_01 breaked words:", words
sorted_words = sort_words(words)
print "---AELZ_02 first and last words:"
print_first_word(words)
print_last_word(words)
print "---AELZ_03 sorted first and last words:", sorted_words
print_first_word(sorted_words)
print_last_word(sorted_words)
sorted_words = sort_sentence(sent)
print "---AELZ_04 sorted sentence", sorted_words
print_first_and_last(sent)
print_first_and_last_sorted(
sent)
