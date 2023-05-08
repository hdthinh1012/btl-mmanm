"""Cipher module."""

from __future__ import annotations

import re

from abc import ABC, abstractmethod
from pathlib import Path
from string import ascii_letters

import numpy as np


def frequency_statistic(text: str, alphabet: str = ascii_letters) -> dict[str, float]:
    """Calculate occurrence rate of each character in `text`, sorted by rate."""

    char, times = np.unique(
        [char for char in text if char in alphabet], return_counts=True
    )
    return dict(
        sorted(
            zip(char, (times * 100 / len(text)).round(2)),
            key=lambda x: x[1],
            reverse=True,
        )
    )


class BaseCipher(ABC):
    """."""

    @staticmethod
    @abstractmethod
    def encrypt(text: str, key: int) -> str | None:
        """Encrypt `text` with `key`."""

        print("Not implemented yet.")

    @staticmethod
    @abstractmethod
    def decrypt(text: str, key: int) -> str | None:
        """Decrypt `text` with `key`."""

        print("Not implemented yet.")

    @staticmethod
    @abstractmethod
    def crack(text: str) -> str | None:
        """Try to decrypt `text` without key."""

        print("Not implemented yet.")


class CaesarCipher(BaseCipher):
    """Caesar cipher."""

    @staticmethod
    def encrypt(text: str, key: int, alphabet: str = ascii_letters) -> str:
        """Caesar cipher encrypt."""

        key = key % len(alphabet)
        if key == 0:
            return text

        shifted_alphabet = alphabet[key:] + alphabet[:key]
        return text.translate(text.maketrans(alphabet, shifted_alphabet))

    @staticmethod
    def decrypt(text: str, key: int, alphabet: str = ascii_letters) -> str:
        """Caesar cipher decrypt."""

        return CaesarCipher.encrypt(text, -key)

    @staticmethod
    def crack(text: str, alphabet: str = ascii_letters) -> str | None:
        """."""

        wordlist = set()
        for word in Path("resource/words_alpha.txt").read_text().split():
            if len(word) >= 5:
                wordlist.add(word)

        for char in list(frequency_statistic(text).keys())[:3]:
            key = alphabet.index(char) - alphabet.index("e")

            plaintext = CaesarCipher.decrypt(text, key, alphabet)

            real_word = 0
            for word in re.finditer(r"\w{6,13}", plaintext[: len(plaintext) // 100]):
                if word.group(0) in wordlist:
                    real_word += 1
                    if real_word >= 50:
                        print("Caesar key: " + str(key))
                        return plaintext

        return None


class RailfenceCipher(BaseCipher):
    """Rail fence cipher."""

    @staticmethod
    def encrypt(text: str, key: int) -> str:
        """Encrypt `text` with `key`."""

        if key <= 1 or key >= len(text):
            return text

        rows = key
        cycle = rows * 2 - 2
        fence_rows = [""] * rows

        for x in range(len(text)):
            y = rows - 1 - abs(cycle // 2 - x % cycle)
            fence_rows[y] += text[x]

        return "".join(fence_rows)

    @staticmethod
    def decrypt(text: str, key: int) -> str:
        """Decrypt `text` with `key`."""

        cols = len(text)
        rows = key
        cycle = rows * 2 - 2

        result = [""] * cols
        index = 0

        for y in range(rows):
            inc = (cycle - 2 * y) or cycle

            x = y
            while x < cols:
                result[x] = text[index]
                index += 1
                if index >= cols:
                    break
                x += inc
                inc = (cycle - inc) or cycle
            else:
                continue

            break

        return "".join(result)

    @staticmethod
    def crack(text: str) -> str | None:
        """Try to decrypt `text` without key."""

        wordlist = Path("resource/words_alpha.txt").read_text()

        for key in range(2, len(text)):
            plaintext = RailfenceCipher.decrypt(text, key)

            real_word = 0
            for word in re.finditer(r"\w{6,13}", plaintext[: len(plaintext) // 100]):
                if word.group(0) in wordlist:
                    real_word += 1
                    if real_word >= 50:
                        print("Railfence key: " + str(key))
                        return plaintext

        return None


class MixCipher(BaseCipher):
    """Double cipher using caesar cipher and railfence cipher."""

    @staticmethod
    def encrypt(text: str, key1: int, key2: int, alphabet: str = ascii_letters) -> str:
        """Encrypt `text` with `key`."""

        return RailfenceCipher.encrypt(CaesarCipher.encrypt(text, key1, alphabet), key2)

    @staticmethod
    def decrypt(text: str, key1: int, key2: int, alphabet: str = ascii_letters) -> str:
        """Decrypt `text` with `key`."""

        return RailfenceCipher.decrypt(CaesarCipher.decrypt(text, key1, alphabet), key2)

    @staticmethod
    def crack(text: str, alphabet: str = ascii_letters) -> str | None:
        """Try to decrypt `text` using caesar cipher and railfence cipher without key."""

        wordlist = Path("resource/words_alpha.txt").read_text()

        for key2 in range(2, len(text)):
            for char in list(frequency_statistic(text, alphabet).keys())[:3]:
                key1 = alphabet.index(char) - alphabet.index("e")

                plaintext = MixCipher.decrypt(text, key1, key2, alphabet)

                real_word = 0
                for word in re.finditer(
                    r"\w{6,13}", plaintext[: len(plaintext) // 100]
                ):
                    if word.group(0) in wordlist:
                        real_word += 1
                        if real_word >= 50:
                            print("Caesar key: " + str(key1))
                            print("Railfence key: " + str(key2))
                            return plaintext

        return None


class Cipher(BaseCipher):
    """Interface for all cipher."""

    @staticmethod
    def encrypt(
        self: CaesarCipher | RailfenceCipher | MixCipher,
        text: str,
        key: list[int],
        alphabet: str = ascii_letters,
    ) -> str:
        """Encrypt method interface for all cipher."""

        if self is not MixCipher:
            return self.encrypt(text, key[0])

        return self.encrypt(text, key[0], key[1], alphabet)

    @staticmethod
    def decrypt(
        self: CaesarCipher | RailfenceCipher | MixCipher,
        text: str,
        key: list[int],
        alphabet: ascii_letters | None = None,
    ) -> str:
        """Decrypt method interface for all cipher."""

        if self is not MixCipher:
            return self.decrypt(text, key[0])

        return self.decrypt(text, key[0], key[1], alphabet)

    @staticmethod
    def crack(
        self: CaesarCipher | RailfenceCipher | MixCipher | Cipher,
        text: str,
        alphabet: str = ascii_letters,
    ) -> str | None:
        """Crack method interface for all cipher."""

        if self is not Cipher:
            return self.crack(text)

        plaintext = CaesarCipher.crack(text, alphabet)

        if plaintext:
            return plaintext

        if list(frequency_statistic(text, alphabet).keys())[0] != "e":
            plaintext = MixCipher.crack(text)

            if plaintext:
                return plaintext
        else:
            plaintext = RailfenceCipher.crack(text)

            if plaintext:
                return plaintext

        return None
