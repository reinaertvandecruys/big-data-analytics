#!/usr/bin/env python3

import itertools
import networkx
import os
from typing import Dict, List, Optional, Set, Tuple


# This module contains the actual DBLP parser.
from dblp import dblpparser


class Parser:
    def parse(self, use_snap: bool, file_path: str, silent: bool) -> None:
        self._authors: List[str] = []
        self._publications: List[Tuple[int, Set[int]]] = []

        dblpparser.Parser().parse(on_record=self._process_record,
                                  use_snap=use_snap, silent=silent)

        with open(file_path, 'w') as f:
            f.write(str((self._authors, self._publications)))

    def _process_record(self, record: Tuple) -> None:
        _, attrs, data = record

        # Consider only publications from the PODS conferences.
        if not 'key' in attrs or not attrs['key'].startswith('conf/pods/'):
            return

        author_indices: Set[int] = set()

        for author in data['author']:
            author: str = author[0]

            if author not in self._authors:
                self._authors.append(author)

            author_indices.add(self._authors.index(author))

        year: int = int(data['year'][0][0])

        self._publications.append((year, author_indices))


def get_collaboration_graph(publications: List[Tuple[int, Set[int]]],
                            begin_year: int=0,
                            end_year: int=3000) -> networkx.Graph:
    graph: networkx.Graph = networkx.Graph()

    for year, authors in publications:
        if not begin_year <= year <= end_year:
            continue

        collaborations = dict()

        for pair in itertools.combinations(sorted(authors), 2):
            if pair not in collaborations:
                collaborations[pair] = 0

            collaborations[pair] += 1

        for author1, author2 in collaborations:
            graph.add_edge(author1, author2, weight=collaborations[pair])

    return graph


def load(use_snap: bool, silent: bool) -> List[Tuple[int, Set[int]]]:
    file_path = '%s%s.txt' % ('publications', ('-snap' if use_snap else ''))

    if not os.path.exists(file_path):
        Parser().parse(use_snap=use_snap, file_path=file_path, silent=False)

    authors, publications = eval(open(file_path).read())

    for i in range(len(publications)):
        year, author_indices = publications[i]
        publications[i] = (year, {authors[index] for index in author_indices})

    return publications


def main() -> None:
    if not os.path.isdir('results'):
        os.mkdir('results')

    for use_snap in [False]:
        publications = load(use_snap=use_snap, silent=False)

        header_line = '  |  '

        for begin_year in range(1980, 2010, 10):
            end_year = begin_year + 10
            
            header_line += '%s%i - %i%s  |  ' % (' ' * 23, begin_year, end_year, ' ' * 23)

            graph = get_collaboration_graph(publications, begin_year, end_year)

            centralities = networkx.betweenness_centrality(graph)
        
        header_line += '\n%s\n' % ('-' * len(header_line))
        
        with open('results/betweenness%s.txt' % ('-snap' if use_snap else ''), 'w') as f:
            f.write(header_line)

        generator = networkx.algorithms.community.centrality.girvan_newman(graph)

        top_level_communities = next(generator)

        next_level_communities = next(generator)

        for community in next_level_communities:
            print(community)


main()
