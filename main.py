import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MinMaxScaler

from displayers.plotters import *
from displayers.textual_tables import show_stats_table_text
from pre_processing import utils
from pre_processing.outliners_management import remove_outliners_iqr
from supervised_training.supervised_learning import train_models_with_cv


def preprocess_data(valorant_data, verbose=False):
    selected_columns = valorant_data[['game_id','agent','kdr','assists','headshot_pct','acs','outcome']]

    if verbose:
        plot_column_statistics(selected_columns, ['kdr','assists','headshot_pct','acs'])

    for column in ['kdr','assists','headshot_pct','acs']:
        selected_columns = remove_outliners_iqr(selected_columns, column)

    selected_columns = utils.filter_dataset_by_categories(selected_columns, 'agent', ['Cypher','Killjoy'])
    selected_columns = utils.filter_dataset_by_categories(selected_columns, 'outcome', ['Win','Loss'])

    if verbose:
        plot_donut(selected_columns)
        plot_column_distributions(selected_columns, ['outcome','agent'],['blue', 'orange', 'green', 'red', 'purple'],10)
        plot_column_statistics(selected_columns, ['kdr','assists','headshot_pct','acs'])
        show_stats_table_text(selected_columns)

    selected_columns = utils.convert_strings_to_indices(selected_columns, 'agent')
    selected_columns = utils.convert_strings_to_indices(selected_columns, 'outcome')

    selected_columns.to_csv('./datasets/valorant_games_outliners_removed.csv', index=False)

    return selected_columns

def train_and_predict(processed_dataset, apply_smote=False):
    X = processed_dataset[['agent', 'kdr', 'assists', 'headshot_pct', 'acs']]
    y = processed_dataset['outcome']

    if apply_smote:
        smote = SMOTE()
        X, y = smote.fit_resample(X, y)

    print(f"smote is {apply_smote} the outcome is {y.value_counts()}")

    best_models = train_models_with_cv(X, y)

    dataset_with_predictions = processed_dataset.copy()

    for model in best_models:
        print(f"Best model for {model}: {best_models[model]['best_estimator']}")
        print(f"Best params for {model}: {best_models[model]['best_params']}")
        dataset_with_predictions[model] = best_models[model]["best_estimator"].predict(processed_dataset[['agent', 'kdr', 'assists', 'headshot_pct', 'acs']])

    dataset_with_predictions.to_csv('./datasets/valorant_games_predictions.csv', index=False)
    return dataset_with_predictions

def main():
    raw_dataset = pd.read_csv('./datasets/valorant_games.csv')

    processed_dataset = preprocess_data(raw_dataset)

    scaler = MinMaxScaler(feature_range=(0, 1))

    numeric_columns = processed_dataset.select_dtypes(include=['float64', 'int64']).columns
    numeric_columns = numeric_columns.drop('game_id')
    processed_dataset[numeric_columns] = scaler.fit_transform(processed_dataset[numeric_columns])

    dataset_with_predictions_NO_SMOTE = train_and_predict(processed_dataset, apply_smote=False)
    dataset_with_predictions_SMOTE = train_and_predict(processed_dataset, apply_smote=True)

    dataset_with_predictions_SMOTE.to_csv('./datasets/valorant_games_predictions_SMOTE.csv', index=False)
    dataset_with_predictions_NO_SMOTE.to_csv('./datasets/valorant_games_predictions_NO_SMOTE.csv', index=False)

if __name__ == '__main__':
    main()