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
    def crack(text: str, alphabet: str = ascii_letters) -> str | None:
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
    def decrypt_2(text: str, key: int, lens: int = -1) -> str:
        """
        N: key
        L: len(text)
        """
        if lens == -1:
            lens = len(text)
        
        #
        # Ideal:
        # L = K * 2 * (N - 1)
        #

        matrix = []
        dummy_text = text

        k = len(text) // (2 * (key - 1))
        if k * 2 * (key - 1) < len(text):
            k += 1
            # Not perfect case
            # Solve: L + y = N + (N - 1) * x
            x = 1
            while x * (key - 1) < len(text) - key:
                x += 1
            y = x * (key - 1) + key - len(text)
            if x % 2 == 1:
                matrix.append(dummy_text[0:k])
                dummy_text = dummy_text[k:]
                for i in range(0, y - 1):
                    matrix.append(dummy_text[0:2*k-1])
                    dummy_text = dummy_text[2*k-1:]
                for i in range(0, key - y - 1):
                    matrix.append(dummy_text[0:2*k])
                    dummy_text = dummy_text[2*k:]
                matrix.append(dummy_text)
            else:
                matrix.append(dummy_text[0:k])
                dummy_text = dummy_text[k:]
                for i in range(0, key - y - 1):
                    matrix.append(dummy_text[0:2*k-1])
                    dummy_text = dummy_text[2*k-1:]
                for i in range(0, y - 1):
                    matrix.append(dummy_text[0:2*k-2])
                    dummy_text = dummy_text[2*k-2:]
                matrix.append(dummy_text)

        else:
            # Perfect case
            matrix.append(dummy_text[0:k])
            dummy_text = dummy_text[k:]
            while len(dummy_text) > k:
                matrix.append(dummy_text[0:2*k])
                dummy_text = dummy_text[2*k:]
            matrix.append(dummy_text)
        # print(matrix)

        idx = 0
        runner = 0
        reversed = False
        result = []
        while idx < lens:
            if len(matrix[runner]) != 0:
                result += matrix[runner][0]
                matrix[runner] = matrix[runner][1:]
                idx += 1
            if runner == 0 and reversed or runner == key - 1 and not reversed:
                reversed = not reversed
            if reversed:
                runner -= 1
            else:
                runner += 1
            # print(result)
        # print("".join(result))
        return "".join(result)


    @staticmethod
    def crack(text: str) -> str | None:
        """Try to decrypt `text` without key."""

        wordlist = set()
        for word in Path("resource/words_alpha.txt").read_text().split():
            if len(word) >= 5:
                wordlist.add(word)

        real_word_record = -1
        current_key = -1
        for key in range(2, len(text)):
            plaintext = RailfenceCipher.decrypt_2(text, key)
            real_word = 0
            for word in re.findall(r"\w{3,}", plaintext):
                if word.lower() in wordlist:
                    # print(word)
                    real_word += 1
                    if real_word >= real_word_record:
                        real_word_record = real_word
                        current_key = key
            if real_word_record - real_word > 1000:
                # The real word count is decreasing
                break
            print(f"Trying key {key}, count {real_word} english words")
        print(f"Railfence key: {current_key}, found {real_word_record} english words in plaintext after decryption")

        if real_word_record < 1000:
            print("Failed to crack")
            return None
        return RailfenceCipher.decrypt(text, current_key)


class MixCipher(BaseCipher):
    """Double cipher using caesar cipher and railfence cipher."""

    @staticmethod
    def encrypt(text: str, key1: int, key2: int, alphabet: str = ascii_letters) -> str:
        """Encrypt `text` with `key`."""

        return RailfenceCipher.encrypt(CaesarCipher.encrypt(text, key1, alphabet), key2)

    @staticmethod
    def decrypt(text: str, key1: int, key2: int, alphabet: str = ascii_letters) -> str:
        """Decrypt `text` with `key`."""

        return CaesarCipher.decrypt(RailfenceCipher.decrypt(text, key2), key1, alphabet)

    @staticmethod
    def crack(text: str) -> str | None:
        """Try to decrypt `text` using caesar cipher and railfence cipher without key."""

        return ""

        print("Failed to crack")

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

        plaintext = RailfenceCipher.crack(text)

        if plaintext:
            return plaintext

        plaintext = MixCipher.crack(text)

        if plaintext:
            return plaintext

        return None
