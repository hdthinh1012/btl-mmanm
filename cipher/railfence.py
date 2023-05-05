from typing import Tuple
import re


def railfence_encrypt(text: str, key: int) -> str:
    """Rail fence cipher (Transposition cipher)"""

    rows = key
    cycle = rows * 2 - 2
    fence_rows = [""] * rows

    for x in range(len(text)):
        y = rows - 1 - abs(cycle // 2 - x % cycle)
        fence_rows[y] += text[x]

    return "".join(fence_rows)


def railfence_decrypt(text: str, key: int) -> str:
    """Rail fence cipher (Transposition cipher)"""

    rows = key
    cycle = rows * 2 - 2
    result = [""] * len(text)

    index = -1
    for y in range(rows):
        for x in range(len(text)):
            if (y + x) % cycle == 0 or (y - x) % cycle == 0:
                index += 1
                result[x] = text[index]

    return "".join(result)


def railfence_cryptoanalysis(text: str) -> Tuple[str, int]:
    """Rail fence cipher cryptoanalysis (Transposition cipher)"""

    valid_words = load_english_vocab_words()
    L = len(text)
    for key in range(2, L // 2):
        print(f"Testing key {key}...")
        res = railfence_decrypt(text, key)
        test_res = res[0:100]
        word_list = re.findall(r"\w+", test_res)
        counter = 0
        for word in word_list:
            if word.lower() in valid_words:
                counter += 1
        if counter > 5:
            return res, key
    return "", 0


def load_english_vocab_words():
    with open("cipher/words.txt") as word_file:
        valid_words = set(word_file.read().split())
    return valid_words
