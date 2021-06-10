from command_handler import CommandHandler
import sys

#COMMANDS
#compiler -l -f C:\Users\VITZ\Desktop\tester.pas
#compiler -l -f C:\Users\VITZ\Desktop\tester.txt
#compiler -l -f C:\Users\Crack\Desktop\test.txt

#compiler -l -d C:\Users\VITZ\Desktop\Тесты
#compiler -l -d C:\Users\VITZ\Desktop\Тесты-2
#compiler -l -d C:\Users\Crack\Desktop\Тесты

#compiler -p -f C:\Users\VITZ\Desktop\tester.txt

#compiler -p -d C:\Users\VITZ\Desktop\Parser

if __name__ == '__main__':
    CommandHandler().executeCommand(sys.argv)