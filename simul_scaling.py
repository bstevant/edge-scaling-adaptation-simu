import os, sys
import random
import argparse

if len(sys.argv) <= 5:
    print "INIT_NODE INIT_INSTANCE INIT_CLIENT MAX_RTT MED_RTT"
    sys.exit(0)

####################################
##### SIMULATION PARAMETERS

# Initial number of node
INIT_NODE = int(sys.argv[1])

#Initial number of instance
INIT_INSTANCE = int(sys.argv[2])

# Initial number of client
INIT_CLIENT = int(sys.argv[3])

#Max RTT accepted between client and service
MAX_RTT = int(sys.argv[4])

#Median value for RTT between nodes
MED_RTT = int(sys.argv[5])

#Probability for a new node to join
#JOIN_PROBA = int(sys.argv[3])

#Probability for a node to quit
#QUIT_PROBA = int(sys.argv[4])

#Probability for a node to check service
#CHECK_PROBA = int(sys.argv[5])



####################################
##### GLOBAL VARIABLES

nodes = set()
instances = set()
clients = set()
links = {}
instance_use = {}
current_n_nodes = 0

####################################
##### GRAPH INIT

# Generate a name nXXX
def gen_node_name():
    global current_n_nodes
    current_n_nodes +=1
    return "n" + str(current_n_nodes)

# Select a value from a Gaussian distribution around median
def select_dest_gaussian(median):
    i = random.randint(1,9)
    #print "- " + str(i)
    if i == 1:
        return random.randint(1,int(median*0.6))
    if (i == 2) or (i == 3):
        p = random.randint(int(median*0.6),int(median*0.9))
        return p
    #
    if (i == 4) or (i == 5) or (i == 6):
        return random.randint(int(median*0.9),int(median*1.1))
    #
    if (i == 7) or (i == 8):
        return random.randint(int(median*1.1),int(median*1.4))
    if i == 9:
        return random.randint(int(median*1.4),int(median*2))

# Select a value from a uniform distribution from 0 to 1.5*median
def select_dest_uni(median):
    i = random.randint(1,4)
    if i == 1:
        return random.randint(1,int(median*0.5))
    if i == 2:
        return random.randint(int(median*0.5), int(median))
    if i == 3:
        return random.randint(int(median), int(median*1.5))
    if i == 4:
        return random.randint(int(median*1.5), int(median*10))
        
# Allocate an instance on node name if no instance found at min. distance rtt
#def allocate_instance(name, rtt):


# Create a node
def create_node():
    global nodes
    
    # Add node to the set of nodes
    name = gen_node_name()
    nodes.add(name)
    return name


# Create a client
def create_client():
    global clients, links
    
    # Add node to the set of nodes
    name = gen_node_name()
    clients.add(name)
    links[name] = {}
    return name


# Select an instance for client c
def select_instance(c):
    global instances, links, instance_use, MED_RTT
    min = 10000000
    selected = ''
    last = ''
    
    # return if there is no instances
    if len(instances) < 1:
        return
    
    #print "Finding instances for " + c
    for i in instances:
        last = i
        # Set latency between c and i
        if not links[c].has_key(i):
            #links[c][i] = select_dest_gaussian(MED_RTT)
            links[c][i] = select_dest_uni(MED_RTT)
        if links[c][i] < min:
            selected = i
            min = links[c][i]
    
    # If no node selected, use the last
    if selected == '':
        selected = last
    
    # Save client usage of selected instance in instance_use
    instance_use[selected].add(c) 
    #print "Found instance " + str(selected) + " at " + str(links[c][selected])


# Scale up or down instances to n
def scale_instances(n):
    global nodes, instances, INIT_NODE
    
    if n > INIT_NODE:
        n = INIT_NODE
    if n < 1:
        n = 1
    if n < len(instances):
        # Select arbitrary instances to becomes nodes
        while len(instances) > n:
            i = instances.pop()
            nodes.add(i)
    elif n > len(instances):
        # Select arbitrary nodes to become instances
        while len(instances) < n:
            i = nodes.pop()
            if not instance_use.has_key(i):
                instance_use[i] = set()
            instances.add(i)


def reset_usage():
    global clients, instance_use
    
    for i in instance_use:
        instance_use[i] = set()
    for c in clients:
        select_instance(c)
    # Remove instance if not used
    for i in instance_use:
        if len(instance_use[i]) == 0:
            instances.discard(i)
            nodes.add(i)

def print_graph():
    global instances, instance_use, links
    
    print "graph G {"
#    print "edge[style=solid, constraint=false];"
    for node in instances:
        print node + " [peripheries=2];"
    for node in clients:
        if node not in instances:
            for n,qual in links[node].iteritems():
                print node + " -- " + n + " [label=\"" + str(qual) + "\"]"
    print "}"

def calc_satisfaction():
    global instances, instances_use, links, MAX_RTT
    violation = 0
    count = 0

    for i in instances:
        for c in instance_use[i]:
            count += 1
            if links[c][i] > MAX_RTT :
                violation += 1
    return count, violation


def calc_average_rtt():
    global instances, instances_use, links
    sum = 0
    count = 0
    rtt = []
    
    for i in instances:
        for c in instance_use[i]:
            count += 1
            sum += links[c][i]
            rtt.append(links[c][i])
    return sum / count
    
def print_report():
    global instances, MAX_RTT
    
    print "############################"
    print "Nb instance: " + str(len(instances))
    l,v = calc_satisfaction()
    print "Links: " + str(l) + " >" + str(MAX_RTT) + ": " + str(v)
    print " "


################################
# Init the topology with initial number of
# nodes, instances and clients
def init_topology(nodes, instances, clients):
    # Create nodes
    for i in range(0, nodes):
        create_node()

    # Create INIT_INSTANCE
    scale_instances(instances)

    # Create INIT_CLIENT clients
    # For each client, select an instance
    for i in range(0, clients):
        c = create_client()
        select_instance(c)


##################################
# Show distribution of RTT until n nodes
def print_rtt_dist(n):
    i = 0
    distribution_variation = []
    while i < n:
        distribution_variation.append(select_dest_uni(MED_RTT))
        i +=1
    print distribution_variation


##################################
# Show number of SLA violation
# while scaling up instances by one until n 
def print_scaling_vs_violation(n):
    i = 0
    violation_variation = []
    while i < n:
        l,v = calc_satisfaction()
        violation_variation.append(v)
        i+=1
        scale_instances(i)
        reset_usage()
    print violation_variation


##################################
# Adaptation strategy 1 : Semi-Dichotomous
# Increase by n until violation = 0
# Decrease by n-1 until violation != 0
# Stop when step = 0

def adapt_scaling_dichotomous(step):
    global instances
    last_v = -1
    violation_variation = []
    inst_variation = []
    step_variation = []
    avg_rtt_variation = []
    
    while step != 0:
        #print_report()
        l,v = calc_satisfaction()
        violation_variation.append(v)
        inst_variation.append(len(instances))
        step_variation.append(step)
        avg_rtt_variation.append(calc_average_rtt())
        
        if v > 0:
            if last_v == 0:
                step -= 1
            scale_instances(len(instances)+step)
        else:
            if last_v > 0:
                step -= 1
            scale_instances(len(instances)-step)
        reset_usage()
        last_v = v
    #print violation_variation
    print inst_variation
    #print step_variation
    print avg_rtt_variation


##################################
# Adaptation strategy 2 : Dichotomous
# Increase by n until violation = 0
# Decrease by n/2 until violation != 0
# Stop when step = 0

def adapt_scaling_dichotomous2(step, factor):
    global instances
    last_v = -1
    violation_variation = []
    inst_variation = []
    step_variation = []
    avg_rtt_variation = []
        
    while step > 1:
        print_report()
        l,v = calc_satisfaction()
        violation_variation.append(v)
        inst_variation.append(len(instances))
        step_variation.append(step)
        avg_rtt_variation.append(calc_average_rtt())
        if v > 0:
            if last_v == 0:
                step = int(step/factor)
            scale_instances(len(instances)+step)
        else:
            if last_v > 0:
                step = int(step/factor)
            scale_instances(len(instances)-step)
        reset_usage()
        last_v = v
    print violation_variation
    print inst_variation
    #print step_variation
    #print avg_rtt_variation


##################################
# Scenario showing dichotomous adaptation
# Increase by n until violation = 0
# Decrease by n/2 until violation != 0
# Stop when step = 0


def scenario_scaling_dichotomous2(step, factor):
    global instances, clients
    
    scenario_nb_client = [INIT_CLIENT * 4, INIT_CLIENT * 2]
    scenario_steps = [ 150 , 300 ]
    iter = 500
    last_v = -1
    violation_variation = []
    inst_variation = []
    step_variation = []
    avg_rtt_variation = []
    client_variation = []

    while iter > 1:
        l,v = calc_satisfaction()
        violation_variation.append(v)
        inst_variation.append(len(instances))
        step_variation.append(step)
        avg_rtt_variation.append(calc_average_rtt())
        client_variation.append(len(clients))
        if v > 0:
            if last_v == 0:
                step = int(step/factor)
            scale_instances(len(instances)+step)
        else:
            if last_v > 0:
                step = int(step/factor)
            scale_instances(len(instances)-step)
        reset_usage()
        last_v = v
        iter -=1
        
        i = -1
        try:
            i = scenario_steps.index(iter)
        except ValueError:
            i = -1
        if i != -1:
            for i in range(0, scenario_nb_client[i]):
                c = create_client()
            reset_usage()
            print_report()
            step = 50
        
    print violation_variation
    print inst_variation
    print client_variation


init_topology(INIT_NODE, INIT_INSTANCE, INIT_CLIENT)
# print_rtt_dist(INIT_NODE)
# print_scaling_vs_violation(INIT_NODE)


sla = MED_RTT / MAX_RTT
init_inst_dicho = int(INIT_CLIENT * sla * 0.05)
#print init_inst_dicho
#adapt_scaling_dichotomous(init_inst_dicho)
#adapt_scaling_dichotomous2(init_inst_dicho, 1.2)
#scale_instances(1)
#reset_usage()

#adapt_scaling_dichotomous(1)
#adapt_scaling_dichotomous(INIT_CLIENT/2)
#adapt_scaling_dichotomous2(INIT_CLIENT/2, 1.5)

scenario_scaling_dichotomous2(INIT_CLIENT/2, 1.5)
