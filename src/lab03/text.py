def normalize(text: str, *, casefold: bool = True, yo2e: bool = True):
    s = text
    if casefold:
        s = s.casefold()
    if yo2e:
        s = s.replace('ё', 'е')
    s = s.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
    s = ' '.join(s.split())
    return s
def tokenize(text):
    tokens = []
    word = ''
    for ch in text:
        if ch.isalnum() or ch == '_':
            word += ch
        elif ch == '-' and word:
            word += '-'
        else:
            if word:
                tokens.append(word)
                word = ''
    if word:
        tokens.append(word)
    return tokens
def count_freq(tokens):
    freq = {}
    for word in tokens:
        freq[word] = freq.get(word, 0) + 1
    return freq
def top_n(freq, n=5):
    result = sorted(freq.items(), key=lambda pair: (-pair[1], pair[0]))
    return result[:n]

#           Тест-кейсы
# assert normalize("ПрИвЕт\nМИр\t") == "привет мир"
# assert normalize("ёжик, Ёлка") == "ежик, елка"
# assert normalize("Hello\r\nWorld") == "hello world"
# assert normalize("  двойные   пробелы  ") == "двойные пробелы"

# print("normalize успешно!")
# assert tokenize("привет, мир!") == ["привет", "мир"]
# assert tokenize("по-настоящему круто") == ["по-настоящему", "круто"]
# assert tokenize("2025 год") == ["2025", "год"]
# assert tokenize("hello,world!!!") == ["hello", "world"]
# assert tokenize("emoji 😀 не слово") == ["emoji", "не", "слово"]
# print("tokenize успешно!")
# freq = count_freq(["a","b","a","c","b","a"])
# assert freq == {"a":3, "b":2, "c":1}
# assert top_n(freq, 2) == [("a",3), ("b",2)]
# print("count_freq + top_n успешно!")

# freq2 = count_freq(["bb","aa","bb","aa","cc"])
# assert top_n(freq2, 2) == [("aa",2), ("bb",2)]
# print("тай-брейк по слову при равной частоте успешно!")