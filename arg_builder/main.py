import typing
from cli import commands, Parser, Context
import func1 # noqa
import func2 # noqa


# function to build list of global arguments.
def global_args(parser: Parser) -> None:
    """Configure default global command line arguments."""

    parser.add_argument(
        "--global1",
        action='store_true',
        help="help for sample global1 argument"
    )
    parser.add_argument(
        "--global2",
        action='store_true',
        help="help for sample global2 argument"
    )


def mydefault_call(ctx: Context) -> None:
    print("Hello mydefault_call()")
    print(f"argument global1 - {ctx.cli.global1}")
    print(f"argument global2 - {ctx.cli.global2}")


# default function to call when no argument provided
default_cfunc = mydefault_call


# The main entry point for the executable
def main(args: typing.Optional[typing.Sequence[str]] = None) -> None:
    # call CommandBuilder.assemble() from cli.py
    # pass the global_args() function to build the global arguments
    # This returns an object of type argparse.ArgumentParser
    # Call ArgumentParser.parse_args(args) to parse the command line arguments
    # https://realpython.com/command-line-interfaces-python-argparse/
    cli = commands.assemble(
        arg_func=global_args
        ).parse_args(args)

    # Create context
    ctx = Context(cli)

    # Get the entry function to the subcommand
    cfunc = getattr(ctx.cli, "cfunc", default_cfunc)
    # Call it.
    cfunc(ctx)
    return


if __name__ == "__main__":
    main()
