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

NUM_CLUSTERS = 1

FEATURE_THRESHOLD = 1/256

MIN_RELATIVE_CLUSTER_SIZE = 0.05

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

    for year_range, titles in sorted(titles_per_year_range.items()):
        print('From %i to %i:' % (year_range[0], year_range[1]))

        tfidf_matrix = vectorizer.transform(titles)

        k_means = KMeans(init='k-means++', n_clusters=NUM_CLUSTERS, n_init=10)
        k_means.fit(tfidf_matrix)

        cluster_sizes = [0] * NUM_CLUSTERS

        for label in k_means.labels_:
            cluster_sizes[label] += 1

        cluster_centers = [
            sorted([(cluster_center[i], feature_names[i])
                    for i in range(len(feature_names))], reverse=True)
            for cluster_center in k_means.cluster_centers_]

        clusters = sorted([(cluster_sizes[i], cluster_centers[i])
                           for i in range(len(cluster_centers))], reverse=True)

        for cluster_size, cluster_center in clusters:
            relative_cluster_size = cluster_size / len(titles)

            if relative_cluster_size < MIN_RELATIVE_CLUSTER_SIZE:
                break

            features = []

            for feature in cluster_center:
                value, name = feature

                if value < FEATURE_THRESHOLD:
                    break

                found = False

                for j in range(len(features)):
                    existing_feature = features[j]

                    if ' ' + name in ' ' + existing_feature[1] and value <= existing_feature[0]:
                        found = True
                        break
                    elif ' ' + existing_feature[1] in ' ' + name and value >= existing_feature[0]:
                        features[j] = feature
                        found = True
                        break
                
                if not found:
                    features.append(feature)

            if len(features) == 0:
                break
            
            print('    %04.2f%% is clustered around:' %
                  (relative_cluster_size * 100))
            
            for feature in sorted(features, reverse=True):
                print('        %.2f %s' % (feature[0], feature[1]))


def main():
    if not os.path.exists(DATA_DIR):
        Parser().parse(silent=False)

    conferences = sorted(list(CONFERENCES))

    for i in range(len(conferences)):
        conference = conferences[i]

        print('--------------------------------------------------------------------------------')
        print(' %s (%i/%s)' % (conference, i + 1, len(conferences)))
        print('--------------------------------------------------------------------------------')

        load(conference)
        analyze()

        print()
        print()


main()
