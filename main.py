from command_handler import CommandHandler

def console():
    print("Available commands:")
    print()
    print("lexer [filename]")
    command = input(">")
    CommandHandler().execute_command(command)

if __name__ == '__main__':
    console()