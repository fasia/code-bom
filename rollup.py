import json
import copy
from typing import Dict, List, Tuple
import pandas as pd
import requests


class Graph :

    def __init__ (self):
        self.allpaths = []

    def FindAllPaths (self, adjlist : Dict[int, List[int]] , src : int, dst : int):
        # Clear previously stored paths
        path = []
        path.append((src, 1))

        # Use depth first search (with backtracking) to find all the paths in the graph
        self.DFS (adjlist, src, dst, path)
        
        return self.allpaths

    def Print (self):
        for path in self.allpaths:
            print("Path : " + str(path))
    
    def Clear (self):
        self.allpaths.clear()

    # This function uses DFS at its core to find all the paths in a graph
    def DFS (self, adjlist : Dict[int, List[int]], src : int, dst : int, path : List[Tuple[int, int]]):
        if (src == dst):
            self.allpaths.append(copy.deepcopy(path))
        else:
            for adjnode in adjlist[src]:
                path.append(adjnode)
                self.DFS (adjlist, adjnode[0], dst, path)
                path.pop()
    
    
def main():

    # read in the input json
    parts = requests.get('https://interviewbom.herokuapp.com/bom/').json()['data']

    # create a DAG object to hold bom
    g = Graph()

    # create an adjacency list DAG from data 
    pg = {}
    for p in parts:
        # {'id': 0, 'parent_part_id': None, 'part_id': 982, 'quantity': 1}
        pg[p['part_id']] = []
        for c in parts:
            if c['parent_part_id'] == p['part_id']:
                pg[p['part_id']].append((c['part_id'], c['quantity']))

    # follow all paths in the DAG b/n the root and all other sub parts 
    # calculate the total quantity of each part needed. 
    summary = []
    # pick part with parent_part_id None/null as root.
    root = None
    for part in parts:
        if part['parent_part_id'] == None:
            root = parts[0]['part_id']
            break
    
    for part in parts:
        paths = g.FindAllPaths(pg, root, part['part_id'])
        sp = {}
        tq = 0
        for path in paths:
            ptq = 1
            for q in path:
                ptq = ptq*q[1]
            tq = tq + ptq
        sp['part_id'] = part['part_id']
        sp['quantity'] = tq
        summary.append(sp)
        g.Clear()


    df = pd.DataFrame(data=summary)
    df.to_excel('dict1.xlsx', index=False)
    #print(summary)
    #print(df)

if __name__ == "__main__":
    main()