from itertools import combinations
import networkx
import os

from _dblp import dblpparser


DATA_DIR = 'c_importance_of_researchers/data'


def to_file_path(name, use_snap):
    return '%s/%s%s.txt' % (DATA_DIR, name, ('-snap' if use_snap else ''))


class Parser:
    def __init__(self):
        self._publications = None

    def parse(self, silent: bool) -> None:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        for use_snap in (True, False):
            self._publications = []

            dblpparser.Parser().parse(on_record=self._process_record,
                                      use_snap=use_snap, silent=silent)

            authors = {}

            for author_group in self._publications:
                for author in author_group:
                    if author in authors:
                        authors[author] += 1
                    else:
                        authors[author] = 1

            

            with open(to_file_path('authors', use_snap), 'w') as authors_file:
                for author in sorted(authors):
                    authors_file.write(str(authors[author]) + ' ' + author + '\n')
            
            authors = sorted(authors)

            author_ids = {authors[i]: i for i in range(len(authors))}

            graph = [[0 for j in range(i + 1, len(authors))]
                     for i in range(len(authors) - 1)]

            for publication in self._publications:
                for author_pair in combinations(publication, 2):
                    author1, author2 = sorted(author_pair)
                    author1_id = author_ids[author1]
                    author2_id = author_ids[author2]

                    graph[author1_id][author2_id - author1_id - 1] += 1

            with open(to_file_path('graph', use_snap), 'w') as graph_file:
                for row in graph:
                    for cell in row:
                        graph_file.write(str(cell) + ' ')
                    graph_file.write('\n')

    def _process_record(self, record):
        _, attrs, data = record

        if 'key' in attrs and attrs['key'].startswith('conf/pods/'):
            self._publications.append({author[0] for author in data['author']})


def analyze(use_snap):
    authors = []
    publication_count = []

    with open(to_file_path('authors', use_snap)) as authors_file:
        for author in authors_file:
            num_publications, name = author.strip().split(' ', 1)
            authors.append(name)
            publication_count.append(num_publications)

    graph = networkx.Graph()

    with open(to_file_path('graph', use_snap)) as graph_file:
        author1_id = 0

        for line in graph_file:
            weights = [int(entry) for entry in line.split() if len(line) > 0]
            weighted_edges = [(author1_id, author1_id + i + 1, weights[i])
                              for i in range(len(weights))]
            graph.add_weighted_edges_from(weighted_edges)
            author1_id += 1

    pagerank = networkx.pagerank(graph)
    _, authority_values = networkx.hits(graph)

    print('ID     Name                                Publication count    PageRank      Authority score       ')
    print('----------------------------------------------------------------------------------------------------')

    for author_id in range(len(authors)):
        print('{:>3}    {:<32}    {:>17}    {:1.8f}    {:<22}'.format(
            author_id, authors[author_id], publication_count[author_id], pagerank[author_id], authority_values[author_id]))


def main():
    if not os.path.exists(DATA_DIR):
        Parser().parse(silent=False)

    for use_snap in (True, False):
        analyze(use_snap)


main()
