


def df_to_table(df):
	
	from rich.table import Table

	table = Table()

	for col in df.columns:
		table.add_column(col)

	for i,row in df.iterrows():
		values = []
		for col in df.columns:
			values.append(str(row[col]))
		table.add_row(*values)

	return table
