import sys
sys.path.insert(1, './MyFunc')
from arg_parser import line_parser

if __name__ == "__main__":
   line_parser(sys.argv[1:])
