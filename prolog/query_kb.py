from pyswip import Prolog
import pandas as pd
from tabulate import tabulate

def carica_dataset(percorso):
    return pd.read_csv(percorso)

def partita_fact(row):
    return f"partita(g{row['game_id']}, '{row['agent']}', {row['kdr']}, {row['assists']}, {row['headshot_pct']}, {row['acs']}, '{row['outcome']}')"

def crea_fatti_prolog(df):
    return [partita_fact(row) for _, row in df.iterrows()]

def definisci_regole():
    return [
        "prec(X, Y) :- partita(X, _, _, _, _, _, _), partita(Y, _, _, _, _, _, _), sub_atom(X, 1, _, 0, ID_X), sub_atom(Y, 1, _, 0, ID_Y), atom_number(ID_X, Num_X), atom_number(ID_Y, Num_Y), Num_X < Num_Y",
        "better(X, Y) :- partita(X, _, _, _, _, ACS_X, _), partita(Y, _, _, _, _, ACS_Y, _), ACS_X > ACS_Y",
        "not_newbie(X) :- partita(X, _, _, _, _, _, _), sub_atom(X, 1, _, 0, ID_X), atom_number(ID_X, Num_X), Num_X > 50",
        "high_kdr(X) :- partita(X, _, KDR, _, _, _, _), KDR > 1.5",
        "high_headshot(X) :- partita(X, _, _, _, Headshot_Pct, _, _), Headshot_Pct > 25",
        "high_assists(X) :- partita(X, _, _, Assists, _, _, _), Assists > 5",
        "astonishing(X) :-  not_newbie(X), (high_kdr(X); high_headshot(X); high_assists(X)), findall(Y, (prec(Y, X), better(X, Y)), BetterGames), length(BetterGames, CountBetter), findall(Y, prec(Y, X), PreviousGames), length(PreviousGames, CountPrevious), CountPrevious > 0, Ratio is CountBetter / CountPrevious, Ratio >= 0.75",
        "normal(X) :-  not_newbie(X), findall(Y, (prec(Y, X), better(X, Y)), BetterGames), length(BetterGames, CountBetter), findall(Y, prec(Y, X), PreviousGames), length(PreviousGames, CountPrevious), CountPrevious > 0, Ratio is CountBetter / CountPrevious, Ratio >= 0.25, Ratio < 0.75",
        "bad(X) :-  not_newbie(X), findall(Y, (prec(Y, X), better(X, Y)), BetterGames), length(BetterGames, CountBetter), findall(Y, prec(Y, X), PreviousGames), length(PreviousGames, CountPrevious), CountPrevious > 0, Ratio is CountBetter / CountPrevious, Ratio < 0.25"
    ]

def aggiungi_fatti_e_regole(prolog, fatti, regole):
    for fatto in fatti:
        prolog.assertz(fatto)
    for regola in regole:
        prolog.assertz(regola)

def esegui_query(prolog, query):
    return list(prolog.query(query))

def stampa_primi_3_result(prolog, query, df):
    results = esegui_query(prolog, query)
    rows = []
    count = 0
    for result in results:
        if count < 3:
            game_id = result["X"]
            game_record = df[df['game_id'] == int(game_id[1:])]
            selected_columns = ['game_id', 'agent', 'kdr', 'assists', 'headshot_pct', 'acs', 'outcome']
            for _, row in game_record[selected_columns].iterrows():
                rows.append(row.tolist())
            count += 1

    headers = ['Game ID', 'Agent', 'KDR', 'Assists', 'Headshot%', 'ACS', 'Outcome']
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def main():
    data_path = "../datasets/valorant_games.csv"
    df = carica_dataset(data_path)

    fatti = crea_fatti_prolog(df)

    prolog = Prolog()

    regole = definisci_regole()

    aggiungi_fatti_e_regole(prolog, fatti, regole)

    queries = {
        "Astonishing games": "astonishing(X)",
        "Normal games": "normal(X)",
        "Bad games": "bad(X)",
        "Games with high KDR": "high_kdr(X)",
        "Games with high headshots": "high_headshot(X)",
        "Games with high assists": "high_assists(X)"
    }

    for description, query in queries.items():
        print(f"\n{description}:")
        stampa_primi_3_result(prolog, query, df)

if __name__ == "__main__":
    main()
