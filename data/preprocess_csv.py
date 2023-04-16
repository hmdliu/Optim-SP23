
vertex_dict = {}
raw_csv_path = './raw_single.csv'
out_csv_path = './raw_double.csv'
parse_neighbor = lambda s: (s[:s.find('(')], float(s[s.find('(')+1:s.find(')')]))

class Vertex:
    def __init__(self, name: str, idx: str, neighbors: list):
        self.name = name
        self.idx = int(idx)
        self.neighbors = neighbors

def main():

    # load raw data
    with open(raw_csv_path, 'r') as f:
        lines = f.read().split('\n')[1:]

    # convert to Vertex class
    name_list = []
    for l in lines:
        name, idx, ns = tuple(l.split(','))
        neighbors = [parse_neighbor(s) for s in ns.split('|')] if ns else []
        vertex_dict[name] = Vertex(name, idx, neighbors)
        name_list.append(name)
    print(f'vertex count: {len(vertex_dict)}')
    
    # complement symmetry edges
    for k, v in vertex_dict.copy().items():
        for n, d in v.neighbors:
            if (k, d) not in vertex_dict[n].neighbors:
                vertex_dict[n].neighbors.append((k, d))
    
    # sort neighbors
    for k, v in vertex_dict.items():
        v.neighbors.sort(key=lambda x: x[0])
        print(f'Vertex {k}: neighbors = {v.neighbors}')
    
    # dump complemented data
    lines = ['name,index,neighbors']
    for name in name_list:
        v = vertex_dict[name]
        neighbors = [f'{n}({d})' for n, d in v.neighbors]
        lines.append(f'{v.name},{v.idx},{"|".join(neighbors)}')
    with open(out_csv_path, 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    main()