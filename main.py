import argparse

from string import ascii_uppercase
from secrets import randbelow
from cipher.caesar import caesar_encrypt, caesar_decrypt
from cipher.railfence import (
    railfence_encrypt,
    railfence_decrypt,
    railfence_cryptoanalysis,
)


def prompt_mode():
    mode = input("Choose mode:\n1. Encrypt\n2. Decrypt\n3. Analysis\n")
    while mode not in ["1", "2", "3"]:
        mode = input(
            "Invalid input. Choose mode:\n1. Encrypt\n2. Decrypt\n3. Analysis\n"
        )
    return mode


def prompt_cipher():
    cipher = input(
        "Choose cipher:\n1. Caesar\n2. Railfence\n3. Combined (Ceasar + Railfence)\n4. Complex(random 1 in 3 above ciphers)\n"
    )
    while cipher not in ["1", "2", "3", "4"]:
        cipher = input("Invalid input. Choose cipher:\n1. Caesar\n2. Railfence\n")
    return cipher


def prompt_input_path():
    input_path = input("Provide input path:\n")
    return input_path


def prompt_output_path():
    output_path = input("Provide output path:\n")
    return output_path


def prompt_ceasar_key():
    key = input("Provide ceasar key:\n")
    return key


def prompt_railfence_key():
    key = input("Provide railfence key:\n")
    return key


if __name__ == "__main__":
    mode = int(prompt_mode())
    cipher = int(prompt_cipher())
    input_path = prompt_input_path()
    output_path = prompt_output_path()

    if mode == 1:
        if cipher == 1:
            ceasar_key = prompt_ceasar_key()
            with open(input_path, "rt") as f:
                plain_text = f.read()
                cipher_text = caesar_encrypt(plain_text, int(ceasar_key))
                fout = open(output_path, "wt")
                fout.write(cipher_text)
                fout.close()
        if cipher == 2:
            railfence_key = prompt_railfence_key()
            with open(input_path, "rt") as f:
                plain_text = f.read()
                cipher_text = railfence_encrypt(plain_text, int(railfence_key))
                fout = open(output_path, "wt")
                fout.write(cipher_text)
                fout.close()

    if mode == 2:
        if cipher == 1:
            ceasar_key = prompt_ceasar_key()
            with open(input_path, "rt") as f:
                cipher_text = f.read()
                plain_text = caesar_decrypt(cipher_text, int(ceasar_key))
                fout = open(output_path, "wt")
                fout.write(plain_text)
                fout.close()
        if cipher == 2:
            railfence_key = prompt_railfence_key()
            with open(input_path, "rt") as f:
                cipher_text = f.read()
                plain_text = railfence_decrypt(cipher_text, int(railfence_key))
                fout = open(output_path, "wt")
                fout.write(plain_text)
                fout.close()

    if mode == 3:
        if cipher == 1:
            # TODO: Ceasar cipher analysis
            pass

        if cipher == 2:
            with open(input_path, "rt") as f:
                railfence_text = f.read()
                plain_text, key = railfence_cryptoanalysis(railfence_text)

                if key != 0:
                    fout = open(output_path, "wt")
                    fout.write(f"Key: {key}\n")
                    fout.write(plain_text)
                    fout.close()

        if cipher == 3:
            # TODO: Combined cipher analysis
            pass

        if cipher == 4:
            # TODO: Complex cipher analysis
            pass

    print("Done")
