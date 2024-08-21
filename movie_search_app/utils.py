from colorama import Fore, Style, init

def color_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"