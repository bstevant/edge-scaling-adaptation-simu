from edge_infra import Infra
from infra_monitor import InfraMonitor

class AdaptationEngine:
    
    def __init__(self, infra, monit):
        self.infra = infra
        self.monit = monit
        
    def adapt_scaling_log(self, rtt_sla):
        current_violation = self.monit.report_sla_violations(rtt_sla)
        if current_violation > 0:
            next_instances = self.monit.report_nb_instances() + (int(current_violation/4) + 1)
            self.infra.scale_instances(next_instances)
            self.infra.reset_usage()
            self.infra.select_instances()
        self.infra.prune_instances()