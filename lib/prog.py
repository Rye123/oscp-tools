"""
lib.prog
Framework for fast argparse.

Example:
```
prog = Prog("test", "for testing", [
    Arg(ArgType.POSITIONAL, "asdf", arg_help="this is asdf"),
    Arg(ArgType.POSITIONAL, "two", arg_help="this is second"),
    Arg(ArgType.OPTIONAL_VAL, "optional", "o", arg_help="optional value"),
    Arg(ArgType.OPTIONAL_FLAG, "opt flag", "p", arg_help="opt flag")
])
```
This creates a `Prog` object with the arguments contained as a dictionary in `prog.args`. All necessary help features are generated with `argparse`.
"""


import argparse
from typing import Union, List, Any
from enum import IntEnum

class ArgType(IntEnum):
    POSITIONAL = 0      # program arg
    OPTIONAL_FLAG = 1   # program -arg
    OPTIONAL_VAL  = 2   # program -arg 2

class Arg:
    def __init__(self, arg_type: ArgType, arg_full_name: str, arg_short_name: Union[str, None]=None, arg_val_type: Any=None, arg_help: str=""):
        """
        Defines an argument.
        - arg_type: The type of argument -- positional, optional flag, optional value
        - arg_full_name: The full name of the argument.
        - arg_short_name: The short name of the argument, not needed if positional.
        - arg_val_type: The Python value type of the argument. Not needed if optional flag. str by default.
        - arg_help: Help description for the argument.
        """
        if (not isinstance(arg_full_name, str)) or len(arg_full_name) == 0:
            raise ValueError(f"Arg.__init__: Expected string value for arg_full_name.")
        if arg_type == ArgType.POSITIONAL:
            if arg_short_name is not None:
                raise ValueError(f"Arg.__init__: Expected empty short name for positional argument {arg_full_name}.")
            if arg_val_type is None:
                arg_val_type = str
        else:
            if arg_short_name is None:
                raise ValueError(f"Arg.__init__: Expected short name for optional argument {arg_full_name}.")
            if arg_val_type is None:
                if arg_type == ArgType.OPTIONAL_FLAG:
                    arg_val_type = bool
                else:
                    arg_val_type = str

        self.arg_type = arg_type
        self.arg_val_type = arg_val_type
        self.arg_full_name = arg_full_name
        self.arg_short_name = arg_short_name
        self.arg_help = arg_help
                

class Prog:
    def __init__(self, prog_name: str, prog_desc: str="", args: List[Arg]=None):
        if args is None:
            args = []

        self._parser = argparse.ArgumentParser(prog=prog_name, description=prog_desc)
        for arg in args:
            if arg.arg_type == ArgType.POSITIONAL:
                self._parser.add_argument(arg.arg_full_name, type=arg.arg_val_type, help=arg.arg_help)
            elif arg.arg_type == ArgType.OPTIONAL_FLAG:
                self._parser.add_argument(
                    f"-{arg.arg_short_name}",
                    f"--{arg.arg_full_name}",
                    action="store_true",
                    help=arg.arg_help
                )
            elif arg.arg_type == ArgType.OPTIONAL_VAL:
                self._parser.add_argument(
                    f"-{arg.arg_short_name}",
                    f"--{arg.arg_full_name}",
                    type=arg.arg_val_type,
                    help=arg.arg_help
                )
            else:
                raise ValueError(f"Program.__init__: Unknown argument type {arg.arg_type}")

        namespace = self._parser.parse_args()
        self.args = vars(namespace)
            
