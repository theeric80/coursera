from abstract_dao_csv import AbstractDaoCSV

class WeightDao(AbstractDaoCSV):
    def __init__(self, filename):
        AbstractDaoCSV.__init__(self, filename)

    def _fmt_value(self, x):
        return float(x) if x else 0

if __name__ == '__main__':
    def main():
        filename = 'weights.csv'
        dao = WeightDao(filename)
        n = dao.total_records()

        for i in xrange(n):
            print dao.get_record(i)

    main()
