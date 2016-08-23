import random

class Node:
    name = ""
    nb_nodes = 0
    # Set containing clients for this node
    used_by = set()
    
    def __init__(self):
        Node.nb_nodes += 1
        self.name = self.gen_node_name()
    
    # Generate a name nXXX
    def gen_node_name(self):
        return "n" + str(Node.nb_nodes)

class Link:
    rtt = 0
    
    def __init__(self, med_rtt):
        self.rtt = self.select_dest_uni(med_rtt)
    
    # Select an rtt value from a Gaussian distribution around median
    def select_dest_gaussian(self, median):
        i = random.randint(1,9)
        if i == 1:
            return random.randint(1,int(median*0.6))
        if (i == 2) or (i == 3):
            return random.randint(int(median*0.6),int(median*0.9))
        if (i == 4) or (i == 5) or (i == 6):
            return random.randint(int(median*0.9),int(median*1.1))
        if (i == 7) or (i == 8):
            return random.randint(int(median*1.1),int(median*1.4))
        if i == 9:
            return random.randint(int(median*1.4),int(median*2))
    
    # Select an rtt value from a uniform distribution from 0 to 1.5*median
    def select_dest_uni(self, median):
        i = random.randint(1,4)
        if i == 1:
            return random.randint(1,int(median*0.5))
        if i == 2:
            return random.randint(int(median*0.5), int(median))
        if i == 3:
            return random.randint(int(median), int(median*1.5))
        if i == 4:
            return random.randint(int(median*1.5), int(median*10))


class Client(Node):
    current_link = None
    known_links = {}
    med_rtt = 0
    
    def __init__(self, med_rtt):
        Node.__init__(self)
        self.med_rtt = med_rtt
        
    # Select the nearest instance
    def select_nearest_instance(self, instances):
        min_rtt = 100000
        selected = None
        
        # return if there is no instances
        if len(instances) < 1:
            return
        
        # For each instance ...
        for i in instances:
            # ... create a link if not in known_links ...
            if not self.known_links.has_key(i):
                self.known_links[i] = Link(self.med_rtt)
            # ... test if link with i is less than the last link found
            if self.known_links[i].rtt < min_rtt:
                selected = i
                min_rtt = self.known_links[i].rtt
        
        # Bail out if nothing selected (necessary ?)
        if selected == None:
            return
        
        # Record selected link
        self.current_link = self.known_links[selected]
        # Add current client in instance used_by
        selected.used_by.add(self)

class Infra:
    # Available nodes in the infrastructure
    nodes = set()
    # Nodes hosting an instance of the service
    instances = set()
    # Clients of the infrastructure
    clients = set()
    
    def __init__(self, nb_nodes, nb_clients, med_rtt):
        self.create_nodes(nb_nodes)
        self.create_clients(nb_clients, med_rtt)
    
    # Create nodes
    def create_nodes(self, n):
        for i in range(0, n):
            self.nodes.add(Node())
    # Create clients
    def create_clients(self, n, med_rtt):
        for i in range(0, n):
            self.clients.add(Client(med_rtt))
    
    # Scale number of instances to n
    def scale_instances(self, n):
        # min n to total number of nodes
        n = min(n, len(self.nodes) + len(self.instances))
        n = max(1, n)
        
        if n < len(self.instances):
            # Select arbitrary instances to becomes nodes
            while len(self.instances) > n:
                i = self.instances.pop()
                self.nodes.add(i)
                # reset node usage
                i.used_by = set()
        elif n > len(self.instances):
            # Select arbitrary nodes to become instances
            while len(self.instances) < n:
                i = self.nodes.pop()
                self.instances.add(i)
    
    # Reset current usage of instances by client
    def reset_usage(self):
        for c in self.clients:
            c.current_link = None
        for i in self.instances:
            i.used_by = set()
            
    # Request clients to select instance
    def select_instances(self):
        for c in self.clients:
            c.select_nearest_instance(self.instances)
    
    # Remove unused instances
    def prune_instances(self):
        unused = set()
        
        for i in self.instances:
            if len(i.used_by) == 0:
                unused.add(i)

        self.instances -= unused
        self.nodes |= unused
    