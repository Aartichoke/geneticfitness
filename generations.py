import os
import random
from scipy.spatial import distance
import numpy as np
from operator import attrgetter
import matplotlib.pyplot
from operator import attrgetter

graph = []
A = 1

def main():
    import_data()
    generations = 1000
    mut_pct = .10
    legend = []
    legend.append("A coefficient: %.2f" % A)
    best_fit = 0
    global_best = 0
    best_run = []
    for r in range(0):
        pop = initial_pop(100)
        local_best = []
        for i in range(generations):
            mates = []
            # elitism
            mates.append(max(pop, key=attrgetter('fitness')))
            for x in range(len(pop) // 2):
                # compute proportional fitness
                child1, child2 = random.choices(population=pop, weights=[m.fitness for m in pop], k=2)
                child1.state, child2.state = crossover_ox(child1.state, child2.state)
                child1 = mutate(child1.state, mut_pct)
                child2 = mutate(child2.state, mut_pct)
                mates.append(member(child1))
                mates.append(member(child2))
            local_best.append(max(mates, key=attrgetter('fitness')).fitness)
            pop = mates.copy()
        if max(mates, key=attrgetter('fitness')).fitness > best_fit:
            global_best = max(mates, key=attrgetter('fitness'))
            best_run = local_best
            best_fit = global_best.fitness
    print("Smallest bisection: ", global_best.bisections, global_best.state)
    matplotlib.pyplot.plot(range(generations), best_run, label="Generations vs. Fitnesss")
    matplotlib.pyplot.title("Generational Fitness Results: Two Point Crossover")
    matplotlib.pyplot.ylabel("Best Individual Fitness")
    matplotlib.pyplot.xlabel("Generation")
    matplotlib.pyplot.legend(legend)
    matplotlib.pyplot.draw()
    matplotlib.pyplot.show()

def mutate(child, mut_pct):
    child = child.copy()
    if mut_pct >= np.random.uniform(0, 1):
        i = range(len(child))
        pt1, pt2 = random.sample(i, 2)
        child[pt1], child[pt2] = child[pt2], child[pt1]
    return child

def initial_pop(pop_size=100):
    pop = []
    for r in range(pop_size):
        t = []
        for x in range(1, 41):
            t.append(x)
        random.shuffle(t)
        pop.append(member(t))
    return pop

def import_data(file="graph.txt"):
    if os.path.isfile(file):
        with open(file) as f:
            for line in f:
                l = line.strip()
                if l is not '':
                    l1,l2 = l.split(' ')
                    graph.append([int(l1),int(l2)])
    return



class member:
    def __init__(self, state):
        self.state = state
        self.fitness = self.compute_fitness()

    def compute_fitness(self):
        c = 0
        for s in graph:
            if s[0] in self.state[0:20] and s[1] in self.state[20:40]:
                c += 1
                continue
            if s[0] in self.state[20:40] and s[1] in self.state[0:20]:
                c += 1
                continue
            #if s[1] in self.state[0:19] and s[0] in self.state[20:39]:
            #    c += 1
            #    continue
            #if s[1] in self.state[20:39] and s[0] in self.state[0:19]:
            #    c += 1
        fitness = 323 - (A * c)
        self.bisections = c
        #self.fitness = 1 / (fitness + 10**-14)
        return fitness

    def compute_propfitness(self, pop):
        self.proportional_fitness = self.fitness / sum(m.fitness for m in pop)

def crossover_ox(parent1, parent2):
    par2 = parent2.copy()
    par1 = parent1.copy()

    pt1 = random.randint(0, len(parent1))
    pt2 = random.randint(0, len(parent1))
    # dont use same crossover points
    while pt2 == pt1:
        pt2 = random.randint(0, len(parent1))
    # keep values in order for crossover
    if pt2 < pt1:
        pt1, pt2 = pt2, pt1

    substr = parent1[pt1:pt2]

    i = 0
    for c in substr:
        if c in par2:
            i += 1
            par2.remove(c)
    child1 = par2[0:len(substr)] + substr + par2[len(substr):len(par2)]
    substr = parent2[pt1:pt2]
    i = 0
    for c in substr:
        if c in par1:
            i += 1
            par1.remove(c)
    child2 = par1[0:len(substr)] + substr + par1[len(substr):len(par1)]

    if sum(child1) != 820:
        print(child1)
    if sum(child1) != 820:
        print(child1)
    return child1, child2

if __name__ == '__main__':
    main()
