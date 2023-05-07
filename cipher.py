"""Cipher module."""

from __future__ import annotations

import json
import re

from abc import ABC, abstractmethod
from pathlib import Path
from string import ascii_letters

import numpy as np


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

        if key == 0:
            return text

        shifted_alphabet = alphabet[key:] + alphabet[:key]
        return text.translate(text.maketrans(alphabet, shifted_alphabet))

    @staticmethod
    def decrypt(text: str, key: int, alphabet: str = ascii_letters) -> str:
        """Caesar cipher decrypt."""

        return CaesarCipher.encrypt(text, -key)

    @staticmethod
    def crack(text: str, alphabet: str = ascii_letters) -> str:
        """."""

        wordlist = set()
        for word in Path("resource/words_alpha.txt").read_text().split():
            if len(word) >= 5:
                wordlist.add(word)

        for key in range(len(alphabet)):
            plaintext = CaesarCipher.decrypt(text, key)

            real_word = 0
            for word in re.findall(r"\w{5,}", plaintext):
                if word in wordlist:
                    real_word += 1
                    if real_word >= 100:
                        return plaintext

        print("Failed to crack")

        return None


class RailfenceCipher(BaseCipher):
    """Rail fence cipher."""

    @staticmethod
    def encrypt(text: str, key: int) -> str:
        """Encrypt `text` with `key`."""

        if key == 0:
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

        if key == 0:
            return text

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

    @staticmethod
    def crack(text: str) -> str | None:
        """Try to decrypt `text` without key."""

        wordlist = set()
        for word in Path("resource/words_alpha.txt").read_text().split():
            if len(word) >= 5:
                wordlist.add(word)

        for key in range(2, len(text)):
            plaintext = RailfenceCipher.decrypt(text, key)

            real_word = 0
            for word in re.findall(r"\w{5,}", plaintext):
                if word in wordlist:
                    print(word)
                    real_word += 1
                    if real_word >= 100:
                        return plaintext

        print("Failed to crack")

        return None


class MixCipher(BaseCipher):
    """Double cipher using caesar cipher and railfence cipher."""


class Cipher(BaseCipher):
    """Factory class for all cipher."""
