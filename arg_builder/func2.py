from cli import commands, Context


def _arg_func2(parser):
    parser.add_argument(
        "--store",
        help="store for func2"
    )


@commands.command(name="func2", cmd_help="Run Function 2", arg_func=_arg_func2)
def func2(ctx: Context) -> None:
    """ Call Func2 """
    print("Hello Function 2 - func2()")
    print(f"argument global1 - {ctx.cli.global1}")
    print(f"argument global2 - {ctx.cli.global2}")
    print(f"argument store - {ctx.cli.store}")
