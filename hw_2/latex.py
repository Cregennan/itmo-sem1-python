from typing import List, Any


def to_latex_table(table: List[List[Any]]) -> str:
    max_row_length = max(map(len, table))
    l = [row + [''] * (max_row_length - len(row)) for row in table]
    row_descr = '\n'.join(map(lambda row: f'\t {" & ".join(map(str, row))} \\\\ \hline', l))
    return f"\\begin{{tabular}}{{ |{'|'.join(['c'] * max_row_length)}| }}  \n \t \hline \n {row_descr} \n\end{{tabular}}"