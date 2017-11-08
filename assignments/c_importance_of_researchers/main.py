from itertools import combinations
import networkx
import os
from pprint import pprint

from dblp import dblpparser


class Parser:
    def __init__(self):
        self._authors = None
    
    def parse(self, use_snap, authors_file_path, silent):
        self._authors = dict()

        dblpparser.Parser().parse(on_record=self._process_record,
                                    use_snap=use_snap, silent=silent)
        
        graph = networkx.Graph()

        for name, author in self._authors.items():
            graph.add_node(name)

            collaborations = []

            for other_name, weight in author.collaborations.items():
                collaborations.append((name, other_name, weight))
            
            graph.add_weighted_edges_from(collaborations)
        
        pagerank = networkx.pagerank(graph)
        _, authority_values = networkx.hits(graph)

        for name, author in self._authors.items():
            author.page_rank = pagerank[name]
            author.authority_score = authority_values[name]

        with open(authors_file_path, 'w') as authors_file:
            authors_file.write(str({name: str(author) for name, author in self._authors.items()}))

    def _process_record(self, record):
        _, attrs, data = record

        if not 'key' in attrs or not attrs['key'].startswith('conf/pods/'):
            return

        names = {author[0] for author in data['author']}

        for name in names:
            if name not in self._authors:
                self._authors[name] = Author(name=name, publication_count=0)
            
            self._authors[name].publication_count += 1
            
        for pair in combinations(names, 2):
            name1, name2 = pair
            author1 = self._authors[name1]
            author2 = self._authors[name2]

            if name2 not in author1.collaborations:
                author1.collaborations[name2] = 0
            if name1 not in author2.collaborations:
                author2.collaborations[name1] = 0
            
            author1.collaborations[name2] += 1
            author2.collaborations[name1] += 1


class Author:
    def __init__(self, **entries):
        self.name = None
        self.publication_count = None
        self.collaborations = dict()
        self.page_rank = None
        self.authority_score = None

        self.__dict__.update(entries)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.name == other.name


def load(use_snap, silent):
    file_path = '%s%s.txt' % ('authors', ('-snap' if use_snap else ''))

    if not os.path.exists(file_path):
        Parser().parse(use_snap=use_snap, authors_file_path=file_path, silent=silent)

    authors = eval(open(file_path).read())

    for name in authors:
        authors[name] = Author(**eval(authors[name]))

    return authors


def analyze(authors):
    authors = sorted(authors.values(), key=lambda x: x.page_rank, reverse=True)



    i = 0
    for author in authors:
        if i > 30:
            break
        i += 1
        pprint(str(author))


def main():
    for use_snap in (True, False):
        authors = load(use_snap=use_snap, silent=False)
        analyze(authors)

main()
