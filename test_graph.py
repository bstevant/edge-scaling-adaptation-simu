#!/usr/bin/python


import os, sys
import random
import argparse

graph = {'n1': [], 
         'n2': [('n1', 0)] }

current_node_name = 'b'

instances = set(['a'])

link_random_pattern = [ 100, 150, 200, 250, 300, 400, 500, 600, 800, 1000 ]
link_random = []
max_hop = 0
current_n_nodes = 2

def init_vars():
    global graph, current_node_name, instances, link_random, link_random_pattern, max_link
    graph = {'n1': [], 
             'n2': [('n1', max_link / 2 + 1)] }

    current_node_name = 'b'

    instances = set(['n1'])

    link_random_pattern = [ 100, 150, 200, 250, 300, 400, 500, 600, 800, 1000 ]
    link_random = []

def gen_node_name():
    global current_n_nodes
    current_n_nodes +=1
    return "n" + str(current_n_nodes)

# Is there an instance (aka a service) near from node n at distance < (MAX_LINK-l)
# This predicate iterates over all the graph, complexity variable of number of node and MAX_LINK
# Prune if h > max_hop
# TODO: ml is fixed, calculation should be done better
def near_instance_found(n, l, ml, h):
    global graph, instances
    found = False
    #found = []
    
    #if h > max_hop:
    #    return found
    
    if l > ml:
        return found
    
    for p, link in graph[n]:
        if (p in instances) and (link+l <= ml):
            #print n + p + " " + str(link+l) + " " + str(ml)
            found = True
            #found.append(p)
        else:
            found |= near_instance_found(p,l+link, ml, h+1)
            continue
    return found


# Select a distance to the node based on maxl
# Simple solution => uniform random
def select_dest_uniform(maxl):
    return random.randint(1,maxl)

# Select a distance to the node based on maxl
# More elaborate solution => gaussian around meanl
# TODO : look at quartiles
def select_dest_gaussian(meanl):
    i = random.randint(1,9)
    #print "- " + str(i)
    if i == 1:
        return random.randint(1,int(meanl*0.6))
    if (i == 2) or (i == 3):
        p = random.randint(int(meanl*0.6),int(meanl*0.9))
        return p
    #
    if (i == 4) or (i == 5) or (i == 6):
        return random.randint(int(meanl*0.9),int(meanl*1.1))
    #
    if (i == 7) or (i == 8):
        return random.randint(int(meanl*1.1),int(meanl*1.4))
    if i == 9:
        return random.randint(int(meanl*1.4),int(meanl*2))


def select_parents(n):
    # Random selection
    return random.sample(graph.keys(), min(len(graph.keys()),n))
    # TODO: Reputation based selection

# Create a node with n parents and link qual random 1 to max link maxl
# Add node to instances if one is not found at less than minq
def create_node(n, maxl, minq):
    global graph, instances
    
    # Create a name
    name = gen_node_name()    
    # Select n parents
    #Without reputation
    parents = select_parents(n)
    
    # Calculate distance with parents 
    link_qual={}
    for i in range(0,len(parents)):
        link_qual[parents[i]] = select_dest_uniform(maxl)
        #link_qual[parents[i]] = select_dest_gaussian(maxl)
        #link_qual = random.sample(link_random, min(len(graph.keys()),n))
    # Insert node in graph
    graph[name] = []
    for i in range(0,len(parents)):
        graph[name].append((parents[i], link_qual[parents[i]]))
        #graph[parents[i]].append((name, link_qual[i]))
    #print graph[name]
    
    # Should this node be part of instances ?
    # Only if an instance could not be found from node name at distance < minq
    found = near_instance_found(name, 0, minq, 1);
    #result[name] = []
    if not found:
        instances.add(name)
    #else:
    #    for i in range(0,len(found)):
    #        result[name].append((found[i], link_qual[found[i]]))


# Create a graph with max_node, each of max_neighbor. 
# Distance from Parent nodes is 1 to Max dest 
# minq for instance decision
def create_graph(max_node, max_neighbor, max_dest, minq):
    global link_random, link_random_pattern
    init_vars()
    # Create table link_random with enough space to select set for parents
    link_random = max_node * link_random_pattern
    for i in range(1,max_node-1):
        create_node(max_neighbor, max_dest, minq)
                
def print_graph():
    global graph
    
    print "graph G {"
#    print "edge[style=solid, constraint=false];"
    for node in instances:
        print node + " [peripheries=2];"
    for node,arcs in graph.iteritems():
        for a, qual in arcs:
            print node + " -- " + a + " [label=\"" + str(qual) + "\"]"
    print "}"

# Print histogram from value recurrence
# term_lines used to feed the terminal
def print_hist(res, max_node, term_lines):
    previous = 0
    printed = 0
    for i in range(1,max_node):
        count = res.count(i)
        if (count == 0) and (previous == 0):
            previous = count
            continue
        if printed <= term_lines:
            print str(i) + " :" + res.count(i) * '*'
            printed += 1
        previous = count
    # Print empty lines until term_lines
    for i in range (1,term_lines-printed):
        print ""

if len(sys.argv) <= 5:
    sys.exit(0)

max_node = int(sys.argv[1])
max_neighbor = int(sys.argv[2])
max_link = int(sys.argv[3])
min_quality = int(sys.argv[4])
term_lines = int(sys.argv[5])

max_hop = max_node / 10
#max_neighbor = max_node - 1

if max_neighbor == 0:
    results = []
    for i in range(1,max_node):
        for k in range(1,2000):
            create_graph(max_node, i, max_link, min_quality)
            results.append(len(instances))
        print "mno: " + str(max_node) + " mne: " + str(i) + " ml: " + str(max_link) + " mq: " + str(min_quality)
        #print results
        print_hist(results,max_node, term_lines)
        results = []
    sys.exit(0)

if min_quality == 0:
    results = []
    for i in range(1,max_link*10):
        for k in range(1,200):
            create_graph(max_node, max_neighbor, max_link, i)
            results.append(len(instances))
        print "mno: " + str(max_node) + " mne: " + str(max_neighbor) + " ml: " + str(max_link) + " mq: " + str(i)
        #print results
        print_hist(results,max_node, term_lines)
        results = []
    sys.exit(0)


if (max_node - max_neighbor) < 1:
    sys.exit(0)
    
create_graph(max_node, max_neighbor, max_link, min_quality)
print_graph()