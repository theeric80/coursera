import csv

class MovieRatingDao(object):
    def __init__(self, filename):
        object.__init__(self)

        self._movies = []
        self._ratings = []

        self._parsefile(filename)

    def _parsefile(self, filename):
        with open(filename, 'rU') as csvfile:
            cvsreader = csv.reader(csvfile, delimiter=',')
            self._movies = cvsreader.next()[1:]
            for row in cvsreader:
                self._ratings.append([int(x) if x else 0 for x in row[1:]])

    def total_movies(self):
        return len(self._movies)

    def get_movie(self, i):
        return self._movies[i]

    def get_ratings(self, i):
        return [u[i] for u in self._ratings if u[i] > 0]

    def count_rating(self, i):
        return len(self.get_ratings(i))

    def count_association(self, i, j):
        return sum(1 for u in self._ratings if u[i] > 0 and u[j] > 0)

if __name__ == '__main__':
    from operator import itemgetter

    filename = '02_assignment-1-instructions_A1Ratings.csv'
    dao = MovieRatingDao(filename)
    movie_num = dao.total_movies()

    def mean():
        result = []
        for i in xrange(movie_num):
            r = dao.get_ratings(i)
            result.append((i, sum(r) / float(len(r))))
        return result

    def more_than_4():
        result = []
        for i in xrange(movie_num):
            r1 = dao.get_ratings(i)
            r2 = filter(lambda x: x >= 4, r1)
            result.append((i, len(r2) / float(len(r1)) * 100))
        return result

    def rating_count():
        return [(i, dao.count_rating(i)) for i in xrange(movie_num)]

    def association(i):
        result = []
        x = dao.count_rating(i)
        for k in xrange(movie_num):
            xy = float(dao.count_association(i, k))
            result.append((k, xy / x * 100))
        return result

    def print_top_5(l):
        for i, x in l[:5]:
            mid = dao.get_movie(i).split(':')[0]
            print '{0}: {1}'.format(mid, x)

    # Validation: 18: Raiders of the Lost Ark

    print '===== Mean Rating ====='
    l = mean()
    assert(2.90 < l[18][1] <= 2.91)
    l.sort(key=itemgetter(1), reverse=True)
    print_top_5(l)

    print '===== Rating Count ====='
    l = rating_count()
    assert(11 == l[18][1])
    l.sort(key=itemgetter(1), reverse=True)
    print_top_5(l)

    print '===== % of ratings 4+ ====='
    l = more_than_4()
    assert(27.2 < l[18][1] <= 27.3)
    l.sort(key=itemgetter(1), reverse=True)
    print_top_5(l)

    print '===== Top 5 Star Wars ====='
    l = association(0)
    assert(46.6 < l[18][1] <= 46.7)
    l.sort(key=itemgetter(1), reverse=True)
    print_top_5(l[1:])
