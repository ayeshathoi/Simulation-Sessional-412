import numpy as np
#####################################################################################################################

def generate_neutron(cumulative_prob):
    random_prob = np.random.uniform(0, 1) 
    neutron_generated_total = 0

    for j in range(4): 
        if random_prob <= cumulative_prob[j]: 
            neutron_generated_total = j 
            break

    return neutron_generated_total

#####################################################################################################################

def print_Gen(n_gen,prob):
    print("Generation -", n_gen)
    print("p[0] =", prob[0]/10000)
    print("p[1] =", prob[1]/10000)
    print("p[2] =", prob[2]/10000)
    print("p[3] =", prob[3]/10000)
    print("p[4] =", prob[4]/10000)
    print("\n")

#####################################################################################################################
    
num_prob        = 4
total           = num_prob + 1
probability     = np.zeros(5)
probabilities   = np.zeros(num_prob)
cumulative_prob = np.zeros(num_prob)

start   = 1
end     = 10
Iter    = 10000

#####################################################################################################################

probabilities[1]    = .2126
probabilities[2]    = .2126 * .5893
probabilities[3]    = .2126 * pow(.5893, 2)
probabilities[0]    = 1 - np.sum(probabilities[1:])

#####################################################################################################################
cumulative_prob[0]  = probabilities[0]

for i in range(1, num_prob):
    cumulative_prob[i] = cumulative_prob[i-1] + probabilities[i]

#####################################################################################################################

for n_gen in range(start, end+1):
    prob = np.zeros(total)

    for iteration in range(Iter):
        next_gen_neutron_number = 1 # start with 1 node root

        for i in range(n_gen):
            current_neutron = next_gen_neutron_number
            next_gen_neutron_number = 0 

            for _ in range(current_neutron):
                next_gen_neutron_number += generate_neutron(cumulative_prob)

        if next_gen_neutron_number <= num_prob:
            prob[next_gen_neutron_number] += 1

    print_Gen(n_gen, prob)
#####################################################################################################################         

    