from abstract_dao_csv import AbstractDaoCSV

class ProfileDao(AbstractDaoCSV):
    def __init__(self, filename):
        AbstractDaoCSV.__init__(self, filename)

    def total_profiles(self):
        return self.total_records()

    def add_profile(self, profile):
        assert(len(profile) == 10)
        self._records.append(profile)

    def get_profile(self, i):
        return self.get_records(i)

if __name__ == '__main__':
    def main():
        filename = 'doc_profile.csv'
        dao = ProfileDao(filename)
        profile_num = dao.total_profiles()

        for i in xrange(profile_num):
            profile = dao.get_profile(i)
            print '{0}: {1}'.format(i, profile)
            assert(len(profile) == 10)

    main()
