from itertools import permutations
from math import ceil, floor
import numpy
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
import os

from _dblp import dblpparser


RECORD_KEY_PREFIX = 'conf/'

CONFERENCES = {
    'kdd',
    'pkdd',
    'icdm',
    'sdm',
    'sigmod',
    'vldb',
    'edbt',
    'icde',
}

DATA_DIR = 'b_topic_drift/data'

NON_FEATURES = \
    [str(i) for i in range(2100)] +\
    ['0' + str(i) for i in range(10)] +\
    [str(i) + 'th' for i in range(4, 100)] +\
    [str(i) + 'st' for i in range(1, 100, 10)] +\
    [str(i) + 'nd' for i in range(2, 100, 10)] +\
    [str(i) + 'rd' for i in range(3, 100, 10)] +\
    [str(i) + 'g' for i in range(100)] +\
    [str(i) + 'x' for i in range(100, 1000, 100)] +\
    ['000', '2b', '2d', '2bench', '2pcp', '3d', '3x', '8i']

NGRAM_RANGE = (1, 6)

DRIFT_INTERVAL = 10
DRIFT_REFERENCE = 0
DRIFT_FORWARD_OVERLAP = 0
DRIFT_BACKWARD_OVERLAP = 0


def conference_to_file_path(conference: str, snap: bool) -> str:
    return DATA_DIR + '/' + conference + ('-snap' if snap else '') + '.txt'


class Parser:
    def __init__(self):
        self._data_files = {conference: None for conference in CONFERENCES}

    def parse(self, silent: bool) -> None:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        for use_snap in (True, False):
            for conference in CONFERENCES:
                file_path = conference_to_file_path(conference, use_snap)
                self._data_files[conference] = open(file_path, 'w')

            dblpparser.Parser().parse(on_record=self._process_record,
                                      use_snap=use_snap, silent=silent)

            for conference in CONFERENCES:
                self._data_files[conference].close()

    def _process_record(self, record) -> None:
        _, attrs, data = record

        key = attrs['key']

        if not key.startswith(RECORD_KEY_PREFIX):
            return

        key = key[len(RECORD_KEY_PREFIX):]

        for conference in CONFERENCES:
            if not key.startswith(conference + '/'):
                continue

            for year in data['year']:
                for title in data['title']:
                    entry = (year[0] + ' ' + title[0])\
                        .replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')

                    self._data_files[conference].write(entry + '\n')

            break


all_titles = []
titles_per_year_range = {}


def get_year_ranges(year):
    year_ranges = []

    offset = (year - DRIFT_REFERENCE)
    num_offset_intervals = floor(offset / DRIFT_INTERVAL)

    begin_year = num_offset_intervals * DRIFT_INTERVAL + DRIFT_REFERENCE
    end_year = begin_year + DRIFT_INTERVAL - 1

    while year >= begin_year - DRIFT_BACKWARD_OVERLAP and year <= end_year + DRIFT_FORWARD_OVERLAP:
        year_ranges.append((begin_year - DRIFT_BACKWARD_OVERLAP,
                            end_year + DRIFT_FORWARD_OVERLAP))

        begin_year -= DRIFT_INTERVAL
        end_year -= DRIFT_INTERVAL

    begin_year = year_ranges[0][0] + DRIFT_INTERVAL + DRIFT_BACKWARD_OVERLAP
    end_year = year_ranges[0][1] + DRIFT_INTERVAL - DRIFT_FORWARD_OVERLAP

    while year >= begin_year - DRIFT_BACKWARD_OVERLAP and year <= end_year + DRIFT_FORWARD_OVERLAP:
        year_ranges.append((begin_year - DRIFT_BACKWARD_OVERLAP,
                            end_year + DRIFT_FORWARD_OVERLAP))

        begin_year += DRIFT_INTERVAL
        end_year += DRIFT_INTERVAL

    return sorted(year_ranges)


def load(conference: str, snap: bool=False) -> None:
    global all_titles, titles_per_year_range

    with open(conference_to_file_path(conference, snap=snap)) as data_file:
        for entry in data_file:
            year, title = entry.split(' ', 1)
            year = int(year)
            year_ranges = get_year_ranges(year)

            all_titles.append(title)

            for year_range in year_ranges:
                if year_range not in titles_per_year_range:
                    titles_per_year_range[year_range] = []

                titles_per_year_range[year_range].append(title)

    all_titles = sorted(all_titles)

    for year_range in titles_per_year_range:
        titles_per_year_range[year_range] = sorted(
            titles_per_year_range[year_range])


def analyze() -> None:
    global all_titles, titles_per_year_range

    vectorizer = TfidfVectorizer(
        ngram_range=NGRAM_RANGE, stop_words='english')

    vectorizer.fit(all_titles)

    feature_names = vectorizer.get_feature_names()

    for year_range, titles in titles_per_year_range.items():
        print(year_range)

        tfidf_matrix = vectorizer.transform(titles)

        k_means = KMeans(init='k-means++', n_clusters=10, n_init=10)
        k_means.fit(tfidf_matrix)

        cluster_centers = [
            sorted([(cluster_center[i], feature_names[i])
                    for i in range(len(feature_names))], reverse=True)
            for cluster_center in k_means.cluster_centers_]

        for cluster_center in cluster_centers:
            num_found = 0
            print(cluster_center[0])
            continue

            for feature in cluster_center:
                if num_found > 0:
                    break

                for word in feature[1].split():
                    if word not in NON_FEATURES:
                        print('    ' + str(feature))
                        num_found += 1
                        break


def main():
    if not os.path.exists(DATA_DIR):
        Parser().parse(silent=False)

    for conference in CONFERENCES:
        load(conference)
        analyze()


main()
