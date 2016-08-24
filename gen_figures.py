import numpy      as np
import gnuplotlib as gp
from edge_infra import Link, Infra
from infra_monitor import InfraMonitor
from adaptation_engine import AdaptationEngine

################################################
# Plot RTT distribution for 500 links
def plot_rtt_distribution():
    data = []
    MED_RTT = 100
    for i in range(1,500):
        l = Link(MED_RTT)
        data.append(l.rtt)

        h, b = np.histogram(data, 100)
        h2 = np.cumsum(h)
        b2 = b[1:]
        gp.plot(b2,h2, 
                hardcopy="plots/rtt_dist.png",
                title="Cumulative distribution of RTT",
                xlabel="RTT (ms)",
                ylabel="# nodes (cumul)")


##################################################
# Plot SLA violation vs. num of instances
def plot_slaviol_instances(nb_run): 
    max_instances = 200 # Max number of instances
    curves= {5:None,
             10:None,
             25:None,
             50:None,
             100:None,
             200:None}

    # Run for nb_run times
    for j in range(nb_run):
        c = {}
        # Init arrays for this run
        for rtt_sla in curves.keys():
            c[rtt_sla] = []
        # Init and monitor
        infra = Infra(1000,100,100)
        monit = InfraMonitor(infra)
        # Increase (or decrease) number of instances
        for i in range(max_instances):
        #for i in range(max_instances,0,-1):
            # Scale instances and reset usage
            infra.scale_instances(i)
            infra.reset_usage()
            infra.select_instances()
            # Evaluate nb of sla violation for each sla
            for rtt_sla in curves.keys():
                nb_slaviol = monit.report_sla_violations(rtt_sla)
                c[rtt_sla].append(nb_slaviol)
        # Add results for this run in the table
        for rtt_sla in curves.keys():
            if curves[rtt_sla] == None:
                curves[rtt_sla] = np.atleast_2d(c[rtt_sla])
            else:
                curves[rtt_sla] = np.concatenate((curves[rtt_sla], np.atleast_2d(c[rtt_sla])), axis=0)

    # Plot the results after average calculation on each column
    nx = np.arange(max_instances)
    gp.plot((nx,np.average(curves[5], axis=0), {'legend':'5%'}),
            (nx,np.average(curves[10], axis=0), {'legend':'10%'}),
            (nx,np.average(curves[25], axis=0), {'legend':'25%'}),
            (nx,np.average(curves[50], axis=0), {'legend':'50%'}),
            (nx,np.average(curves[100], axis=0), {'legend':'100%'}),
            (nx,np.average(curves[200], axis=0), {'legend':'200%'}),
            hardcopy="plots/slaviol_instances.png",
            title="Variation of SLA violations with service deployment",
            xlabel="# services instances",
            ylabel="# SLA violations")

##################################################
# Plot scaling adaptation to RTT SLA using log
def plot_log_adaptation():
    nb_iter = 100
    rtt_sla = 10
    infra = Infra(1000,100,100)
    monit = InfraMonitor(infra)
    adapt = AdaptationEngine(infra, monit)
    slaviol = []
    instances = []
    
    for i in range(nb_iter):
        instances.append(monit.report_nb_instances())
        slaviol.append(monit.report_sla_violations(rtt_sla))
        adapt.adapt_scaling_log(rtt_sla)
    
    x = np.arange(nb_iter)
    gp.plot((x, np.array(slaviol), {'legend':'# SLA violations','with': 'filledcurve x1 fill transparent solid 0.5'}),
            (x,np.array(instances), {'legend':'# instances', 'with': 'linespoints linewidth 2'}),
            xlabel="iterations",
            ylabel="Count",
            hardcopy="plots/adapt_log.png")

# Plot RTT distribution
#plot_rtt_distribution()

# Plot SLA violation vs. num of instances
#plot_slaviol_instances(10)

# Plot scaling adaptation to RTT SLA using log
plot_log_adaptation()