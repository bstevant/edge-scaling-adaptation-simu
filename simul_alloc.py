import os, sys
import random
import argparse

if len(sys.argv) <= 7:
    print "INIT_NODE INIT_INSTANCE JOIN_PROBA QUIT_PROBA CHECK_PROBA MAX_RTT MED_RTT GENERATION"
    sys.exit(0)

####################################
##### SIMULATION PARAMETERS

# Initial number of node
INIT_NODE = int(sys.argv[1])

#Initial number of instance
INIT_INSTANCE = int(sys.argv[2])

#Probability for a new node to join
JOIN_PROBA = int(sys.argv[3])

#Probability for a node to quit
QUIT_PROBA = int(sys.argv[4])

#Probability for a node to check service
CHECK_PROBA = int(sys.argv[5])

#Max RTT accepted between client and service
MAX_RTT = int(sys.argv[6])

#Median value for RTT between nodes
MED_RTT = int(sys.argv[7])


####################################
##### GLOBAL VARIABLES

nodes = set()
instances = set()
links = {}
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


# Allocate an instance on node name if no instance found at min. distance rtt
def allocate_instance(name, rtt):
    global nodes, instances, links
    
    if links.has_key(name):
        l = links[name]
    else:
        l = {}
    
    nearest = 100000000
    for i in instances:
        # If node does not know its distance with i ... 
        if not l.has_key(i):
            # ... then select one
            l[i] = select_dest_gaussian(MED_RTT)
        # Keep the nearest instance
        nearest = min(nearest, l[i])

    # If the nearest instance is more than rtt, then allocate instance
    if nearest > rtt:
        instances.add(name)
    links[name] = l
    

def create_node():
    global nodes, instances
    
    # Add node to the set of nodes
    name = gen_node_name()
    nodes.add(name)
    
    allocate_instance(name, MAX_RTT)
    

def print_graph():
    global nodes, instances, links
    
    print "graph G {"
#    print "edge[style=solid, constraint=false];"
    for node in instances:
        print node + " [peripheries=2];"
    for node in nodes:
        if node not in instances:
            for n,qual in links[node].iteritems():
                print node + " -- " + n + " [label=\"" + str(qual) + "\"]"
    print "}"

def calc_satisfaction():
    global nodes, instances, links
    for i in nodes:
        if node not in instances:
            for n,qual in links[node].iteritems():



# Graph construction until INIT_NODE
for i in range(0, INIT_NODE):
    create_node()

s = calc_satisfaction()
print "Nn: " + str(len(nodes)) + "Ni: " + str(len(instances))
