
import pickle

vertex_dict = {}
dump_path = './D.pkl'
data_path = './data/raw_double.csv'
parse_neighbor = lambda s: (s[:s.find('(')], float(s[s.find('(')+1:s.find(')')]))

class Graph():
 
    def __init__(self, v_num, edges):
        self.v_num = v_num
        self.edges = edges
 
    def minDistance(self, dist, sptSet):
        min_dist = 1e8
        for v in range(self.v_num):
            if (dist[v] < min_dist) and (sptSet[v] == False):
                min_index, min_dist = v, dist[v]
        return min_index
 
    def dijkstra(self, src):
        dist = [1e7] * self.v_num
        sptSet = [False] * self.v_num
        dist[src] = 0
        for _ in range(self.v_num):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True
            for v in range(self.v_num):
                if (self.edges[u][v] > 0) and (sptSet[v] == False) and (dist[v] > dist[u] + self.edges[u][v]):
                    dist[v] = dist[u] + self.edges[u][v]
        return [round(v, 1) for v in dist]

class Vertex:
    def __init__(self, name: str, idx: str, neighbors: list):
        self.name = name
        self.idx = int(idx)
        self.neighbors = neighbors

def main():

    # load data
    with open(data_path, 'r') as f:
        lines = f.read().split('\n')[1:]

    # convert to Vertex class
    name_list = []
    for l in lines:
        name, idx, ns = tuple(l.split(','))
        neighbors = [parse_neighbor(s) for s in ns.split('|')] if ns else []
        vertex_dict[name] = Vertex(name, idx, neighbors)
        name_list.append(name)
    print(f'vertex count: {len(vertex_dict)}')

    # build adjacency matrix
    e_num = 0
    edges = [[0 for i in range(len(vertex_dict))] for j in range(len(vertex_dict))]
    for k, v in vertex_dict.items():
        for n, d in v.neighbors:
            edges[v.idx][vertex_dict[n].idx] = d
            e_num += 1
    print(f'edge count: {e_num // 2}')

    # compute shorest path distance matrix D
    D = []
    g = Graph(v_num=len(vertex_dict), edges=edges)
    for i in range(len(vertex_dict)):
        D.append(g.dijkstra(i))

    # dump results
    with open(dump_path, 'wb') as f:
        pickle.dump(D, f)
    print('matrix D dumped successfully')

if __name__ == '__main__':
    main()