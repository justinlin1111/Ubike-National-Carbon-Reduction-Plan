import random

# GA main function
def genetic_algorithm(
    stations,       # 自訂的class所組成的陣列，即[Station1,Station2,...,StationN]
    pop_size=50,    # how many populations are generated
    generations=100 # 迭代次數
):
    population = initialize_population(pop_size, len(stations))
    for _ in range(generations):
        # 評估適應度
        fitness_scores = [fitness(chromo, stations) for chromo in population]
        new_population = []
        for _ in range(pop_size // 2):
            # 選擇
            parent1, parent2 = selection(population, fitness_scores)
            # 交叉
            child1, child2 = crossover(parent1, parent2)
            # 變異
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])
        population = new_population
    # 返回最佳解
    best_solution = max(population, key=lambda chromo: fitness(chromo, stations))
    return best_solution

# generate the first generation
def initialize_population(
    pop_size,       # how many populations are generated
    station_count   # the amount of the stations in the population
):
    population = []
    for _ in range(pop_size):
        chromosome = [random.randint(-10, 10) for _ in range(station_count)]
        population.append(chromosome)
    return population

# function that estimate the score of population
def fitness(
    chromosome, # a candidate in population
    stations    # 自訂的class所組成的陣列，即[Station1,Station2,...,StationN]
):
    total_diff = 0
    total_cost = 0
    for gene, station in zip(chromosome, stations):
        # 計算差值
        # 這邊要重新設計
        diff = abs(station.current_bikes + gene - station.required_bikes)
        total_diff += diff
        # 計算調度成本
        cost = abs(gene) * 5  # 假設每調度一輛車的成本為5
        total_cost += cost
    return -total_diff - total_cost  # 適應度越高越好

# function that choose two parents according to the fitness score
def selection(
    population,     # array of all candidates
    fitness_scores  # array of the scores given by fitness function
):
    total_fitness = sum(fitness_scores)                                     # total score
    probabilities = [score / total_fitness for score in fitness_scores]     # array of all probabilaties
    selected = random.choices(population, weights=probabilities, k=2)       # choose two cadidates as parents
    return selected

# generate two childs from two parents
def crossover(
    parent1,    # candidate 1
    parent2     # candidate 2
):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# the function that apply mutations
def mutate(
    chromosome,         # candidate that could be apply mutation
    mutation_rate=0.1   # the chance to apply mutation
):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] += random.randint(-3, 3)  # 隨機調整基因值
    return chromosome