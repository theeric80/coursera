import csv

class AbstractDaoCSV(object):
    def __init__(self, filename):
        object.__init__(self)

        self._headers = []
        self._records = []
        self._record_names = []

        if filename:
            self._parsefile(filename)

    def _parsefile(self, filename):
        with open(filename, 'rU') as csvfile:
            cvsreader = csv.reader(csvfile, delimiter=',')
            self._headers = cvsreader.next()[1:]
            for row in cvsreader:
                self._record_names.append(row[0])
                self._records.append(map(self._fmt_value, row[1:]))

    def _fmt_value(self, x):
        return int(x) if x else 0

    def total_records(self):
        return len(self._records)

    def total_fields(self):
        return len(self._headers)

    def get_record_name(self, i):
        return self._record_names[i]

    def get_record(self, i):
        return self._records[i]

    def get_field(self, i):
        return [record[i] for record in self._records]

    def get_header(self, i):
        return self._headers[i]

