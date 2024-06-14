import matplotlib.pyplot as plt

def plot_vectors(good_vectors, failed_vectors, q):
    good_norms = [sum(vec) for vec in good_vectors]
    bad_norms = [sum(vec) for vec in failed_vectors]
    # Plot the L1 norms
    plt.figure(figsize=(10, 6))
    plt.scatter(good_norms, [1] * len(good_norms), color='green', label='Good Vectors')
    plt.scatter(bad_norms, [0] * len(bad_norms), color='red', label='Bad Vectors')
    plt.axhline(y=0.5, color='black', linestyle='--')
    plt.xlabel('L1 Norm not absolute value')
    plt.ylabel('Outcome')
    plt.title('L1 Norms not absolute of Vectors: Good vs. Bad')
    plt.legend()
    plt.show()