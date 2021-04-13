from command_handler import CommandHandler
from lexer.lexer import Lexer

#COMMANDS
#lexer C:\Users\VITZ\Desktop\tester.pas
#lexer C:\Users\VITZ\Desktop\tester.txt
#lexer C:\Users\Crack\Desktop\test.txt

#lexers C:\Users\VITZ\Desktop\КОД

def console():
    print("Available commands:")
    print()
    print("lexer [filename]")
    print("lexers [dirname]")
    command = input(">")
    CommandHandler().execute_command(command)

if __name__ == '__main__':
    console()