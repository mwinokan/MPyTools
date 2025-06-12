def df_to_table(df):

    from rich.table import Table
    import pandas as pd

    table = Table()

    if isinstance(df.index, pd.MultiIndex):
        multi = True
        for name in df.index.names:
            table.add_column(name)
    else:
        multi = False
        if df.index.name:
            table.add_column(df.index.name)
        else:
            table.add_column("index")

    for col in df.columns:
        table.add_column(col)

    for i, row in df.iterrows():

        values = []

        if multi:
            for name in i:
                values.append(str(name))
        else:
            values.append(str(i))

        for col in df.columns:
            values.append(str(row[col]))
        table.add_row(*values)

    return table
