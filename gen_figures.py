import numpy      as np
import gnuplotlib as gp
from edge_infra import Link, Infra
from infra_monitor import InfraMonitor

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
                xlabel="RTT (ms)",
                ylabel="# nodes (cumul)")


##################################################
# Plot SLA violation vs. num of instances
def plot_slaviol_instances(trys): 
    curves= {5:None,
             10:None,
             25:None,
             50:None,
             100:None,
             200:None}

    for j in range(trys):
        c = {}
        for rtt_sla in curves.keys():
            c[rtt_sla] = []
        infra = Infra(1000,100,100)
        monit = InfraMonitor(infra)
#        for i in range(250,1,-1):
        for i in range(250):
            infra.scale_instances(i)
            infra.reset_usage()
            infra.select_instances()
            for rtt_sla in curves.keys():
                y = c[rtt_sla] 
                y.append(monit.report_sla_violations(rtt_sla))
                c[rtt_sla] = y
        for rtt_sla in curves.keys():
            if curves[rtt_sla] == None:
                curves[rtt_sla] = np.atleast_2d(c[rtt_sla])
            else:
                curves[rtt_sla] = np.concatenate((curves[rtt_sla], np.atleast_2d(c[rtt_sla])), axis=0)
        
    nx = np.arange(250)
    gp.plot((nx,np.average(curves[5], axis=0), {'legend':'5%'}),
            (nx,np.average(curves[10], axis=0), {'legend':'10%'}),
            (nx,np.average(curves[25], axis=0), {'legend':'25%'}),
            (nx,np.average(curves[50], axis=0), {'legend':'50%'}),
            (nx,np.average(curves[100], axis=0), {'legend':'100%'}),
            (nx,np.average(curves[200], axis=0), {'legend':'200%'}),
            hardcopy="plots/slaviol_instances.png",
            xlabel="# services instances",
            ylabel="# SLA violations")

plot_slaviol_instances(3)