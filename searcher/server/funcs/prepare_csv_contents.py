async def prepare_csv_contents(contents: list[str]):
    contents[0] = contents[0].replace('\ufeff', '')
    requests_data = []
    error_rows = []
    for row in contents:
        try:
            if '"' in row:
                row = row.replace('"', "", 1)
                row_values = row.strip().split('",', 1)
                row_values[1] = int(row_values[1])
            else:
                row_values = row.strip().split(",", 1)
                row_values[1] = int(row_values[1])
            requests_data.append(row_values)
        except (ValueError, TypeError, IndexError):
            error_rows.append(row)
    for r in requests_data:
        if r[0].isdigit():
            print(r[0])
    return requests_data, error_rows