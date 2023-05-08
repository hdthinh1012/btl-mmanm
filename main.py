"""."""
from timeit import default_timer as timer
import argparse

from pathlib import Path

from cipher import CaesarCipher, Cipher, MixCipher, RailfenceCipher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    sub_parser = parser.add_subparsers(title="Mode", required=True, dest="mode")

    enc_parser = sub_parser.add_parser("enc", help="Encrypt mode")
    enc_parser.add_argument(
        "cipher", choices=["caesar", "railfence", "mix"], help="Cipher"
    )
    enc_parser.add_argument("key", nargs="+", type=int, help="Cipher key")

    enc_parser.add_argument(
        "--inp",
        type=str,
        default="temp/inp.txt",
        metavar="FILE",
        help="Input file",
    )
    enc_parser.add_argument(
        "--out",
        type=str,
        default="temp/enc.txt",
        metavar="FILE",
        help="Output file",
    )

    dec_parser = sub_parser.add_parser("dec", help="Decrypt mode")
    dec_parser.add_argument(
        "cipher", choices=["caesar", "railfence", "mix"], help="Cipher"
    )
    dec_parser.add_argument("key", nargs="+", type=int, help="Cipher key")

    dec_parser.add_argument(
        "--inp",
        type=str,
        default="temp/enc.txt",
        metavar="FILE",
        help="Input file",
    )
    dec_parser.add_argument(
        "--out",
        type=str,
        default="temp/out.txt",
        metavar="FILE",
        help="Output file",
    )

    crk_parser = sub_parser.add_parser("crk", help="Crack mode")
    crk_parser.add_argument(
        "--cipher", choices=["caesar", "railfence", "mix"], help="Cipher"
    )

    crk_parser.add_argument(
        "--inp",
        type=str,
        default="temp/enc.txt",
        metavar="FILE",
        help="Input file",
    )
    crk_parser.add_argument(
        "--out",
        type=str,
        default="temp/out.txt",
        metavar="FILE",
        help="Output file",
    )

    args = parser.parse_args()

    # print(args)
    # exit()

    inp = Path(args.inp).read_text()

    if args.cipher == "caesar":
        cipher_class = CaesarCipher
    elif args.cipher == "railfence":
        cipher_class = RailfenceCipher
    elif args.cipher == "mix":
        cipher_class = MixCipher
    else:
        cipher_class = Cipher

    if args.mode == "enc":
        out = Cipher.encrypt(cipher_class, inp, args.key)
    elif args.mode == "dec":
        start = timer()
        out = Cipher.decrypt(cipher_class, inp, args.key)
        end = timer()
        print(f"{(end - start) * 1000} miliseconds")
        if args.cipher == "railfence":
            start = timer()
            out = RailfenceCipher.decrypt_2(inp, args.key[0])
            end = timer()
            print(f"{(end - start) * 1000} miliseconds")

    elif args.mode == "crk":
        start = timer()
        out = Cipher.crack(cipher_class, inp)
        end = timer()
        print(f"Crack time: {(end - start) * 1000} miliseconds")

    if out:
        Path(args.out).write_text(out)
