import threading
import time
import sys
import xml.sax


__author__ = "Reinaert Van de Cruys"


MONITOR_INTERVAL = 1.0


class DBLP:
    PATH = 'dblp/dblp.xml'
    SIZE = 5860030


class DBLP_SNAP:
    PATH = 'dblp/dblp-snap.xml'
    SIZE = 50000


DEFAULT_DATA = [
    'address',
    'author',
    'booktitle',
    'cdrom',
    'chapter',
    'cite',
    'crossref',
    'editor',
    'ee',
    'isbn',
    'journal',
    'month',
    'note',
    'number',
    'pages',
    'publisher',
    'school',
    'series',
    'title',
    'url',
    'volume',
    'year',
]


class _Handler(xml.sax.ContentHandler):
    def __init__(self):
        super().__init__()

        self.on_record = None

        self.num_records_processed = None
        self.is_running = False

        self._depth = None

        self._name = None
        self._attributes = None
        self._children = None

        self._child_name = None

    def startDocument(self):
        self.is_running = True
        self.num_records_processed = 0
        self._depth = 0

    def endDocument(self):
        self.is_running = False

    def startElement(self, name, attrs):
        self._depth += 1

        if self._depth == 3:
            self._child_name = name
            self._children[self._child_name].append(['', attrs])
        elif self._depth == 2:
            self._name = name
            self._attributes = attrs
            self._children = {key: [] for key in DEFAULT_DATA}
        elif self._depth > 3:
            self._children[self._child_name][-1][0] += '<' + name + '>'

    def characters(self, content):
        if self._depth >= 3:
            self._children[self._child_name][-1][0] += content

    def endElement(self, name):
        if self._depth == 2:
            self.on_record((self._name, self._attributes, self._children))
            self.num_records_processed += 1
        elif self._depth > 3:
            self._children[self._child_name][-1][0] += '</' + name + '>'

        self._depth -= 1


class _Monitor(threading.Thread):
    def __init__(self):
        super().__init__()

        self.source = None
        self.handler = None

        self.start_time = None

        self.should_stop = None
        self.should_abort = None

    def run(self):
        self.should_stop = False
        self.should_abort = False

        while (not self.handler.is_running) and (not self.should_stop):
            time.sleep(0.1)

        self.start_time = time.time()

        while not self.should_stop and not self.should_abort:
            self.print_progess()
            time.sleep(MONITOR_INTERVAL)

        if not self.should_abort:
            self.print_progess()
            print('DONE')

    def print_progess(self):
        num_done = self.handler.num_records_processed
        num_total = self.source.SIZE
        fraction_done = num_done / num_total
        elapsed_time = time.time() - self.start_time
        estimated_time_remaining = ((1 - fraction_done) / (
            fraction_done / elapsed_time)) if fraction_done > 0 and elapsed_time > 1 else None

        output = 'Progress: ' + str(int(fraction_done * 100)).rjust(3) + '%  '
        output += '(' + str(num_done).rjust(len(str(num_total))) + \
            ' / ' + str(num_total) + ')        '
        output += 'Elapsed time: ' + str(int(elapsed_time / 60)).rjust(
            2, '0') + ':' + str(round(elapsed_time) % 60).rjust(2, '0') + '        '
        output += 'Estimated time remaining: ' + ((str(
            int(estimated_time_remaining / 60)).rjust(2, '0') + ':' + str(
                round(estimated_time_remaining) % 60).rjust(
                    2, '0')) if estimated_time_remaining is not None else 'Unknown')

        print(output, flush=True)


class Parser:
    def __init__(self):
        self._parser = xml.sax.make_parser()
        self._handler = _Handler()

        self._parser.setFeature(xml.sax.handler.feature_namespaces, False)
        self._parser.setContentHandler(self._handler)

    def parse(self, on_record, use_snap=False, silent=False):
        self._handler.on_record = on_record

        source = DBLP_SNAP if use_snap else DBLP

        input_path = source.PATH

        monitor = _Monitor()
        monitor.source = source
        monitor.handler = self._handler

        if not silent:
            monitor.start()

        try:
            self._parser.parse(input_path)
        except (KeyboardInterrupt, SystemExit):
            monitor.should_abort = True
            print('\nInterrupted by user.', flush=True)
            sys.exit()

        monitor.should_stop = True
