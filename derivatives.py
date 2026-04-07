distances_matrix = np.array([
    [4, 7, 9, 2, 3],
    [1, 0, 5, 6, 8],
    [3, 2, 8, 4, 7],
    [1, 7, 6, 0, 9],
    [2, 5, 7, 9, 0]
])

num_iterations = 250

num_ants = 25

best_distance = float('inf')
best_path = []
best_iteration = -1

for iteration in range(num_iterations):
    ant_paths = []
    ant_distances = []

    # Build solutions for each ant
    for ant in range(num_ants):
        path = ...
        distance = ...
        
        ant_paths.append(path)
        ant_distances.append(distance)

    # ✅ NOW it's safe to use ant_distances
    min_distance_idx = np.argmin(ant_distances)
    if ant_distances[min_distance_idx] < best_distance:
        best_distance = ant_distances[min_distance_idx]
        best_path = ant_paths[min_distance_idx]
        best_iteration = iteration

best_path, best_distance, best_iteration = ant_colony_optimization(num_iterations)

print("Iteration with the best distance:", best_iteration)
