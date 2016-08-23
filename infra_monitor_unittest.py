from edge_infra import Infra
from infra_monitor import InfraMonitor

RTT_SLA = 30

# Create an infra
infra = Infra(100, 20, 500)
# Create a monitor
monit = InfraMonitor(infra)
# Print report
print "Step 1: New infra"
print "Number of instances: " + str(monit.report_nb_instances())
print "Number of SLA violations: " + str(monit.report_sla_violations(RTT_SLA))
print "Average RTT for clients: " + str(monit.report_average_rtt())
#print monit.inspect_clients()

# Scale instances inside infra
infra.scale_instances(50)
# Reset client usage
infra.reset_usage()
# Select instances for clients
infra.select_instances()
# Print report
print "Step 2: Scale up to 50 instances"
print "Number of instances: " + str(monit.report_nb_instances())
print "Number of SLA violations: " + str(monit.report_sla_violations(RTT_SLA))
print "Average RTT for clients: " + str(monit.report_average_rtt())
#print monit.inspect_clients()

# Remove unused instances
infra.prune_instances()
# Print report
print "Step 3: Removed unused instances"
print "Number of instances: " + str(monit.report_nb_instances())
print "Number of SLA violations: " + str(monit.report_sla_violations(RTT_SLA))
print "Average RTT for clients: " + str(monit.report_average_rtt())
#print monit.inspect_clients()

# Scale instances inside infra
infra.scale_instances(10)
# Reset client usage
infra.reset_usage()
# Select instances for clients
infra.select_instances()
# Print report
print "Step 4: Scale down to 10 instances"
print "Number of instances: " + str(monit.report_nb_instances())
print "Number of SLA violations: " + str(monit.report_sla_violations(RTT_SLA))
print "Average RTT for clients: " + str(monit.report_average_rtt())
#print monit.inspect_clients()

# Remove unused instances
infra.prune_instances()
# Print report
print "Step 5: Removed unused instances"
print "Number of instances: " + str(monit.report_nb_instances())
print "Number of SLA violations: " + str(monit.report_sla_violations(RTT_SLA))
print "Average RTT for clients: " + str(monit.report_average_rtt())
#print monit.inspect_clients()
