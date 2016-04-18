from abstract_dao_csv import AbstractDaoCSV

class LikeDao(AbstractDaoCSV):
    def __init__(self, filename):
        AbstractDaoCSV.__init__(self, filename)

    def total_users(self):
        return self.total_records()

    def get_likes(self, i):
        return self.get_records(i)

if __name__ == '__main__':
    def main():
        filename = 'user_like.csv'
        dao = LikeDao(filename)
        user_num = dao.total_users()

        for i in xrange(user_num):
            like = dao.get_likes(i)
            print '{0}: {1}'.format(i, like)
            assert(len(like) == 20)

    main()
