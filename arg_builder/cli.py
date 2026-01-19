import typing
from collections import namedtuple
import argparse


# An interface class to stand in for the argument parser
# Just used for the type checker
# https://realpython.com/python-protocol/
class Parser(typing.Protocol):
    """Minimal protocol for wrapping argument parser"""

    def set_defaults(self, **kwargs: typing.Any):
        """Set a default value for an argument parser"""

    def add_argument(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> typing.Any:
        """Add an argument to be parsed"""


# https://realpython.com/python-namedtuple/#getting-to-know-namedtuple-in-python
# Creates a named tuple called Command with
# 4 arguments - name, cmd_func, arg_func, cmd_help
Command = namedtuple("Command", "name cmd_func arg_func cmd_help")


# Helper command to obtain the help string from the command data structure
# above.
def get_help(cmd: Command) -> str:
    if cmd.cmd_help is not None:
        return cmd.cmd_help
    if cmd.cmd_func.__doc__:
        return cmd.cmd_func.__doc__
    return ""


# Helper command to go through a Command data structures and
# call the argparser calls to build the argument parser.
def add_command(subparsers: typing.Any, cmd: Command) -> None:
    subparser = subparsers.add_parser(cmd.name, help=get_help(cmd))
    subparser.set_defaults(cfunc=cmd.cmd_func)
    if cmd.arg_func is not None:
        cmd.arg_func(subparser)


class CommandBuilder:
    def __init__(self):
        self._commands = []
        self._names = set()

    # This is a decorator factory function to be used on entry functions to a
    # subcommand.
    # https://www.geeksforgeeks.org/python/decorators-with-parameters-in-python/
    # This is the outer decorator which takes parameters.
    def command(self, name, arg_func=None, cmd_help=None):
        # Check to see if the command with the same name already exists
        if name in self._names:
            raise ValueError(f"{name} already in use")
        # if not, add it
        self._names.add(name)

        # This is the inner decorator. This receives the original function as
        # an argument. Unlike how other decorators are used, we do not create
        # a wrapper function which calls the original function. Instead we
        # just use it to append to the list of Commands and returns the
        # original function ie. we just record the function into the list of
        # commands and do not wrap it.
        def _wrapper(f):
            self._commands.append(
                Command(
                    name=name, cmd_func=f, arg_func=arg_func, cmd_help=cmd_help
                )
            )
            return f

        return _wrapper

    # The main call which goes through the list of Commands and generates the
    # argparser data for the sub commands.
    # This call takes the function for global arguments.
    def assemble(
            self, arg_func: typing.Optional[typing.Callable] = None
    ) -> argparse.ArgumentParser:
        # create a new argparse object.
        parser = argparse.ArgumentParser()
        # if the function to build the global arguments exists,
        # then call it to build it.
        if arg_func is not None:
            arg_func(parser)
        # create subparser object for the subcommand
        subparsers = parser.add_subparsers()
        # go through the list of commands and add each command
        # as a subcommand.
        for cmd in self._commands:
            add_command(subparsers, cmd)
        return parser


# create the commands object which is exported
commands = CommandBuilder()


class Context:
    """CLI context for the python executable"""

    def __init__(self, cli_args: argparse.Namespace):
        self._cli = cli_args

    # https://realpython.com/python-property/
    @property
    def cli(self) -> argparse.Namespace:
        return self._cli
