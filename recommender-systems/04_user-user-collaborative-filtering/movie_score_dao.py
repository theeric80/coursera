from abstract_dao_csv import AbstractDaoCSV

class MovieScoreDao(AbstractDaoCSV):
    def __init__(self, filename):
        AbstractDaoCSV.__init__(self, filename)

    def _fmt_value(self, x):
        return float(x) if x else x

    def index_uid(self, uid):
        return self._headers.index(str(uid))

    def get_uid(self, i):
        return int(self.get_header(i))

    def get_user_scores(self, i):
        return self.get_field(i)

    def get_movie_scores(self, i):
        return self.get_record(i)

    def get_mid(self, i):
        return int(self.get_record_name(i).split(':')[0])

if __name__ == '__main__':
    def main():
        filename = 'movie_row.csv'
        dao = MovieScoreDao(filename)
        print dao.get_field(0)
        print dao.get_record(0)

    main()
