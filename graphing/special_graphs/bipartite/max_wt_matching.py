"""
Implements the Hungarian method algo defined
in section 17.2 of Schrijver.
"""
import networkx as nx
import numpy as np


## How do we express a matching? Its a set of edges.
class Matching():
    def __init__(self,edges,wts,gr):
        self.graph=gr
        self.mtch={}
        self.wt = 0
        for i in range(len(edges)):
            self.mtch[edges[i]] = wts[i]
            self.wt += wts[i]
        self.l_verts_covered = set()
        self.r_verts_covered = set()
        for e in edges:
            self.l_verts_covered.add(e[0])
            self.r_verts_covered.add(e[1])
        self.l_verts_not_covered = gr.l_verts - self.l_verts_covered
        self.r_verts_not_covered = gr.r_verts - self.r_verts_covered

    def add_edge(self,ed,wt):
        if ed[0] in self.l_verts_covered:
            raise Exception("The left vertex has been seen.\
                    This isn't a valid addition to a matching.")
        if ed[1] in self.r_verts_covered:
            raise Exception("The right vertex has been seen.\
                This isn't a valid addition to a matching.")
        self.l_verts_covered.add(ed[0])
        self.r_verts_covered.add(ed[1])
        self.graph.l_verts.add(ed[0])
        self.graph.r_verts.add(ed[1])
        self.l_verts_not_covered-=self.l_verts_covered
        self.r_verts_not_covered-=self.r_verts_covered


class Graph():
    def __init__(self,edges,wts):
        self.set_edges = set(edges)
        self.edges = edges
        self.wts = wts
        self.verts = set()
        self.l_verts= set()
        self.r_verts = set()
        self.edge_dict = {}
        for ix in range(len(edges)):
            self.edge_dict[edges[ix]] = wts[ix]
        for e in edges:
            self.l_verts.add(e[0])
            self.r_verts.add(e[1])
        self.max_ver_ix = max(self.r_verts)


def find_max_matchings(graph):
    ## Start with an empty matching.
    m = Matching([],[],graph)
    while True:
        g = nx.DiGraph()
        for ix in range(len(graph.edges)):
            ed = graph.edges[ix]
            if ed in m.mtch:
                g.add_edge(ed[1],ed[0],weight=graph.wts[ix])
            else:
                g.add_edge(ed[0],ed[1],weight=-graph.wts[ix])
        u_m = m.l_verts_not_covered
        w_m = m.r_verts_not_covered
        for ver in u_m:
            g.add_edge(0,ver,weight=0)
        for ver in w_m:
            g.add_edge(ver,graph.max_ver_ix+1,weight=0)
        pth = nx.shortest_path(g,source=0,\
                target=graph.max_ver_ix+1,weight='weight',\
                    method='bellman-ford')
        ## If no path is found we can exit the loop.
        if len(pth)==0:
            break
        else:
            p_edges = set()
            for ix in range(len(pth)-1):
                p_edges.add((pth[ix],pth[ix+1]))
            nu_edges = p_edges.symmetric_difference(graph.set_edges)
            nu_wts = [graph.edge_dict[ed] for ed in nu_edges]
            m = Matching(nu_edges,nu_wts,graph)

if __name__=="__main__":
    edges=[[1,3],
            [1,4],
            [2,4],
            [2,5],
            [2,6],
            [2,7]]
    wts = [.4,.4,.1,.33,.33,.33]
    gr = Graph(edges,wts)
