def railfence_encrypt(text: str, key: int) -> str:
    """Rail fence cipher (Transposition cipher)"""

    rows = key
    cycle = rows * 2 - 2
    fence_rows = [''] * rows

    for x in range(len(text)):
        y = rows - 1 - abs(cycle // 2 - x % cycle)
        fence_rows[y] += text[x]

    return ''.join(fence_rows)


def railfence_decrypt(text: str, key: int) -> str:
    """Rail fence cipher (Transposition cipher)"""

    rows = key
    cycle = rows * 2 - 2
    result = [''] * len(text)

    index = -1
    for y in range(rows):
        for x in range(len(text)):
            if (y + x) % cycle == 0 or (y - x) % cycle == 0:
                result[x] = text[++index]

    return ''.join(result)
