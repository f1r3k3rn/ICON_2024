def filter_dataset_by_categories(dataset, column_name, categories_to_keep):
    if column_name not in dataset.columns:
        raise ValueError(f"La colonna '{column_name}' non esiste nel dataset.")

    filtered_dataset = dataset[dataset[column_name].isin(categories_to_keep)]

    return filtered_dataset

def convert_strings_to_indices(dataset, column_name):

    if column_name not in dataset.columns:
        raise ValueError(f"La colonna '{column_name}' non esiste nel dataset.")

    unique_values = {value: idx for idx, value in enumerate(dataset[column_name].unique())}
    print(unique_values)
    dataset[column_name] = dataset[column_name].map(unique_values)

    return dataset