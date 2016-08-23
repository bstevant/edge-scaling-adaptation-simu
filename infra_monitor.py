class InfraMonitor:
    infra = None
    
    def __init__(self, infra):
        self.infra = infra

    # Report number of instances
    def report_nb_instances(self):
        return len(self.infra.instances)
    
    # Report number of violation of SLA
    def report_sla_violations(self, rtt_sla):
        nb_violation = 0
        # Count number of client with current_link > SLA
        for c in self.infra.clients:
            if (c.current_link != None) and (c.current_link.rtt > rtt_sla):
                nb_violation += 1
        return nb_violation
    
    # Report average RTT for clients
    def report_average_rtt(self):
        sum = 0
        count = 0
        for c in self.infra.clients:
            if c.current_link != None:
                count += 1
                sum += c.current_link.rtt
        if count == 0:
            return 0
        else:
            return sum / count
    
    # Inspect client informations (current instance + known links)
    def inspect_clients(self):
        for c in self.infra.clients:
            str_current = ""
            if c.current_instance != None:
                str_current = "i:" + c.current_instance.name
            if c.current_link != None:
                str_current += " rtt: " + str(c.current_link.rtt)
            print "Client " + c.name + " " + str_current
            str_links = "Known links: "
            for i,l in c.known_links.items():
                str_links += "i:" + i.name + " l:" + str(l.rtt) + " - "
            print str_links
    
        