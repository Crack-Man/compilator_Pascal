from command_handler import CommandHandler
from lexer.lexer import Lexer

#COMMANDS
#lexer C:\Users\VITZ\Desktop\tester.pas


def console():
    print("Available commands:")
    print()
    print("lexer [filename]")
    command = input(">")
    CommandHandler().execute_command(command)

if __name__ == '__main__':
    console()