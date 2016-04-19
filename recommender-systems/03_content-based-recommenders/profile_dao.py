import math
from abstract_dao_csv import AbstractDaoCSV

class ProfileDao(AbstractDaoCSV):
    def __init__(self, filename):
        AbstractDaoCSV.__init__(self, filename)

    def normalize_scores(self):
        result = []
        num = self.total_records()
        for i in xrange(num):
            records = self.get_records(i)
            length = math.sqrt(sum(map(lambda x: x*x, records)))
            result.append([x / length for x in records])
        self._records = result

    def total_profiles(self):
        return self.total_records()

    def total_keywords(self):
        return len(self._headers)

    def add_profile(self, profile):
        assert(len(profile) == 10)
        self._records.append(profile)

    def get_profile(self, i):
        return self.get_records(i)

    def get_keyword_scores(self, i):
        return [record[i] for record in self._records]

if __name__ == '__main__':
    def main():
        filename = 'doc_profile.csv'
        dao = ProfileDao(filename)
        profile_num = dao.total_profiles()

        for i in xrange(profile_num):
            profile = dao.get_profile(i)
            print '{0}: {1}'.format(i, profile)
            assert(len(profile) == 10)

        dao.normalize_scores()
        for i in xrange(profile_num):
            profile = dao.get_profile(i)
            print '{0}: {1}'.format(i, profile)

    main()
