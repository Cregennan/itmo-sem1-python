import sys
import os

def main():
    argv = sys.argv[1:]

    if len(argv) == 0 or argv[0] == '-':
        exec_from_stdio()
        return
        
    if os.path.isfile(argv[0]) and os.path.exists(argv[0]):
        with open(argv[0], 'r') as file:
            exec_from_lines(file.read().splitlines())
            return
    else:
        print(f'File {argv[0]} does not exist')
        return
        
        
def exec_from_stdio():
    i = 0
    while True:
        line = input()
        if len(line) == 0:
            return
        print(f'{i} {line}')
        i += 1
        
            

def exec_from_lines(lines : list[str]):
    for i in range(len(lines)):
        print(f'{i} {lines[i]}')
    
if __name__ == '__main__': 
    main()