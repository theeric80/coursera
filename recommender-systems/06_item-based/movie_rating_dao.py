from abstract_dao_csv import AbstractDaoCSV

def mean(data):
    return sum(data) / len(data)

class MovieRatingDao(AbstractDaoCSV):
    def __init__(self, filename):
        AbstractDaoCSV.__init__(self, filename)
        self._norm_ratings = []

    def _fmt_value(self, x):
        return float(x) if x else 0.0

    def _build_norm_ratings(self):
        result = []
        n = self.total_records()
        for m in xrange(n):
            record = self.get_record(m)
            mu = mean(filter(bool, record))
            result.append(map(lambda x: x-mu if x else x, record))
        self._norm_ratings = result

    def movie_id(self, i):
        return self.get_header(i).split(':')[0]

    def total_movies(self):
        return self.total_fields()

    def get_movie_ratings(self, i):
        return self.get_field(i)

    def get_norm_movie_ratings(self, i):
        if not self._norm_ratings:
            self._build_norm_ratings()
        return [record[i] for record in self._norm_ratings]

    def get_user_ratings(self, i):
        return self.get_record(i)

if __name__ == '__main__':
    def main():
        filename = 'ratings.csv'
        dao = MovieRatingDao(filename)
        n = dao.total_records()

        print '===== Records ====='
        for i in xrange(n):
            print dao.get_record(i)

    main()
