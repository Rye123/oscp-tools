# oscp-tools

This contains a bunch of scripts and tools I'm using as part of the PEN-200 course.

## Attribution
The contents are not all mine, especially those in the `http` directory.
- `http/linux`:
  - `unix-privesc-check`: A Unix privilege escalation checker, found [here](https://pentestmonkey.net/tools/audit/unix-privesc-check)
- `http/windows`:
  - `PowerUp.ps1`: PowerShell script for privilege escalation, found [here](https://github.com/PowerShellMafia/PowerSploit/blob/master/Privesc/PowerUp.ps1)
  - `depends.zip`: DependencyWalker executable for checking dynamically-linked functions, found [here](https://www.dependencywalker.com/).
  - `mimikatz.zip`: Tool for extracting NT hashes, found [here](https://github.com/ParrotSec/mimikatz)
  - `powercat.ps1`: PowerShell script that replicates netcat functionality, found [here](https://github.com/besimorhino/powercat)
- Much of the executable/payload generation scripts replicate code from the PEN-200 course.
  - The reverse shell executables adapt code from [here](https://github.com/izenynn/c-reverse-shell/blob/main/windows.c).
  
## Description
### Directories
- **`http`**: HTTP directory meant as a base directory for a C2 server for downloads.
- **`lib`**: Custom library that the tools depend on. So far, this includes:
  - **`prog`**: Simplified wrapper for `argparse` because I'm too lazy to memorise their syntax.
  - **`wordlist`**: Script to generate a Python list of words from a wordlist, predicting the encoding automatically.

### Tools
- **Generation Tools**: These generate a certain script, executable or DLL. Arguments vary based on the tool. In general, a reverse shell generator requires an IP address and port.
  - **`gen_pwsh_rshell`**: Generates a PowerShell reverse shell, encoded in Base64.
  - **`gen_win_dll_cmd`**: Generates a DLL that, upon attachment by a process, runs the given CMD commands.
  - **`gen_win_exe_cmd`**: Generates an EXE that runs the given CMD commands.
  - **`gen_win_dll_rshell`**: Generates a DLL that, upon attachment by a process, runs the reverse shell.
  - **`gen_win_exe_rshell`**: Generates an EXE that runs the reverse shell.
- **SMTP Enumeration**:
  - **`smtp_vrfy_enum`**: Enumerates an SMTP server, with `VRFY` against a wordlist of potential recipients.
  - **`smtp_rcpt_enum`**: Enumerates an SMTP server, with `RCPT TO` against a wordlist of potential recipients. This requires the username and password for SMTP access.
- **Miscellaneous**:
  - **`encode_url`**: Applies URL encoding on a string, because I'm too lazy to memorise it.
  - **`tocharcode`**: Converts a string to comma-separated charcode, useful for encoding JavaScript XSS payloads.
  - **`table_to_dict`**: A Python library that converts a table into a list of dictionary objects that can be introspected.
