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

    for i, ch in enumerate(text):
        # Проверяем, является ли символ допустимым в слове
        if ch.isalnum() or ch == "_":
            word += ch

        elif ch == "-":
            # Проверяем, является ли дефис частью составного слова
            prev_is_alnum = i > 0 and text[i - 1].isalnum()
            next_is_alnum = i < len(text) - 1 and text[i + 1].isalnum()

            if prev_is_alnum and next_is_alnum:
                # Дефис между буквами/цифрами → часть слова
                word += ch
            else:
                # Дефис как разделитель → завершаем текущее слово
                if word:
                    tokens.append(word)
                    word = ""

        else:
            # Любой другой символ (пробел, запятая и т.д.)
            if word:
                tokens.append(word)
                word = ""

    # Добавляем последнее слово
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
