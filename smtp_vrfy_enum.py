#!/usr/bin/python3
import lib.prog as prog
import lib.wordlist as wl
import lib.log as log
from socket import socket, AF_INET, SOCK_STREAM

PROG_NAME = "smtp_vrfy_enum"
PROG_DESC = "Enumerates an SMTP server with VRFY against a wordlist."

def verify(ip: str, port: int, user: str):
        global DEBUG
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((ip, port))
        banner = s.recv(1024)
        # Send VRFY
        s.send(b"VRFY " + user.encode() + b"\r\n")
        result = s.recv(1024)
        return result
	#if b"Recipient address rejected" in result:
	#	return False
	#return True

if __name__ == "__main__":
        program = prog.Prog(PROG_NAME, PROG_DESC, [
                prog.Arg(prog.ArgType.POSITIONAL, "ip", arg_val_type=str, arg_help="SMTP server IP"),
                prog.Arg(prog.ArgType.POSITIONAL, "port", arg_val_type=int, arg_help="SMTP server port"),
                prog.Arg(prog.ArgType.POSITIONAL, "wordlist", arg_val_type=str, arg_help="wordlist to test")
        ])
        ip = program.args["ip"]
        port = program.args["port"]
        wordlist = wl.Wordlist(program.args["wordlist"]).words
        for user in wordlist:
                print(f"{user}: {verify(ip, port, user)}")
