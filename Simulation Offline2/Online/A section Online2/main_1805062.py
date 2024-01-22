from lcgrand_1805062 import *

output_file = open("out.txt", "w")
filename = "./IOs/io1/in.txt"
inputs = open(filename, "r").read().split()
################################################################################
prob_distrib_demand = []
smalls              = [] 
bigs                = []

trials              = int(inputs[0])
initial_inv_level   = int(inputs[1])
num_months          = int(inputs[2])
num_policies        = int(inputs[3])
num_values_demand   = int(inputs[4])
mean_interdemand    = float(inputs[5])
setup_cost          = float(inputs[6])
incremental_cost    = float(inputs[7])
holding_cost        = float(inputs[8])
shortage_cost       = float(inputs[9])
E_setupCost         = float(inputs[10])
E_incrementalCost   = float(inputs[11])
minlag              = float(inputs[12])
maxlag              = float(inputs[13])
E_minlag            = float(inputs[14])
E_maxlag            = float(inputs[15])

#print(trials, initial_inv_level, num_months, num_policies, num_values_demand, mean_interdemand, setup_cost, incremental_cost, holding_cost, shortage_cost, E_setupCost, E_incrementalCost, minlag, maxlag, E_minlag, E_maxlag)

start = 16

for i in range(start, start + num_values_demand):
    prob_distrib_demand.append(float(inputs[i]))

#print(prob_distrib_demand)
start = start + num_values_demand
count = 0


output_file.write("------Single-Product Inventory System------\n\n")
output_file.write("Initial inventory level: " + str(initial_inv_level) + " items\n\n")
output_file.write("Number of demand sizes: "+ str(num_values_demand) + " \n\n")
output_file.write("Distribution function of demand sizes: ")
for i in range(num_values_demand):
    output_file.write(str(prob_distrib_demand[i]) + " ")
output_file.write("\n\n")
output_file.write("Mean inter-demand time" + str(mean_interdemand) + " months\n\n")
output_file.write("Delivery lag range: " + str(minlag) + " to " + str(maxlag) + " months\n\n")
output_file.write("Express Order lag range: " + str(E_minlag) + " to " + str(E_maxlag) + " months\n\n")
output_file.write("Length of simulation: " + str(num_months) + " months\n\n")
output_file.write("Costs:\n")
output_file.write("K = " + str(setup_cost) + "\n" )
output_file.write("i = " + str(incremental_cost)+ "\n" ) 
output_file.write("h = " + str(holding_cost) + "\n" ) 
output_file.write("pi = " + str(shortage_cost) + "\n")
output_file.write("E_K = " + str(E_setupCost)+ "\n" ) 
output_file.write("E_i = " + str(E_incrementalCost) + "\n\n" ) 
output_file.write("Number of policies : " + str(num_policies) + "\n\n")
output_file.write("Policies:\n")
output_file.write("--------------------------------------------------------------------------------------------------\n")
output_file.write("  Policy       Avg_before_express     Avg_after_express   Expected_express_count\n")
output_file.write("--------------------------------------------------------------------------------------------------\n")

##################################################################################################

def determine_next_event():
    global next_event_type,simulation_time , order_time, demand_time, eval_time, end_time
    min_time_next_event = 1.0e+29
    next_event_type = 0

    if order_time < min_time_next_event:
        min_time_next_event = order_time
        next_event_type = 1
    
    if demand_time < min_time_next_event:
        min_time_next_event = demand_time
        next_event_type = 2
    
    if end_time < min_time_next_event:
        min_time_next_event = end_time
        next_event_type = 3
    
    if eval_time < min_time_next_event:
        min_time_next_event = eval_time
        next_event_type = 4

    simulation_time = min_time_next_event
    

def initialize():
    global simulation_time, last_event_time,order_time, demand_time, eval_time, end_time
    global initial_inv_level, inv_level
    global total_ordering_cost, area_holding, area_shortage
    global avg_cost 
    
    simulation_time    = 0.0

    inv_level           = initial_inv_level
    last_event_time     = 0.0

    total_ordering_cost = 0
    area_holding        = 0.0
    area_shortage       = 0.0

    order_time = 1.0e+30
    demand_time = simulation_time + expon(mean_interdemand)
    eval_time = 0.0
    end_time = num_months



def update_time_stats():
    global last_event_time, simulation_time, inv_level, area_holding, area_shortage
    time_since_last_event = simulation_time - last_event_time
    last_event_time = simulation_time

    if inv_level < 0:
        area_shortage -= time_since_last_event * inv_level
    else:
        area_holding  += time_since_last_event * inv_level

def order_event():
    global inv_level, amount, order_time
    inv_level += amount
    order_time = 1.0e+30

def demand_event():

    global inv_level, demand_time
    inv_level -= random_integer(prob_distrib_demand)
    demand_time = simulation_time + expon(mean_interdemand)

def eval_event(flag):

    global inv_level, smalls, bigs, amount
    global total_ordering_cost, setup_cost, incremental_cost
    global simulation_time, minlag, maxlag, order_time, eval_time
    count = 0
    if flag : 
        if(inv_level < 0):
            amount = -inv_level
            total_ordering_cost += E_setupCost + E_incrementalCost * amount
            order_time = simulation_time + uniform(E_minlag, E_maxlag)
            count = 1
        elif(inv_level < smalls):
                amount = bigs - inv_level
                total_ordering_cost += setup_cost + incremental_cost * amount
                order_time = simulation_time + uniform(minlag, maxlag)
    else : 
        if inv_level < smalls:
            amount = bigs - inv_level
            total_ordering_cost += setup_cost + incremental_cost * amount
            order_time = simulation_time + uniform(minlag, maxlag)
        
    eval_time = simulation_time + 1.0
    return count


def report():
    avg_ordering_cost = total_ordering_cost / num_months
    avg_holding_cost = holding_cost * area_holding / num_months
    avg_shortage_cost = shortage_cost * area_shortage / num_months
    avg_total_cost = avg_ordering_cost + avg_holding_cost + avg_shortage_cost
    avg_cost = avg_total_cost
    #print(avg_total_cost," ", avg_ordering_cost," ", avg_holding_cost," ",  avg_shortage_cost)
    output_file.write("\n")
    
    #output_file.write(format(avg_total_cost, '.2f') + "\t\t\t\t")
    return avg_cost


def final_report(smalls,bigs,after,before,co_nt):
    before  = format(before,'2f')
    after   = format(after,'2f')
    co_nt   = format(co_nt,'2f')
    print(smalls,bigs,before,after,co_nt)
    if bigs < 99:
        output_file.write("\n(" + str(smalls) + ", " + str(bigs) + ")\t\t\t\t")
    else:
        output_file.write("\n(" + str(smalls) + "," + str(bigs) + ")\t\t\t\t")
    # output_file.write(format(before, '.2f') + "\t\t\t\t")
    # output_file.write(format(after, '.2f') + "\t\t\t\t")
    # output_file.write(format(co_nt, '.2f') + "\t\t\t\t")
    # output_file.write("\n")


##################################################################################################
with_e = True
without_e = False
sum_cost = 0
counte = 0
total_cnt = 0
with_sum_cost = 0
for i in range(start, start + num_policies):
    smalls  = int(inputs[start+ count])
    bigs    = int(inputs[start+ count + 1])
    count += 2
    try_trials = trials
    while(try_trials > 0):
        initialize()
        while True:
            determine_next_event()
            update_time_stats()
            if next_event_type == 1:
                order_event()
            elif next_event_type == 2:
                demand_event()
            elif next_event_type == 4:
                eval_event(without_e)
            elif next_event_type == 3:
                avg_cost = report()
                sum_cost += avg_cost
                break
        try_trials -= 1
    before = sum_cost/trials
    try_trials = trials
    sum_cost = 0
    while(try_trials > 0):
        initialize()
        while True:
            determine_next_event()
            update_time_stats()
            if next_event_type == 1:
                order_event()
            elif next_event_type == 2:
                demand_event()
            elif next_event_type == 4:
                cnt = eval_event(with_e)
                counte += cnt
            elif next_event_type == 3:
                avg_cost = report()
                sum_cost += avg_cost
                break
        try_trials -= 1
    after = sum_cost/trials
    co_nt = counte/(num_months*trials)
    counte = 0
    sum_cost = 0
    final_report(smalls,bigs,after,before,co_nt)


##################################################################################################

output_file.write("\n\n--------------------------------------------------------------------------------------------------\n")

