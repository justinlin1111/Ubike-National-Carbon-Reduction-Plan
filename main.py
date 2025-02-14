import random
from custom_exceptions import SurplusEmptyError, DeficitEmptyError

class Station:
    # name -> 站點名稱
    # total -> 總車柱數
    # current_bikes -> 現有車輛
    # required_bikes -> 需求車輛
    # diff -> current_bikes跟required_bikes的差值
    def __init__(self, name, total, current_bikes, required_bikes) -> None:
        self.name = name
        self.total = total
        self.current_bikes = current_bikes
        self.required_bikes = required_bikes
        self.diff = self.current_bikes - self.required_bikes

    def __str__(self):
        return f"Station {self.name}: Current Bikes: {self.current_bikes}, Required Bikes: {self.required_bikes}, Diff: {self.diff}"

def initialize_population(pop_size, station_count):
    population = []
    for _ in range(pop_size):
        chromosome = [random.randint(-10, 10) for _ in range(station_count)]
        population.append(chromosome)
    return population

def fitness(chromosome, stations):
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

def selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    selected = random.choices(population, weights=probabilities, k=2)
    return selected

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome, mutation_rate=0.1):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] += random.randint(-3, 3)  # 隨機調整基因值
    return chromosome
# stations -> 自訂的class所組成的陣列，即[Station1,Station2,...,StationN]
def genetic_algorithm(stations, pop_size=50, generations=100):
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

'''
輸出
調度完的結果
調度花費

to do list:
1.意願函數 假設 100
    車子 100 + 油錢(先不考慮/3.3 * 0.7 ntd/km)
    意願 100% 費用 5
    <=20騎 相反 車載
2.意願不是100討論期望值
    def 意願函數(費用 距離)
4.預測需求:可以使用很多方法 抓真實資料比較有意義 可以抓去年下學期的Ubike使用數量
最後在使用GA或者其他方法來實現調度
5.這樣的話需求就不需要隨機，而可以直接變成一個已知數



'''