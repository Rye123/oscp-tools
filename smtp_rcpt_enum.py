#!/usr/bin/python3
import lib.prog as prog
import lib.wordlist as wl
import lib.log as log
from base64 import b64encode
from socket import socket, AF_INET, SOCK_STREAM

PROG_NAME = "smtp_rcpt_enum"
PROG_DESC = "Enumerates an SMTP server with RCPT TO against a wordlist."

def auth(ip: str, port: int, username: str, password: str):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((ip, port))
    banner = s.recv(1024)

    # Login
    ub64 = b64encode(username.encode('ascii'))
    pb64 = b64encode(password.encode('ascii'))

    s.send(b"HELO " + username.encode('ascii') + b"\r\n")
    s.recv(1024)
    s.send(b"AUTH LOGIN\r\n")
    s.recv(1024)
    s.send(ub64 + b"\r\n")
    s.recv(1024)
    s.send(pb64 + b"\r\n")
    result = s.recv(1024)
    if b"Authentication failed" in result:
        return None
    return s

def rcpt(s: socket, user: str, domain: str):
    # Send VRFY
    s.send(b"RCPT TO: " + user.encode() + b"@" + domain.encode() + b"\r\n")
    result = s.recv(1024)
    return result

if __name__ == "__main__":
    program = prog.Prog(PROG_NAME, PROG_DESC, [
        prog.Arg(prog.ArgType.POSITIONAL, "ip", arg_val_type=str, arg_help="SMTP server IP"),
        prog.Arg(prog.ArgType.POSITIONAL, "port", arg_val_type=int, arg_help="SMTP server port"),
        prog.Arg(prog.ArgType.POSITIONAL, "user", arg_val_type=str, arg_help="SMTP server user"),
        prog.Arg(prog.ArgType.POSITIONAL, "pass", arg_val_type=str, arg_help="SMTP server pass"),
        prog.Arg(prog.ArgType.POSITIONAL, "domain", arg_val_type=str, arg_help="Email domain"),
        prog.Arg(prog.ArgType.POSITIONAL, "sender", arg_val_type=str, arg_help="Email sender, this is appended to the email domain"),
        prog.Arg(prog.ArgType.POSITIONAL, "wordlist", arg_val_type=str, arg_help="wordlist to test")
        ])
    ip = program.args["ip"]
    port = program.args["port"]
    user = program.args["user"]
    pw = program.args["pass"]
    domain = program.args["domain"]
    sender = program.args["sender"]
    wordlist = wl.Wordlist(program.args["wordlist"]).words

    # Idiot-proofing because I'm an idiot
    if "@" in domain:
        # Allow @ to be in domain
        dom_parts = domain.split("@")
        if len(dom_parts) != 2:
            raise Exception(f"Unexpected domain {domain} (expected @domain.com or domain.com)")
        domain = dom_parts[1]
    if "@" not in sender:
        # Only append the domain if the domain isn't already in the sender email
        sender = sender + "@" + domain

    # Authenticate
    sock = auth(ip, port, user, pw)
    if sock is None:
        print("Failed to login")
        exit(1)

    sock.send(b"MAIL FROM:" + sender.encode("ascii") + b"\r\n")
    result = sock.recv(1024)

    for user in wordlist:
        print(f"{user}: {rcpt(sock, user, domain)}")
