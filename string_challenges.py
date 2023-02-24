# Вывести последнюю букву в слове
word = 'Архангельск'
print(f'Последняя буква в "{word}": {word[-1]}')


# Вывести количество букв "а" в слове
word = 'Архангельск'
print(f'Количество "а" в "{word}": {word.count("а")}')


# Вывести количество гласных букв в слове
word = 'Архангельск'
vovels = 'аяуюоеёэиы'
vovels_num = 0
for letter in word.lower():
    if letter in vovels:
        vovels_num += 1
print(f'Количество глассных букв в "{word}": {vovels_num}')


# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
print(f'Количество слов в "{sentence}": {sentence.count(" ") + 1}')


# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
print(f'Первые буквы в словах из"{sentence}" по одной на строке:')
for elem in sentence.split():
    print(elem[0])


# Вывести усреднённую длину слова в предложении
sentence = 'Мы приехали в гости'
words_list = sentence.split()
words_count = len(words_list)
letters_count = 0
for word in words_list:
    letters_count += len(word)
print(f'Средняя длина слов в "{sentence}": {letters_count / words_count}')
