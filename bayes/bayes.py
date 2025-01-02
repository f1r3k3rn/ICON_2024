import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from pgmpy.estimators import HillClimbSearch, K2Score, MaximumLikelihoodEstimator
from pgmpy.models import BayesianNetwork


def load_data(file_path):
    data = pd.read_csv(file_path)
    return data[['agent', 'kdr', 'assists', 'headshot_pct', 'acs', 'outcome']]

def learn_structure(data):
    estimator = HillClimbSearch(data)
    model = estimator.estimate(scoring_method=K2Score(data), max_indegree=6, max_iter=int(1e5))
    return model

def learn_parameters(model, data):
    bayesian_model = BayesianNetwork(model.edges())
    bayesian_model.fit(data, estimator=MaximumLikelihoodEstimator)
    return bayesian_model

def plot_network(model):
    G = nx.DiGraph()
    for edge in model.edges():
        G.add_edge(edge[0], edge[1])

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=12, font_weight='bold', arrows=True)
    plt.title("Learned Bayesian Network")
    plt.show()

def generate_random_example(model, num_samples=1):
    samples = model.simulate(num_samples)
    return samples

def main():
    data = load_data('../datasets/valorant_games_outliners_removed.csv')
    model = learn_structure(data)
    print("Learned structure:", model.edges())

    model = learn_parameters(model, data)
    plot_network(model)

    random_example = generate_random_example(model, num_samples=5)
    print("Random examples:\n", random_example)

    data = pd.DataFrame({
        'agent': [1,0,1],
        'kdr': [0.9,0.8,0.4],
        'headshot_pct': [19,29,22],
    })

    probability_agent = model.predict(data)
    print("Predicted probabilities:\n", probability_agent)

if __name__ == '__main__':
    main()