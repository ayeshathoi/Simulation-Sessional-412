import random
import numpy as np
import matplotlib.pyplot as plt

#####################################################################################################################

def select_standard(candidate_score_list,candidate,n):
    dropped_candidate_index = random.sample(list(range(n)), candidate)
    drop_out_candidate_list = [candidate_score_list[i] for i in dropped_candidate_index]

    criteria = 0
    if drop_out_candidate_list != []:
        criteria = np.max(drop_out_candidate_list)
    return criteria, dropped_candidate_index


#####################################################################################################################
           
def select_top(candidate_score_list,dropped_candidate_index,n):
    selected_index = -1

    for i in range(n):
        if candidate_score_list[i] > criteria:
            if i not in dropped_candidate_index:
                selected_index = i
                break

    if selected_index == -1:
        selected_index = n - 1

    return selected_index

#####################################################################################################################

def plotting(success_rate_list, s):
    plt.figure(figsize=(10, 5))
    plt.title('For n = 100, s = ' + str(s))
    plt.plot(range(100), success_rate_list)
    plt.savefig('task2_' + str(s) + '.png')

#####################################################################################################################
n = 100
selected = [1, 3, 5, 10] # anyone from best, top 3, top 5, top 10
Iteration = 10000
#####################################################################################################################

for num in selected:
    success_rate_list = []

    for candidate in range(n):
        success = 0
        for iteration in range(Iteration):
            candidate_score_list = []

            for i in range(n):
                candidate_score_list.append(random.uniform(0,1))

            criteria, dropped_candidate_index = select_standard(candidate_score_list, candidate, n)
            selected_index = select_top(candidate_score_list,dropped_candidate_index,n)
            top_scorers = sorted(candidate_score_list, reverse=True)[:num] 
            
            if candidate_score_list[selected_index] in top_scorers:
                success += 1

        success_rate_list.append((success / Iteration) * 100)

    plotting(success_rate_list, num)