from command_handler import CommandHandler
import sys

#COMMANDS
#-l -f C:\Users\VITZ\Desktop\tester.txt
#-l -f C:\Users\Crack\Desktop\test.txt

#-l -d C:\Users\VITZ\Desktop\Lexer
#-l -d C:\Users\VITZ\Desktop\Тесты-2
#-l -d C:\Users\Crack\Desktop\Тесты

#-p -f C:\Users\VITZ\Desktop\tester.txt
#-p -f "C:\Users\Crack\Desktop\parser\14 (code).txt"

#-p -d C:\Users\VITZ\Desktop\Parser
#-p -d C:\Users\Crack\Desktop\parser

#-ps -f C:\Users\VITZ\Desktop\tester.txt
#-ps -f C:\Users\Crack\Desktop\test.txt

#-ps -d C:\Users\VITZ\Desktop\Parser_Stmt
#-ps -d C:\Users\Crack\Desktop\parser_stmt

if __name__ == '__main__':
    CommandHandler().checkCommand(sys.argv)