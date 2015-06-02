import os,sys,random
import networkx as nx
from load_data import *
       
def calcTransTrip(g):
    res = {}
    avg_c = 0
    for i in range(g.number_of_nodes()):
        c = 0
        for j in range(g.number_of_nodes()):
            if g.has_edge(i,j):
                for h in range(g.number_of_nodes()):
                    if g.has_edge(i,h) and g.has_edge(j,h):
                        c += 1
        avg_c += c                
        res[i] = c
    return res,avg_c*1.0/g.number_of_nodes()
    
def calcThreeCycles(g):
    res = {}
    avg_c = 0
    for i in range(g.number_of_nodes()):
        c = 0
        for j in range(g.number_of_nodes()):
            if g.has_edge(i,j):
                for h in range(g.number_of_nodes()):
                    if g.has_edge(h,i) and g.has_edge(j,h):
                        c += 1
        avg_c += c                
        res[i] = c
    return res,avg_c*1.0/g.number_of_nodes() 
    
def calcTransTies(g):
    res = {}
    avg_c = 0
    for i in range(g.number_of_nodes()):
        c = 0
        for j in range(g.number_of_nodes()):
            if g.has_edge(i,j):
                for h in range(g.number_of_nodes()):
                    if g.has_edge(i,h) and g.has_edge(h,j):
                        c += 1
                        break
        avg_c += c                
        res[i] = c
    return res,avg_c*1.0/g.number_of_nodes() 

def calcBalance(g):
    res = {}
    avg_c = 0
    for i in range(g.number_of_nodes()):
        c = 0
        b = 0
        for j in range(g.number_of_nodes()):
            if g.has_edge(i,j):
                for h in range(g.number_of_nodes()):
                    if h == j or h == i:
                        continue
                    if g.has_edge(i,h) and not g.has_edge(j,h):
                        b += 1
                    else:
                        if not g.has_edge(i,h) and g.has_edge(j,h):
                            b += 1
        b = b*1.0/((g.number_of_nodes()-2)*(g.number_of_nodes()-1))
        
        has_at_least_one_out_edge = False
        for j in range(g.number_of_nodes()):
            v = 0
            if g.has_edge(i,j):      
                has_at_least_one_out_edge = True
                for h in range(g.number_of_nodes()):
                    if h == j or h == i:
                        continue
                    if g.has_edge(i,h) and not g.has_edge(j,h):
                        v += b-1
                    else:
                        if not g.has_edge(i,h) and g.has_edge(j,h):
                            v += b-1
                        else:
                            v += b
            c += v
        if not has_at_least_one_out_edge:
            c = g.number_of_nodes()-2             
        avg_c += c*-1.0/(g.number_of_nodes()-2)                
        res[i] = c*-1.0/(g.number_of_nodes()-2)     
    return res,avg_c*1.0/g.number_of_nodes() 
   
def calcPopIn(g):
    res = {}
    avg_c = 0
    for i in range(g.number_of_nodes()):
        c_i = 0
        for j in range(g.number_of_nodes()):
            c = 0
            if g.has_edge(i,j):
                for k in range(g.number_of_nodes()):
                    if g.has_edge(k,j):
                        c += 1
            c = c**.5
            c_i += c
        avg_c += c_i               
        res[i] = c_i
    return res,avg_c*1.0/g.number_of_nodes() 
    
def calcPopOut(g):
    res = {}
    avg_c = 0
    for i in range(g.number_of_nodes()):
        c_i = 0
        for j in range(g.number_of_nodes()):
            c = 0
            if g.has_edge(i,j):
                for k in range(g.number_of_nodes()):
                    if g.has_edge(j,k):
                        c += 1
            c = c**.5
            c_i += c
        avg_c += c_i               
        res[i] = c_i
    return res,avg_c*1.0/g.number_of_nodes() 

def calcActIn(g):
    res = {}
    avg_c = 0
    for i in range(g.number_of_nodes()):
        c_i = 0
        for j in range(g.number_of_nodes()):
            c = 0
            if g.has_edge(j,i):
                for k in range(g.number_of_nodes()):
                    if g.has_edge(i,k):
                        c += 1
            c = c**.5
            c_i += c
        avg_c += c_i               
        res[i] = c_i
    return res,avg_c*1.0/g.number_of_nodes() 
    
def calcActOut(g):
    res = {}
    avg_c = 0
    for i in range(g.number_of_nodes()):
        c_i = 0
        for j in range(g.number_of_nodes()):
            c = 0
            if g.has_edge(i,j):
                for k in range(g.number_of_nodes()):
                    if g.has_edge(i,k):
                        c += 1
            c = c**.5
            c_i += c
        avg_c += c_i               
        res[i] = c_i
    return res,avg_c*1.0/g.number_of_nodes() 

metrics_dict = {"Transitivity Triplets":calcTransTrip,"Three Cycles":calcThreeCycles,"Balance":calcBalance,\
                "Popularity Ingoing":calcPopIn,"Popularity Outgoing":calcPopOut,"Activity Ingoing":calcActIn,"Activity Outgoing":calcActOut}

def getMetric(g,metric="Trans Trip"):
    if metric in metrics_dict:
        return metrics_dict[metric](g)
    else:
        print "ERROR metric:"+metric+" not implemented"
        return None

def addMetricsAsAttributes(graphs,metrics="all"):
    if metrics == "all":
        metrics = []
        for key in metrics_dict:
            metrics.append(key)
    for metric in metrics:
        if metric in metrics_dict:
            for g in graphs:
                for_node,avg = getMetric(g,metric)
                g.graph[metric] = [for_node[key] for key in range(g.number_of_nodes())]
    return graphs

def scatterPlotForMetrics(g1,g2,attribute):
    x = g1.graph[attribute]
    y = g2.graph[attribute]
    plt.scatter(x,y)
    plt.plot([min(x+y),max(x+y)],[min(x+y),max(x+y)],'k-',lw=2)
    plt.xlabel(g1.graph["title"])
    plt.ylabel(g2.graph["title"])
    plt.xlim(min(x+y),max(x+y))
    plt.ylim(min(x+y),max(x+y))
    plt.title(attribute)
    #------------------------
    #     sample usage
    #------------------------
    #  graphs,node_mapping = load_4_layers()
    #  graphs = addMetricsAsAttributes(graphs)
    #  i = 1
    #  for metric in metrics_dict:
    #      plt.subplot(3,3,i)
    #      scatterPlotForMetrics(graphs[2],graphs[5],metric)
    #      i += 1
    #  plt.show()
 
def main():
    graphs,node_mapping = load_4_layers("bms")
    graphs = addMetricsAsAttributes(graphs)
    #for key in metrics_dict:
    #    plt.figure()
    #    drawGraphs(graphs,key,False,True)
    i = 1
    for metric in metrics_dict:
        plt.subplot(3,3,i)
        scatterPlotForMetrics(graphs[2],graphs[5],metric)
        i += 1
    plt.show()
    
if __name__ == "__main__"    :
    main()
    