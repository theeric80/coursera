import csv

class AbstractDaoCSV(object):
    def __init__(self, filename):
        object.__init__(self)

        self._headers = []
        self._records = []

        if filename:
            self._parsefile(filename)

    def _parsefile(self, filename):
        with open(filename, 'rU') as csvfile:
            cvsreader = csv.reader(csvfile, delimiter=',')
            self._headers = cvsreader.next()[1:]
            for row in cvsreader:
                self._records.append(map(self._fmt_value, row[1:]))

    def _fmt_value(self, x):
        return int(x) if x else 0

    def total_records(self):
        return len(self._records)

    def get_records(self, i):
        return self._records[i]

if __name__ == '__main__':
    def main():
        filename = 'doc_profile.csv'
        dao = AbstractDaoCSV(filename)
        total_num = dao.total_records()

        for i in xrange(total_num):
            r = dao.get_records(i)
            print '{0}: {1}'.format(i, r)

    main()
