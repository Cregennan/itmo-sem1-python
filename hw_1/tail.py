import os, sys

def main():
    argv = sys.argv[1:]
    if len(argv) == 0:
        return_from_stdio()
    else:
        return_from_filenames(argv)
        
        
def return_from_stdio():
    lines = []
    while True:
        line = input()
        if len(line) == 0 or line == '':
            break
        lines.append(line)
    print('\n'.join(lines[-17:]))
    
    
def return_from_filenames(names: list[str]):
    for name in names:
        if os.path.isfile(name) and os.path.exists(name):
            with open(name, 'r') as file:
                print(f'==> {name} <==')
                print('\n'.join(file.read().splitlines()[-10:]))
        else:
            print(f'{name}: No such file')
            
            
if __name__ == '__main__':
    main()