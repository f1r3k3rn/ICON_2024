import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import learning_curve


def plot_column_statistics(df, columns):

    n_cols = len(columns)
    fig, axes = plt.subplots(1, n_cols, figsize=(5 * n_cols, 5))
    fig.suptitle("Distribuzioni: Media, Deviazione Standard, Min, Max", fontsize=16)

    if n_cols == 1:
        axes = [axes]

    for ax, col in zip(axes, columns):
        if col in df.columns:
            col_data = df[col].dropna()
            stats = {
                'Mean': col_data.mean(),
                'Std Dev': col_data.std(),
                'Min': col_data.min(),
                'Max': col_data.max()
            }

            ax.bar(stats.keys(), stats.values(), color=['blue', 'orange', 'green', 'red'])
            ax.set_title(f"Colonna: {col}", fontsize=12)
            ax.set_ylabel("Valori")
            ax.set_xticks(range(len(stats.keys())))
            ax.set_xticklabels(stats.keys(), rotation=45)


            ax.set_ylim(0, max(stats.values()) * 1.1)
        else:
            ax.set_title(f"Colonna: {col} non trovata", fontsize=12)
            ax.axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def plot_donut(valorant_data):
    agent_win_status = valorant_data.groupby(["agent", "outcome"])["outcome"].count().reset_index(name="counts")

    colors = plt.cm.tab10.colors
    outcome_labels = agent_win_status["outcome"].unique()

    fig, ax = plt.subplots(1,2,figsize=(16,8))
    for r, i in enumerate(outcome_labels):
        outcome_status = agent_win_status[agent_win_status["outcome"] == i]
        status_count = len(outcome_status)
        pivot_tables= []
        val = []

        if status_count > 0:
            for index, (agent, value) in enumerate(zip(outcome_status[outcome_status["outcome"] == i]["agent"], outcome_status[outcome_status["outcome"] == i]["counts"])):
                sum_outcome = outcome_status["counts"].sum()
                perc = (value / sum_outcome) * 100
                if perc < 2:
                    outcome_status.loc[outcome_status["agent"] == agent, "agent"] = "Others"
                else:
                    continue

            status_count -= 1

        for _ in range(len(outcome_status)):
            pivot_outcomes = outcome_status.pivot_table(values="counts", index="agent", aggfunc=list)
            vals = np.array([np.sum(x) for x in pivot_outcomes["counts"]])
            val.append((pivot_outcomes.index, vals))

        labels, values = val[r]
        ax[r].pie(values, labels=labels, radius=1-0.2,
                  colors=colors,
                  wedgeprops=dict(width=0.3, edgecolor='w'),
                  textprops={'fontsize': 14, 'fontweight': 'normal'})

        ax[r].pie(values, colors=colors,
                  wedgeprops=dict(width=0.3, edgecolor='w'),
                  textprops={'fontsize': 12},
                  hatch=['O.', '\\', '++'],)
        ax[r].set_title(i, fontsize=20)
    plt.show()

def plot_column_distributions(dataset, columns, colors, min_percentage=2):
    fig, ax = plt.subplots(1, len(columns), figsize=(16, 8))

    if len(columns) == 1:
        ax = [ax]

    for r, column in enumerate(columns):
        column_data = dataset[column]
        value_counts = column_data.value_counts()

        total_count = value_counts.sum()
        value_counts = value_counts.apply(lambda x: x if (x / total_count) * 100 >= min_percentage else 0)
        value_counts["Others"] = total_count - value_counts.sum() if total_count - value_counts.sum() > 0 else 0
        value_counts = value_counts[value_counts > 0]

        labels = value_counts.index
        values = value_counts.values

        ax[r].pie(values, labels=labels, radius=1 - 0.2,
                  colors=colors[:len(labels)],
                  wedgeprops=dict(width=0.3, edgecolor='w'),
                  textprops={'fontsize': 14, 'fontweight': 'normal'})

        ax[r].pie(values, colors=colors[:len(labels)],
                  wedgeprops=dict(width=0.3, edgecolor='w'),
                  textprops={'fontsize': 12},
                  autopct="%1.1f%%")
        ax[r].set_title(f"Distribuzione di {column}", fontsize=20)

    plt.show()


def plot_classification_report(report_str, model_name):
    report_dict = classification_report_from_string(report_str)

    metrics_0 = report_dict['0.0']
    metrics_1 = report_dict['1.0']

    names = ['Precision', 'Recall', 'F1-score']
    values_0 = [metrics_0['precision'], metrics_0['recall'], metrics_0['f1-score']]
    values_1 = [metrics_1['precision'], metrics_1['recall'], metrics_1['f1-score']]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].bar(names, values_0, color=['blue', 'cyan', 'purple'])
    axes[0].set_ylim(0, 1)
    axes[0].set_ylabel('Score')
    axes[0].set_title('Metriche basate sulla sconfitta')

    axes[1].bar(names, values_1, color=['blue', 'cyan', 'purple'])
    axes[1].set_ylim(0, 1)
    axes[1].set_ylabel('Score')
    axes[1].set_title('Metriche basate sulla vittoria')

    fig.suptitle(model_name)
    plt.tight_layout()
    plt.show()

def classification_report_from_string(report_str):
    lines = report_str.split('\n')
    report_dict = {}
    for line in lines[2:4]:
        if line.strip():
            parts = line.split()
            class_name = parts[0]
            precision, recall, f1_score = map(float, parts[1:4])
            report_dict[class_name] = {
                'precision': precision,
                'recall': recall,
                'f1-score': f1_score
            }
    return report_dict

def plot_learning_curves(model, X, y, model_name):
    scoring_metrics = ['f1', 'precision', 'recall']
    titles = ['F1-score Error', 'Precision Error', 'Recall Error']
    colors = [('blue', 'lightblue'), ('green', 'lightgreen'), ('red', 'lightcoral')]

    plt.figure(figsize=(24, 8))

    for i, scoring in enumerate(scoring_metrics):
        train_sizes, train_scores, test_scores = learning_curve(model, X, y, cv=10, scoring=scoring, n_jobs=-1)

        train_errors = 1 - train_scores.mean(axis=1)
        train_std = train_scores.std(axis=1)
        test_errors = 1 - test_scores.mean(axis=1)
        test_std = test_scores.std(axis=1)

        train_sizes_percent = (train_sizes / len(X)) * 100

        plt.subplot(2, 3, i + 1)
        plt.plot(train_sizes_percent, train_errors, label="Train error", color=colors[i][0])
        plt.fill_between(train_sizes_percent, train_errors - train_std, train_errors + train_std, color=colors[i][1], alpha=0.3)
        plt.plot(train_sizes_percent, test_errors, label="Test error", color=colors[i][0], linestyle='dashed')
        plt.fill_between(train_sizes_percent, test_errors - test_std, test_errors + test_std, color=colors[i][1], alpha=0.3)

        plt.title(f'{titles[i]} ({model_name})')
        plt.xlabel('Training Set Size (%)')
        plt.ylabel('Error')
        plt.legend(loc="best")
        plt.grid()

        cell_text = []
        for size, train_err, test_err in zip(train_sizes_percent, train_errors, test_errors):
            cell_text.append([f'{size:.1f}%', f'{train_err:.3f}', f'{test_err:.3f}'])

        plt.subplot(2, 3, i + 4)
        plt.axis('tight')
        plt.axis('off')
        table = plt.table(cellText=cell_text, colLabels=['Training Size (%)', 'Train Error', 'Test Error'], loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(0.8, 0.8)

    plt.tight_layout()
    plt.show()