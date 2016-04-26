from abstract_dao_csv import AbstractDaoCSV

def mean(data):
    return sum(data) / len(data)

class MovieRatingDao(AbstractDaoCSV):
    def __init__(self, filename):
        AbstractDaoCSV.__init__(self, filename)

    def _fmt_value(self, x):
        return float(x) if x else 0.0

    def normalize(self):
        result = []
        n = self.total_records()
        for i in xrange(n):
            record = self.get_record(i)
            mu = mean([x for x in record if x])
            result.append(map(lambda x: x-mu if x else x, record))
        self._records = result

    def movie_id(self, i):
        return self.get_record_name(i).split(':')[0]

    def total_movies(self):
        return self.total_fields()

    def get_movie_ratings(self, i):
        return self.get_field(i)

if __name__ == '__main__':
    def main():
        filename = 'ratings.csv'
        dao = MovieRatingDao(filename)
        n = dao.total_records()

        print '===== Records ====='
        for i in xrange(n):
            print dao.get_record(i)

        print '===== Normalized Records ====='
        dao.normalize()
        for i in xrange(n):
            print dao.get_record(i)

    main()
