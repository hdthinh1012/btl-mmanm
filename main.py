import argparse

from string import ascii_uppercase
from secrets import randbelow
from cipher.caesar import caesar_encrypt, caesar_decrypt
from cipher.railfence import railfence_encrypt, railfence_decrypt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--enc", nargs="?", type=argparse.FileType('rt'), const="temp/inp.txt", metavar="FILE", help="Encrypt from input file")
    parser.add_argument("--dec", nargs="?", type=argparse.FileType('wt'), const="temp/out.txt", metavar="FILE", help="Decrypt to output file")

    parser.add_argument("--caesar", type=str, default="temp/caesar.txt", metavar="FILE", help="Caesar cipher encrypted file")
    parser.add_argument("--railfence", type=str, default="temp/railfence.txt", metavar="FILE", help="Rail Fence cipher encrypted file")

    args = parser.parse_args()

    if args.enc:
        with (
            open(args.caesar, "wt") as f1,
            open(args.railfence, "wt") as f2
        ):
            plain_text = args.enc.read()
            f1.write(caesar_encrypt(plain_text, key=randbelow(26)))
            f2.write(railfence_encrypt(plain_text, key=randbelow(len(plain_text))))

    if args.dec:
        with (
            open(args.caesar, "rt") as f1,
            open(args.railfence, "rt") as f2
        ):
            caesar_text = f1.read()
            railfence_text = f2.read()
            for k in range(len(caesar_text)):
                if (caesar_text[k].isalpha() and railfence_text[k].isalpha()):
                    args.dec.write(caesar_decrypt(caesar_text, key=(ord(caesar_text[k]) - ord(railfence_text[k]))))
                    break
