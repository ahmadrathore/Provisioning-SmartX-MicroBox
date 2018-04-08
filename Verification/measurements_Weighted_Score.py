def align(array):
    col_size = {}
    for row in array:
        for i, col in enumerate(row):
            col_size[i] = max(col_size.get(i, 0), len(col))
    ncols = len(col_size)
    result = []
    for row in array:
        row = list(row) + [''] * (ncols - len(row))
        for i, col in enumerate(row):
            row[i] = col.ljust(col_size[i])
        result.append(row)
    return result