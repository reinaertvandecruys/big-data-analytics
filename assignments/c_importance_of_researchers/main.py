from itertools import combinations
import networkx
import os
from pprint import pprint

# This module contains the actual DBLP parser.
from dblp import dblpparser


__author__ = "Jens Vannitsen, and Reinaert Van de Cruys"


# Script entrypoint at the bottom of the file.


class Parser:
    """
    This class uses the parser from the dblpparser module to read in the authors
    of every publication. It then creates a graph of author collaborations based
    on this information, and uses that graph to calculate the PageRank, hub
    score and authority score of every author. It writes this information to
    authors.txt and authors-snap.txt for the full dataset and the snap file
    respectively. These files are then used by code further below to perform
    the actual analysis and present the data in a handy human-readable format.
    """

    def __init__(self):
        self._authors = None

    def parse(self, use_snap, authors_file_path, silent):
        """"""
        self._authors = dict()

        # Parse the requested dataset (full or snap). See the _process_record
        # method below for details on what is done with each record.
        dblpparser.Parser().parse(on_record=self._process_record,
                                  use_snap=use_snap, silent=silent)

        # Build a graph representing author collaborations.
        graph = networkx.Graph()

        for name, author in self._authors.items():
            graph.add_node(name)

            collaborations = []

            for other_name, weight in author.collaborations.items():
                collaborations.append((name, other_name, weight))

            graph.add_weighted_edges_from(collaborations)

        # Feed the graph to the pagerank and hits functions of networkx.
        pagerank = networkx.pagerank(graph)
        hubs, authorities = networkx.hits(graph)

        # Assign each author their appropriate scores.
        for name, author in self._authors.items():
            author.page_rank = pagerank[name]
            author.hub = hubs[name]
            author.authority = authorities[name]

        # Write the result to the authors(-snap).txt file.
        with open(authors_file_path, 'w') as authors_file:
            authors_file.write(str({name: str(author)
                                    for name, author in self._authors.items()}))

    def _process_record(self, record):
        """
        This method is called for every record (=publication) found by the
        parser in the dblpparser module.
        """
        _, attrs, data = record

        # Consider only publications from the PODS conferences.
        if not 'key' in attrs or not attrs['key'].startswith('conf/pods/'):
            return

        # For each author, note their name, increment their publication count,
        # and increment the number of times they collaborated with each of the
        # other authors.
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
    """
    This class represents an author from the DBLP dataset. Most properties speak
    for itself, except maybe the collaborations property. This contains a
    dictionary indicating how often this author has published together with
    particular other authors, e.g. {'Liying Sui': 2, 'Alin Deutsch': 3}.
    """

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
    """
    Load the author set, along with their scores and collaborations, from the
    authors(-snap).txt file. If this file does not exist yet, create it first by
    parsing the actual dblp(-snap) dataset.
    """
    
    file_path = '%s%s.txt' % ('authors', ('-snap' if use_snap else ''))

    if not os.path.exists(file_path):
        Parser().parse(use_snap=use_snap, authors_file_path=file_path, silent=silent)

    authors = eval(open(file_path).read())

    for name in authors:
        authors[name] = Author(**eval(authors[name]))

    return authors


def analyze(authors, key, file):
    """
    Print out the given author set in a human-readable format, and sorted by the
    given key. When this is done for different keys (publication_count,
    page_rank, hub and authority), this makes a comperative analysis relatively
    easy.
    """

    # Sort the authors by the given key.
    ordered = sorted(authors.values(),
                     key=lambda x: x.__dict__[
                     key],
                     reverse=True)

    # Write the table header.
    file.write('Name                                PC    PageRank    ' +
               'Hub                       Authority                 ' +
               'Collaborations                          PC    PageRank    ' +
               'Hub                       Authority             \n')
    file.write(('-' * 212) + '\n')

    # For every author, write his/her properties.
    for author in ordered:
        file.write('%s    %s    %0.6f    %s    %s' % (
            author.name.ljust(32),
            str(author.publication_count).rjust(2),
            author.page_rank,
            str(author.hub).ljust(22),
            str(author.authority).ljust(22)))

        # Write the list of collaborators of the current author, along with
        # their properties.
        if (len(author.collaborations) == 0):
            file.write('\n')

        first = True

        for name, i in sorted(author.collaborations.items(),
                              key=lambda x: (
                                  x[1], authors[x[0]].__dict__[key]),
                              reverse=True):
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
    """Main function, dictates what data is analyzed and how."""

    if not os.path.isdir('results'):
        os.makedirs('results')

    # Run on both the snap file and the full dataset. remove a value from the
    # array to run on only one.
    for use_snap in [True, False]:
        # Load the author set into memory.
        authors = load(use_snap=use_snap, silent=False)

        # For each of the given properties, sort the authors by that property
        # and write the result to an appropriately named file in the 'results'
        # directory.
        for key in ['authority', 'hub', 'page_rank', 'publication_count']:
            file_path = 'results/' + key + \
                ('-snap' if use_snap else '') + '.txt'

            with open(file_path, 'w') as file:
                analyze(authors=authors, key=key, file=file)


# Entrypoint of the script.
main()
