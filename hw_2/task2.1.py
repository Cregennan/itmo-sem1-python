from latex import to_latex_table

if __name__ == '__main__':
    test = [
        [1, [4, 5, 6]],
        [2, 'bara', 'bere'],
        ['za', 'tebya', 'kalym', 'otdam']
    ]

    result = to_latex_table(test)
    with open('artifacts/task2.1.tex', 'w') as file:
        file.writelines(result)
