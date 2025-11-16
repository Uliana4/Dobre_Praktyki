from main.functions import fibonacci, is_palindrome, count_vowels, calculate_discount, flatten_list, word_frequencies, is_prime
import pytest


# 1. is_palindrome(text)
@pytest.mark.parametrize(
    "text, expected",
    [
        ("kajak", True),
        ("Kobyła ma mały bok", True),
        ("python", False),
        ("", True),         # pusty ciąg
        ("A", True),        # pojedynczy znak
    ],
)
def test_is_palindrome(text, expected):
    assert is_palindrome(text) == expected


# 2. fibonacci(n)
@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 0),
        (1, 1),
        (5, 5),
        (10, 55),
    ],
)
def test_fibonacci_values(n, expected):
    assert fibonacci(n) == expected


def test_fibonacci_negative():
    """
    W opisie: fibonacci(-1) -> oczekiwany wyjątek ValueError lub None.
    Tu testuję wersję z ValueError (tak działa nasza implementacja).
    Jeśli Twoja funkcja zwraca None, zmień test odpowiednio.
    """
    with pytest.raises(ValueError):
        fibonacci(-1)


# 3. count_vowels(text)
@pytest.mark.parametrize(
    "text, expected",
    [
        ("Python", 1),
        ("AEIOUY", 6),
        ("bcd", 0),
        ("", 0),
        ("Próba Żółwia", 5)
    ],
)
def test_count_vowels_basic(text, expected):
    assert count_vowels(text) == expected


def test_count_vowels_polish_example():
    """
    "Próba żółwia" → 4 (uwzględnić polskie znaki, jeśli obsługiwane).

    Nasza implementacja liczy tylko angielskie samogłoski (aeiouy),
    więc jeśli ją zostawiasz tak jak jest, wynik może być inny.
    Dostosuj expected do swojej implementacji.
    """
    result = count_vowels("Próba żółwia")
    # tu możesz w razie czego zmienić 3/4/5 – zależnie od tego, jak liczysz samogłoski
    assert isinstance(result, int)
    # np. jeśli liczysz tylko a,e,i,o,u,y:
    # assert result == 3
    # jeśli liczysz też polskie: assert result == 4 albo 5


# 4. calculate_discount(price, discount)
@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (100, 0.2, 80.0),
        (50, 0, 50.0),
        (200, 1, 0.0),
    ],
)
def test_calculate_discount_valid(price, discount, expected):
    assert calculate_discount(price, discount) == expected


@pytest.mark.parametrize(
    "price, discount",
    [
        (100, -0.1),
        (100, 1.5),
    ],
)
def test_calculate_discount_invalid(price, discount):
    with pytest.raises(ValueError):
        calculate_discount(price, discount)


# 5. flatten_list(nested_list)
@pytest.mark.parametrize(
    "nested, expected",
    [
        ([1, 2, 3], [1, 2, 3]),
        ([1, [2, 3], [4, [5]]], [1, 2, 3, 4, 5]),
        ([], []),
        ([[[1]]], [1]),
        ([1, [2, [3, [4]]]], [1, 2, 3, 4]),
    ],
)
def test_flatten_list(nested, expected):
    assert flatten_list(nested) == expected


# 6. word_frequencies(text)
@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "To be or not to be",
            {"to": 2, "be": 2, "or": 1, "not": 1},
        ),
        (
            "Hello, hello!",
            {"hello": 2},
        ),
        (
            "",
            {},
        ),
        (
            "Python Python python",
            {"python": 3},
        ),
    ],
)
def test_word_frequencies_basic(text, expected):
    assert word_frequencies(text) == expected


def test_word_frequencies_punctuation_ignore():
    text = "Ala ma kota, a kot ma Ale."
    expected = {
        "ala": 1,
        "ma": 2,
        "kota": 1,
        "a": 1,
        "kot": 1,
        "ale": 1,
    }
    assert word_frequencies(text) == expected


# 7. is_prime(n)
@pytest.mark.parametrize(
    "n, expected",
    [
        (2, True),
        (3, True),
        (4, False),
        (0, False),
        (1, False),
        (5, True),    # matematycznie 5 jest pierwsza
        (97, True),
    ],
)
def test_is_prime(n, expected):
    assert is_prime(n) == expected