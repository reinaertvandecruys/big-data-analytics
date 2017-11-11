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
        hubs, authorities = networkx.hits(graph)

        for name, author in self._authors.items():
            author.page_rank = pagerank[name]
            author.hub = hubs[name]
            author.authority = authorities[name]

        with open(authors_file_path, 'w') as authors_file:
            authors_file.write(str({name: str(author)
                                    for name, author in self._authors.items()}))

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
        self.hub = None
        self.authority = None

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


def analyze(authors, key, file):
    ordered = sorted(authors.values(), key=lambda x: x.__dict__[key], reverse=True)

    file.write('Name                                PC    PageRank    Hub                       Authority                 Collaborations                          PC    PageRank    Hub                       Authority             \n')
    file.write('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')

    for author in ordered:
        file.write('%s    %s    %0.6f    %s    %s' % (
            author.name.ljust(32),
            str(author.publication_count).rjust(2),
            author.page_rank,
            str(author.hub).ljust(22),
            str(author.authority).ljust(22)))

        if (len(author.collaborations) == 0):
            file.write('\n')

        first = True

        for name, i in sorted(author.collaborations.items(), key=lambda x: (x[1], authors[x[0]].__dict__[key]), reverse=True):
            if first:
                file.write('    ')
                first = False
            else:
                file.write(' ' * 106)

            other = authors[name]
            file.write('%s  %s    %s    %0.6f    %s    %s\n' % (
                str(i).rjust(2),
                other.name.ljust(32),
                str(other.publication_count).rjust(2),
                other.page_rank,
                str(other.hub).ljust(22),
                str(other.authority).ljust(22)))


def main():
    for use_snap in [True, False]:
        authors = load(use_snap=use_snap, silent=False)

        for key in ['authority', 'hub', 'page_rank', 'publication_count']:
            file_path = 'results/' + key + ('-snap' if use_snap else '') + '.txt'

            with open(file_path, 'w') as file:
                analyze(authors=authors, key=key, file=file)


main()
