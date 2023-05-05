# import numpy as np
from string import ascii_uppercase

# theory_freq = {
#     'E' : 12.49,
#     'T' : 09.28,
#     'A' : 08.04,
#     'O' : 07.64,
#     'I' : 07.57,
#     'N' : 07.23,
#     'S' : 06.51,
#     'R' : 06.28,
#     'H' : 05.05,
#     'L' : 04.07,
#     'D' : 03.82,
#     'C' : 03.34,
#     'U' : 02.73,
#     'M' : 02.51,
#     'F' : 02.40,
#     'P' : 02.14,
#     'G' : 01.87,
#     'W' : 01.68,
#     'Y' : 01.66,
#     'B' : 01.48,
#     'V' : 01.05,
#     'K' : 00.54,
#     'X' : 00.23,
#     'J' : 00.16,
#     'Q' : 00.12,
#     'Z' : 00.09,
# }


def caesar_encrypt(text: str, key: int, alphabet: str = ascii_uppercase) -> str:
    """Caesar cipher (Substitution cipher)"""

    shifted_alphabet = alphabet[key:] + alphabet[:key]
    return text.translate(text.maketrans(alphabet, shifted_alphabet))


def caesar_decrypt(text: str, key: int, alphabet: str = ascii_uppercase) -> str:
    """Caesar cipher (Substitution cipher)"""

    return caesar_encrypt(text, -key, alphabet)

# def frequency_calculate(text: str) -> dict[str, float]:
#     '''
#     Calculate occurrence rate of each character in text
#     '''

#     if not text:
#         return {}

#     char, times = np.unique(list(text), return_counts=True)
#     return dict(zip(char, (times * 100 / len(text)).round(2)))

# def predict_mapping(reality_freq: dict[str, float], theory_freq: dict[str, float]) -> list[list[str, str]]:
#     '''
#     Predict caesar cipher character mapping table by comparing frequency
#     '''

#     if not reality_freq or not theory_freq:
#         return []

#     diff = np.array(np.abs(np.hstack(list(reality_freq.values())) - np.vstack(list(theory_freq.values()))))
#     src = list(theory_freq.keys())
#     dst = list(reality_freq.keys())

#     mapping = []
#     while diff.size != 0:
#         i1, i2 = np.array(np.where(diff == diff.min()))[:,0] # i1 for vstack, i2 for hstack
#         mapping.append([src.pop(i1), dst.pop(i2)])
#         diff = np.delete(diff, i1, axis=0)
#         diff = np.delete(diff, i2, axis=1)
#     return mapping

# def optimize_dev(dev: np.ndarray, alphabet: str = ascii_uppercase) -> np.ndarray:
#     print(dev)
#     print(np.std(dev))

#     optimized_dev = dev.copy()
#     for idx in range(len(optimized_dev)):
#         tmp = optimized_dev.copy()
#         tmp[idx] = (tmp[idx] + len(alphabet)) if (tmp[idx] < 0) else (tmp[idx] - len(alphabet))
#         if np.std(tmp) < np.std(optimized_dev):
#             optimized_dev = tmp

#     if np.array_equal(dev, optimized_dev):
#         return dev
#     else:
#         return optimize_dev(optimized_dev)

# def predict_key(mapping: list[list[str, str]], alphabet: str = ascii_uppercase) -> int:
#     '''
#     Predict caesar cipher encryption key
#     '''

#     dev = np.array([alphabet.index(dst) - alphabet.index(src) for src, dst in mapping])
#     key = np.std(optimize_dev(dev)).astype(int)
#     return key
