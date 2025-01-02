def show_stats_table_text(valorant_data):
    na = valorant_data.isna().sum()
    print(f"Valori NaN:\n{na}\n")

    dup = valorant_data.duplicated().sum()
    print(f"Valori duplicati: {dup}\n")