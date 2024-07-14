#!/usr/bin/python3

PROG_NAME = "tocharcode"
PROG_DESC = "converts a string to comma-separated charcode"
ENCODING  = "utf-8"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog=PROG_NAME,
        description=PROG_DESC)

    parser.add_argument("string", type=str)

    args = parser.parse_args()
    inp = args.string
    out = ",".join([str(ord(c)) for c in inp])[:-1]
    print(out)
