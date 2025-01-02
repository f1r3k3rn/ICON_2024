import csv

from pyswip import Prolog


def load_data_from_csv(csv_file):
    with open(csv_file, mode='r') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            row['kdr'] = float(row['kdr'])
            row['assists'] = int(row['assists'])
            row['headshot_pct'] = int(row['headshot_pct'])
            row['acs'] = int(row['acs'])
            data.append(row)
    return data

def create_prolog_knowledge_base(data, output_file="./pl_files/knowledge_base.pl"):

    with open(output_file, "w") as f:
        f.write("% Fatti: rappresentazione delle statistiche per partita\n")
        for row in data:
            f.write(f"stat({row['game_id']}, '{row['agent']}', {row['kdr']}, {row['assists']}, "
                    f"{row['headshot_pct']}, {row['acs']}, {row['outcome']}, {row['ann']}).\n")

        f.write("\n% Regola: verifica se una partita è stata vinta\n")
        f.write("win(GameID) :- stat(GameID, _, _, _, _, _, 1, _).\n")

        f.write("\n% Regola: verifica se l'esito della partita e la previsione ANN sono concordanti\n")
        f.write("concord(GameID) :- stat(GameID, _, _, _, _, _, Outcome, Outcome).\n")

        f.write("\n% Regola: verifica se tutte le partite con ACS maggiore di un valore sono vinte\n")
        f.write("all_win_above_acs(ACSValue) :- \\+ (stat(GameID, _, _, _, _, ACS, Outcome, _), ACS > ACSValue, Outcome \\= 1).\n")

        f.write("\n% Regola: verifica se la maggior parte delle partite con ACS maggiore di un valore sono vinte\n")
        f.write("""\
                most_win_above_acs(ACSValue) :-
                    findall(GameID, (stat(GameID, _, _, _, _, ACS, 1, _), ACS > ACSValue), Wins),
                    findall(GameID, (stat(GameID, _, _, _, _, ACS, 0, _), ACS > ACSValue), Loses),
                    length(Wins, WinCount),
                    length(Loses, LosesCount),
                    WinCount > LosesCount.
        """)

        f.write("\n% Regola: verifica se la maggior parte delle partite con ACS maggiore di un valore sono state predette come vittorie\n")
        f.write("""\
                  most_win_above_acs_ann(ACSValue) :-
                      findall(GameID, (stat(GameID, _, _, _, _, ACS, _, 1), ACS > ACSValue), Wins),
                      findall(GameID, (stat(GameID, _, _, _, _, ACS, _, 0), ACS > ACSValue), Loses),
                      length(Wins, WinCount),
                      length(Loses, LosesCount),
                      WinCount > LosesCount.
          """)


if __name__ == "__main__":
    data = load_data_from_csv("../datasets/valorant_games_predictions_with_original_values.csv")

    create_prolog_knowledge_base(data)

    prolog = Prolog()
    prolog.consult("./pl_files/knowledge_base.pl")

    print(bool(list(prolog.query("win(22)"))))
    print(bool(list(prolog.query("concord(20)"))))
    print(bool(list(prolog.query("concord(22)"))))
    print(bool(list(prolog.query("all_win_above_acs(350)"))))
    print(bool(list(prolog.query("most_win_above_acs(200)"))))
    print(bool(list(prolog.query("most_win_above_acs_ann(200)"))))
    print(bool(list(prolog.query("most_win_above_acs(150)"))))
    print(bool(list(prolog.query("most_win_above_acs_ann(150)"))))
    print(bool(list(prolog.query("most_win_above_acs(170)"))))
    print(bool(list(prolog.query("most_win_above_acs_ann(170)"))))


