import pandas as pd

def replace_scaled_values_with_original(predictions_path, original_path, output_path):
    predictions_df = pd.read_csv(predictions_path)
    original_df = pd.read_csv(original_path)

    merged_df = predictions_df.merge(original_df, on='game_id', suffixes=('_scaled', '_original'))

    columns_to_replace = ['agent', 'kdr', 'assists', 'headshot_pct', 'acs', 'outcome']

    for column in columns_to_replace:
        merged_df[column + '_scaled'] = merged_df[column + '_original']

    merged_df = merged_df.drop(columns=[col + '_original' for col in columns_to_replace])
    merged_df = merged_df.rename(columns={col + '_scaled': col for col in columns_to_replace})


    ann_columns = ['game_id'] + columns_to_replace + ['ann']
    ann_df = merged_df[ann_columns]

    ann_df['ann'] = [int(i) for i in ann_df['ann']]

    ann_df.to_csv(output_path, index=False)


if __name__ == "__main__":

    replace_scaled_values_with_original(
        '../datasets/valorant_games_predictions_NO_SMOTE.csv',
        '../datasets/valorant_games_outliners_removed.csv',
        '../datasets/valorant_games_predictions_with_original_values.csv'
    )

