#!/usr/bin/python3

import urllib.parse

PROG_NAME = "encode_url"
PROG_DESC = "URL encodes a string."
ENCODING  = "utf-8"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog=PROG_NAME,
        description=PROG_DESC)

    parser.add_argument("string", type=str)
    parser.add_argument("-d", "--decode", action="store_true", help="decode a URL-encoded string")
    parser.add_argument("-p", "--spaceplus", action="store_true", help="replace spaces with '+' instead of '%%20'")
    parser.add_argument("-e", "--encodeperiods", action="store_true", help="encode periods as well")

    args = parser.parse_args()
    result = ""

    if args.decode:
        result = urllib.parse.unquote(
            args.string,
            encoding=ENCODING,
            errors="replace")
    else:
        if args.spaceplus:
            result = urllib.parse.quote_plus(
                args.string,
                encoding=ENCODING,
                safe="",
                errors="strict")
        else:
            result = urllib.parse.quote(
                args.string,
                encoding=ENCODING,
                safe="",
                errors="strict")

        if args.encodeperiods:
            result = result.replace(".", "%2E")
    print(result)
        
    
