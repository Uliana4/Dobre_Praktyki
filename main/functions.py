import re


def is_palindrome(text: str) -> bool:
    cleaned = re.sub(r'\s+', '', text).lower()
    return cleaned == cleaned[::-1]


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")

    if n == 0:
        return 0
    if n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def count_vowels(text: str) -> int:
    vowels = "aeiouyąęó"
    return sum(1 for char in text.lower() if char in vowels)


def calculate_discount(price: float, discount: float) -> float:
    if not (0 <= discount <= 1):
        raise ValueError("Discount must be between 0 and 1")
    return price * (1 - discount)


def flatten_list(nested_list: list) -> list:
    result = []

    for element in nested_list:
        if isinstance(element, list):
            result.extend(flatten_list(element))
        else:
            result.append(element)

    return result


def word_frequencies(text: str) -> dict:
    cleaned = re.sub(r'[^\w\s]', '', text.lower())
    words = cleaned.split()
    freq = {}

    for word in words:
        freq[word] = freq.get(word, 0) + 1

    return freq


def is_prime(n: int) -> bool:
    if n < 2:
        return False

    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False

    return True

