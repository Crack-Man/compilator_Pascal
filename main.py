from command_handler import CommandHandler

#COMMANDS
#compiler -l -f C:\Users\VITZ\Desktop\tester.pas
#compiler -l -f C:\Users\VITZ\Desktop\tester.txt
#compiler -l -f C:\Users\Crack\Desktop\test.txt

#compiler -l -d C:\Users\VITZ\Desktop\тесты
#compiler -l -d C:\Users\VITZ\Desktop\тесты-2

def console():
    print("Available commands:")
    print()
    print("compiler -l -f [filename]")
    print("compiler -l -d [dirname]")
    command = input(">")
    CommandHandler().executeCommand(command)

if __name__ == '__main__':
    console()