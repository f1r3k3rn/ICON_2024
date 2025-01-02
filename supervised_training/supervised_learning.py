from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from displayers.plotters import plot_classification_report, plot_learning_curves


def get_param_grids():
    return {
        'decision_tree': {
            'criterion': ['gini', 'entropy', 'log_loss'],
            'max_depth': [5, 10, 15],
            'min_samples_split': [2, 5, 10],
        },
        'random_forest': {
            'n_estimators': [25, 50, 100],
            'max_depth': [5, 10, 20],
            'min_samples_split': [2, 5, 10],
        },
        'logistic_regression': {
            'penalty': ['l2'],
            'C': [0.001, 0.01, 0.1, 1, 10],
            'solver': ['liblinear', 'saga'],
            'max_iter': [100000, 150000],
        },
        'svm': {
            'C': [0.1,0.5, 1, 2],
            'kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
            'gamma': ['scale', 'auto'],
        },
        'ann': {
            'hidden_layer_sizes': [(20,), (40,), (20, 10), (40,20)],
            'activation': ['logistic', 'relu'],
            'solver': ['sgd', 'adam'],
            'alpha': [0.0001, 0.05],
            'learning_rate': ['constant', 'adaptive'],
            'max_iter': [2000],
        },
    }

def initialize_models():
    return {
        'decision_tree': DecisionTreeClassifier(),
        'random_forest': RandomForestClassifier(),
        'logistic_regression': LogisticRegression(),
        'svm': SVC(),
        'ann': MLPClassifier(),
    }

def train_model_with_cv(model_name, model, param_grid, X_train, y_train):
    print(f"Training {model_name}...")
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid,
                               cv=10, scoring='accuracy', n_jobs=-1, verbose=1)

    grid_search.fit(X_train, y_train)

    print(f"Best parameters for {model_name}: {grid_search.best_params_}")
    print(f"Validation accuracy for {model_name}: {grid_search.best_score_:.4f}\n")

    return {
        'best_estimator': grid_search.best_estimator_,
        'best_params': grid_search.best_params_,
        'validation_score': grid_search.best_score_,
    }

def evaluate_model(model_name, model, X_test, y_test):
    print(f"Evaluating {model_name} on test set...")
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)

    plot_classification_report(report,model_name)

    print(f"Classification report for {model_name} on test set:\n{report}")
    return report

def train_models_with_cv(X, y):

    param_grids = get_param_grids()
    models = initialize_models()

    best_models = {}

    for model_name, model in models.items():
        best_models[model_name] = train_model_with_cv(model_name, model, param_grids[model_name],X,y)

    for model_name, model_info in best_models.items():
        best_model = model_info['best_estimator']
        plot_learning_curves(best_model, X, y , model_name)

    return best_models