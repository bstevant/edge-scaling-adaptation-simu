from edge_infra import Node, Link, Client, Infra

# Create a node
a = Node()
# Create a Link
l = Link(500)
# Create a Client
c = Client(500)
# Select an Instance
i = set()
i.add(a)
c.select_nearest_instance(i)

# Create an infra
infra = Infra(100, 20, 500)
# Scale instances inside infra
infra.scale_instances(50)
# Reset client usage
infra.reset_usage()
# Select instances for clients
infra.select_instances()
# Remove unused instances
infra.prune_instances()