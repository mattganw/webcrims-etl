from colorama import init, Fore, Style

"""
Colorama module used to print colored text to the terminal
"""

def color(text, c) -> str:
    init(autoreset=True)
    return f"{c}{text}{Style.RESET_ALL}"
