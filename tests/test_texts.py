import pytest
from lib.texts import normalize, tokenize, count_freq, top_n


# === Тесты для normalize ===


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка!", "ежик, елка!"),
        ("Hello\r\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
        ("", ""),
        ("   \n\t\r   ", ""),
        ("Тест-слово", "тест-слово"),
        ("С-слово и_ещё_одно", "с-слово и_еще_одно"),
    ],
)
def test_normalize_basic(source, expected):
    assert normalize(source) == expected


def test_normalize_casefold_off():
    text = "Привет МИР"
    expected = "Привет МИР"  # не меняется
    assert normalize(text, casefold=False) == expected


def test_normalize_yo2e_off():
    text = "Ёжик и елка"
    expected = "ёжик и елка"  # "Ё" не заменяется
    assert normalize(text, yo2e=False) == expected


# === Тесты для tokenize ===


@pytest.mark.parametrize(
    "text, expected",
    [
        ("привет, мир!", ["привет", "мир"]),
        ("слово-через-дефис", ["слово-через-дефис"]),
        ("слово -не -через", ["слово", "не", "через"]),
        ("", []),
        ("   ", []),
        ("a1b2_3", ["a1b2_3"]),
        ("test123_word", ["test123_word"]),
        ("слово, ещё!", ["слово", "ещё"]),
        ("слово- и ещё", ["слово", "и", "ещё"]),
        ("a-b-c", ["a-b-c"]),
        ("a--b", ["a", "b"]),  # два дефиса — разрывает слово
    ],
)
def test_tokenize_basic(text, expected):
    assert tokenize(text) == expected


# === Тесты для count_freq ===


@pytest.mark.parametrize(
    "tokens, expected",
    [
        ([], {}),
        (["a"], {"a": 1}),
        (["a", "b", "a"], {"a": 2, "b": 1}),
        (["один", "два", "один", "два", "один"], {"один": 3, "два": 2}),
    ],
)
def test_count_freq_basic(tokens, expected):
    assert count_freq(tokens) == expected


# === Тесты для top_n ===


def test_top_n_basic():
    freq = {"a": 5, "b": 3, "c": 7}
    result = top_n(freq, 2)
    expected = [("c", 7), ("a", 5)]
    assert result == expected


def test_top_n_n_larger_than_data():
    freq = {"a": 1, "b": 1}
    result = top_n(freq, 5)  # запрашиваем больше, чем есть
    expected = [("a", 1), ("b", 1)]  # всё возвращается
    assert result == expected


def test_top_n_tie_breaker():
    freq = {"банан": 3, "апельсин": 3, "яблоко": 3}
    result = top_n(freq, 3)
    # При равной частоте сортируем по алфавиту
    expected = [("апельсин", 3), ("банан", 3), ("яблоко", 3)]
    assert result == expected


def test_top_n_empty():
    assert top_n({}, 5) == []


def test_top_n_zero():
    freq = {"a": 2, "b": 1}
    assert top_n(freq, 0) == []


# === Интеграционный тест: полная цепочка ===


def test_full_pipeline():
    text = "Привет, ёжик! Привет, мир! Мир — красив."
    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    top = top_n(freq, 3)

    # Ожидаем: "привет" (2), "мир" (2), "ёжик|ежик" → "ежик", "красив" (1)
    # После нормализации: "ежик", "привет", "мир", "красив"
    assert freq["привет"] == 2
    assert freq["мир"] == 2
    assert "ежик" in freq
    assert top[0][0] in ["мир", "привет"]  # один из них на первом месте
    assert len(top) == 3
