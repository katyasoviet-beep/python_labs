def normalize(text: str, *, casefold: bool = True, yo2e: bool = True):
    s = text
    if casefold:
        s = s.casefold()
    if yo2e:
        s = s.replace("ё", "е")
    s = s.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    s = " ".join(s.split())
    return s


def tokenize(text):
    tokens = []
    word = ""
    for ch in text:
        if ch.isalnum() or ch == "_":
            word += ch
        elif ch == "-" and word:
            word += "-"
        else:
            if word:
                tokens.append(word)
                word = ""
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


text = input()
text = normalize(text)
tokens = tokenize(text)
freq = count_freq(tokens)
top = top_n(freq, 5)
print("Всего слов:", len(tokens))
print("Уникальных слов:", len(freq))
print("Топ-5:")
for word, count in top:
    print(f"{word}:{count}")
