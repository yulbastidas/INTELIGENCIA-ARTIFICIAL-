import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Función de evaluación (fitness)
# -------------------------------
def fitness(board):
    """ Calcula el número de ataques entre reinas. """
    n = len(board)
    attacks = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                attacks += 1
                
    return -attacks  # Se devuelve el negativo porque queremos minimizar los ataques

# -------------------------------
# Funciones de Algoritmo Genético
# -------------------------------

def create_population(size, n):
    """ Crea una población inicial de tableros aleatorios. """
    return [np.random.permutation(n) for _ in range(size)]

def selection(population, fitness_values, num_parents):
    """ Selecciona los mejores individuos basados en su aptitud (fitness). """
    sorted_indices = np.argsort(fitness_values)[-num_parents:]  # Mejores num_parents individuos
    return [population[i] for i in sorted_indices]

def crossover(parent1, parent2):
    """ Cruce de un punto: combina dos padres para generar un hijo. """
    n = len(parent1)
    point = np.random.randint(1, n - 1)  # Punto de cruce
    child = np.concatenate((parent1[:point], parent2[point:]))
    
    # Arreglar duplicados y valores faltantes
    unique_values = set(child)
    missing_values = list(set(range(n)) - unique_values)
    np.random.shuffle(missing_values)
    
    for i in range(n):
        if list(child).count(child[i]) > 1:  # Si hay duplicados
            child[i] = missing_values.pop()  # Reemplazamos por un valor único
    
    return child

def mutation(board, mutation_rate=0.2):
    """ Aplica mutación intercambiando dos posiciones con probabilidad mutation_rate. """
    if np.random.rand() < mutation_rate:
        i, j = np.random.randint(0, len(board), size=2)
        board[i], board[j] = board[j], board[i]
    return board

# -------------------------------
# Algoritmo Genético para N-Reinas
# -------------------------------

def genetic_algorithm(n, population_size=100, generations=500, mutation_rate=0.2):
    """ Algoritmo Genético para resolver el problema de las N-Reinas. """
    
    population = create_population(population_size, n)
    best_fitness_values = []  # Para graficar
    
    for gen in range(generations):
        # Evaluar aptitud de la población
        fitness_values = np.array([fitness(ind) for ind in population])
        
        # Guardar mejor valor para graficar
        best_fitness_values.append(max(fitness_values))
        
        # Si encontramos una solución óptima (sin ataques)
        if max(fitness_values) == 0:
            best_index = np.argmax(fitness_values)
            print(f"Solución encontrada en la generación {gen+1}!")
            return population[best_index], best_fitness_values
        
        # Selección de los mejores padres
        parents = selection(population, fitness_values, population_size // 2)
        
        # Generación de nueva población con crossover y mutación
        new_population = []
        for _ in range(population_size):
            idx1, idx2 = np.random.choice(len(parents), size=2, replace=False)  # Selección de índices
            parent1, parent2 = parents[idx1], parents[idx2]  # Obtener padres
            child = crossover(parent1, parent2)  # Cruzar padres
            child = mutation(child, mutation_rate)  # Aplicar mutación
            new_population.append(child)

        population = new_population  # Reemplazo de la población

    print("No se encontró una solución en el número de generaciones.")
    return None, best_fitness_values

# -------------------------------
# Ejecutar el Algoritmo y Graficar
# -------------------------------

N = 9 # Número de reinas
solution, fitness_history = genetic_algorithm(N)

if solution is not None:
    print("\nTablero solución:", solution)
    board_visual = np.zeros((N, N), dtype=int)
    for i in range(N):
        board_visual[solution[i], i] = 1
    print("\nTablero visual:\n", board_visual)

    # Graficar convergencia del fitness
    plt.figure(figsize=(8, 5))
    plt.plot(fitness_history, marker='o', linestyle='-', color='b', label="Mejor Fitness")
    plt.xlabel("Generaciones")
    plt.ylabel("Fitness (menor es mejor)")
    plt.title("Convergencia del Algoritmo Genético para N-Reinas")
    plt.legend()
    plt.grid()
    plt.show()
