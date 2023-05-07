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

    # def __frequency_statistic(self: CaesarCipher, text: str) -> dict[str, float]:
    #     """Calculate occurrence rate of each character in text."""

    #     char, times = np.unique(list(text), return_counts=True)
    #     return dict(zip(char, (times * 100 / len(text)).round(2)))

    # def __predict_mapping(self: CaesarCipher) -> list[list[str, str]]:
    #     """Predict mapping table by comparing frequency."""

    #     reality_freq = self.__frequency_statistic()

    #     diff = np.array(
    #         np.abs(
    #             np.hstack(list(reality_freq.values()))
    #             - np.vstack(list(self.__theory_freq.values()))
    #         )
    #     )
    #     src = list(self.__theory_freq.keys())
    #     dst = list(reality_freq.keys())

    #     mapping = []
    #     while diff.size != 0:
    #         i1, i2 = np.array(np.where(diff == diff.min()))[
    #             :, 0
    #         ]  # i1 for vstack, i2 for hstack
    #         mapping.append([src.pop(i1), dst.pop(i2)])
    #         diff = np.delete(diff, i1, axis=0)
    #         diff = np.delete(diff, i2, axis=1)
    #     return mapping

    # def __optimize_dev(self: CaesarCipher, dev: np.ndarray) -> np.ndarray:
    #     """."""
    #     print(dev)
    #     print(np.std(dev))

    #     optimized_dev = dev.copy()
    #     for idx in range(len(optimized_dev)):
    #         tmp = optimized_dev.copy()
    #         tmp[idx] = (
    #             (tmp[idx] + len(self.__alphabet))
    #             if (tmp[idx] < 0)
    #             else (tmp[idx] - len(self.__alphabet))
    #         )
    #         if np.std(tmp) < np.std(optimized_dev):
    #             optimized_dev = tmp

    #     if np.array_equal(dev, optimized_dev):
    #         return dev

    #     return self.__optimize_dev(optimized_dev)

    # def predict_key(self: CaesarCipher) -> int:
    #     """Predict key."""

    #     mapping = self.__predict_mapping()
    #     dev = np.array(
    #         [
    #             self.__alphabet.index(dst) - self.__alphabet.index(src)
    #             for src, dst in mapping
    #         ]
    #     )
    #     return np.std(self.__optimize_dev(dev)).astype(int)

    @staticmethod
    def crack(text: str, alphabet: str = ascii_letters) -> str:
        """."""

        # theory_freq = json.dumps(Path.read_text("resource/char_frequency.json"))

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
            if len(word) >= 3:
                wordlist.add(word)

        for key in range(2, len(text)):
            plaintext = RailfenceCipher.decrypt(text, key)

            real_word = 0
            for word in re.findall(r"\w{3,}", plaintext):
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
