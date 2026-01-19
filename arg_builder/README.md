# Pattern to build a python executable with subcommands

This pattern is to build a python executable which accepts subcommands func1 and func2. These subcommands are implemented within their own individual python file func1.py and func2.py.

We use the argparse module to build the argument list for the python executable.

## main.py
The main entry point into the python executable.

## cli.py
The file contains the main CommandBuilder class which is used by this pattern. This includes the decorator command() and assemble() which generates the argument list. The decorator command() is placed on top of the main entry function to each subcommand.

This also contains a simple Context class which acts as the container for the argparse.Namespace object ie. cli.

## func1.py, func2.py
The subcommands of the python executable.

## Makefile
Provides the help and run targets to test the python executable.