# Subcommand func1


from cli import commands, Context


# function to build the argument list for subcommand func1
def _arg_func1(parser):
    parser.add_argument(
        "--setup",
        help="Run setup for func1"
    )


# The decorator which ends up adding subcommand func1 to the list of Commands
# The function below is called when the func1 subcommand is executed.
@commands.command(name="func1", cmd_help="Run Function 1", arg_func=_arg_func1)
def func1(ctx: Context) -> None:
    """ Call Func1 """
    print("Hello func1()")
    print(f"argument global1 - {ctx.cli.global1}")
    print(f"argument global2 - {ctx.cli.global2}")
    print(f"argument setup - {ctx.cli.setup}")
