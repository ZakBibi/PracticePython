
def remove_vowels(word):
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    abbreviation = []
    abbreviation.append(word[0])
    for w in word[1:]:
        if w not in vowels:
            abbreviation.append(w)
    return ''.join(abbreviation)