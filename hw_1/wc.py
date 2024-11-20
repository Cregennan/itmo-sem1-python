import os, sys

def main():
    argv = sys.argv[1:]
    if len(argv) > 0:
        read_files(argv)
    else:
        read_stdin()

def read_files(filenames: list[str]):
    total_lines, total_words, total_bytes = 0, 0, 0
    for filename in filenames:
        if not os.path.isfile(filename) or not os.path.exists(filename):
            print(f'File {filename} not found')
            return

        with open(filename, 'r') as file:
            data = file.read()
            lines_count, words_count, bytes_count = stats(data)
            lines_count = lines_count - 1 if lines_count > 0 else 0 # поправка на то, что wc не считает последнюю строку
            total_bytes += bytes_count
            total_lines += lines_count
            total_words += words_count
            print(f'{lines_count:8}{words_count:8}{bytes_count:8} {filename}')

    if len(filenames) > 1:
        print(f'{total_lines:8}{total_words:8}{total_bytes:8} total')


def read_stdin():
    lines = []
    try:
        while True:
            lines.append(input())
    except EOFError:
        pass
    text = '\n'.join(lines) + '\n'
    lines_count, words_count, bytes_count = stats(text)
    print(f'{lines_count:8}{words_count:8}{bytes_count:8}')


def stats(original: str) -> (int, int, int):
    lines = original.splitlines()
    lines_count = len(lines)
    words_count = sum(map(len, map(lambda x: x.split(), lines)))
    bytes_count = len(original)
    return lines_count, words_count, bytes_count

if __name__ == '__main__':
    main()