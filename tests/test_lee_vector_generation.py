import random

def lee_distance(u, v, m):
    """Calculate the Lee distance between two vectors u and v in Z_m^n."""
    distance = 0
    for ui, vi in zip(u, v):
        diff = int(ui - vi)   # Calculate the modular difference
        distance += min(diff, m - diff) % q  # Use Lee weight definition
    return distance

def lee_weight(vector,q):
    vector = [component % q for component in vector]
    return sum(min(component, q - component) % q for component in vector)

def generate_lee_error_vectors(n, vector_weight, num_vectors, q, max_tries=10000):
    """
    Generate error vectors of a specific Lee weight vector_weight in Z_q^n.

    Parameters:
    n (int): Length of the vector.
    vector_weight (int): Desired Lee weight.
    num_vectors (int): Number of vectors to generate.
    q (int): The modulus.
    max_tries (int): Maximum number of attempts to generate unique vectors.

    Returns:
    list: A list of generated vectors with the specified Lee weight.
    """
    unique_vectors = set()
    attempts = 0

    while len(unique_vectors) < num_vectors and attempts < max_tries:

        vector = [0] * n
        added_weight = 0
        while added_weight < vector_weight:
            available_indexes = [i for i in range(n) if abs(vector[i]) < q // 2] 
            if not available_indexes:
                print("Ran out of indexes to add weight.")
                break
            index = random.choice(available_indexes)
            vector[index] += 1
            added_weight += 1
        # Randomly invert each coordinate with a 50% probability
        vector = [component if random.random() > 0.5 else -component for component in vector]
        vector = [component % q for component in vector]
        print(vector)
        if lee_weight(vector, q) == vector_weight:
            unique_vectors.add(tuple(vector))
        else:
            print(f"Vector {vector} has Lee weight {lee_weight(vector, q)} instead of {vector_weight}.")
        attempts += 1

    if len(unique_vectors) < num_vectors:
        print("Only generated", len(unique_vectors), "unique error vectors out of", num_vectors, "requested.")

    return list(unique_vectors)

def generate_lee_error_vectors_for_all_weights(n, q, max_weight, num_vectors, max_tries=10000):
    """
    Generate error vectors for each Lee weight from 1 to max_weight in Z_q^n.

    Parameters:
    n (int): Length of the vector.
    q (int): The modulus.
    max_weight (int): Maximum weight to generate vectors for.
    num_vectors (int): Number of vectors to generate for each weight.
    max_tries (int): Maximum number of attempts to generate unique vectors.

    Returns:
    dict: A dictionary where keys are weights and values are lists of generated vectors with the specified Lee weight.
    """
    all_vectors = {}
    for weight in range(1, max_weight + 1):
        all_vectors[weight] = generate_lee_error_vectors(n, weight, num_vectors, q, max_tries)
    return all_vectors


# Example usage for n=11, q=17 and checking Lee weight
n = 11
q = 5
max_weight = 5
num_vectors = 5
all_lee_vectors = generate_lee_error_vectors_for_all_weights(n, q, max_weight, num_vectors)
for weight, vectors in all_lee_vectors.items():
    print(f"Lee weight {weight}:")
    for v in vectors:
        print(v)  # Print the generated Lee weight vectors
        # Verify the Lee weight of the vector
        actual_weight = lee_weight(v, q) 
        assert actual_weight == weight, f"Error: Vector {v} does not have the expected Lee weight {weight}. Actual weight: {actual_weight}."
        