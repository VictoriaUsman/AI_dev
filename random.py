import random

TARGET_PHRASE = "Hello, World"
POPULATION_SIZE = 100
MUTATION_RATE = 0.01

def generate_population():  
  population = []
  for _ in range(POPULATION_SIZE):
    individual = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABDEFGHIJKLMNOPQRSTUVWXYZ ,.! ')for _ in range(len(TARGET_PHRASE)))
    population.append(individual)
  return population

generate_population()

def calculate_fitness(individual):
  score = 0
  for i in range(len(TARGET_PHRASE)):
    if individual[i] == TARGET_PHRASE[i]:
      score += 1
  return score

calculate_fitness(TARGET_PHRASE)

def select_parents(population):
  parents = []
  for _ in range(2):
    parents.append(max(population, key=calculate_fitness))
  return parents

def crossover(parents):
  offspring = ''
  crossover_point = random.randint(1, len(TARGET_PHRASE) - 1)
  for i in range(len(TARGET_PHRASE)):
    if i < crossover_point:
      offspring += parents[0][i]
    else:
      offspring += parents[1][i]
  return offspring

crossover(select_parents(generate_population()))
