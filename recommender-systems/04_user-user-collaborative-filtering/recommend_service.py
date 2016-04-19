import math
import operator
from itertools import izip, ifilter

def mean(data):
    return sum(data) / len(data)

def pvariance(data, mu=None):
    _mu = mu
    if _mu is None:
        _mu = mean(data)
    return sum(pow(x-_mu, 2) for x in data) / len(data)

def pstdev(data, mu=None):
    return math.sqrt(pvariance(data, mu))

class RecommendService(object):
    def __init__(self, movie_score_dao, user_correlation_dao):
        object.__init__(self)

        self._movie_score_dao = movie_score_dao
        self._user_correlation_dao = user_correlation_dao

        self._build_user_correlation()

    @property
    def total_users(self):
        return self._movie_score_dao.total_fields()

    @property
    def total_movies(self):
        return self._movie_score_dao.total_records()

    def _uid(self, i):
        return self._movie_score_dao.get_uid(i)

    def _mid(self, i):
        return self._movie_score_dao.get_mid(i)

    def _uidx(self, uid):
        return self._movie_score_dao.index_uid(uid)

    def _user_scores(self, i):
        return self._movie_score_dao.get_user_scores(i)

    def _rated(self, x, y):
        a, u = izip(*ifilter(lambda (p, q): p and q, izip(x, y)))
        return list(a), list(u)

    # Pearson Correlation Coefficient
    def _correl(self, x, y):
        r_a, r_u = self._rated(x, y)

        m = len(r_a)
        mu_a = mean(r_a)
        mu_u = mean(r_u)
        dev_a = map(lambda x: x-mu_a, r_a)
        dev_u = map(lambda x: x-mu_u, r_u)

        def numerator():
            return sum(dev_a[i]*dev_u[i] for i in xrange(m))

        def denominator():
            s_a = math.sqrt(sum(dev_a[i]*dev_a[i] for i in xrange(m)))
            s_u = math.sqrt(sum(dev_u[i]*dev_u[i] for i in xrange(m)))
            return s_a * s_u

        return numerator() / denominator()

    def _build_user_correlation(self):
        for a in xrange(self.total_users):
            for u in xrange(self.total_users):
                correl = self._correl(
                    self._user_scores(a),
                    self._user_scores(u))

                self._user_correlation_dao.add_correlation(
                    self._uid(a),
                    (self._uid(u), correl))

    def get_correlation(self, uid1, uid2):
        return self._user_correlation_dao.get_correlation(uid1, uid2)

    def get_sorted_neighbors(self, uid):
        return self._user_correlation_dao.get_sorted_correlation(uid)

    def _fn_predict(self, score_wieghts):
        _score_wieghts = filter(operator.itemgetter(0), score_wieghts)

        sum_r, sum_w = 0, 0
        for r, w in _score_wieghts:
            sum_r += (r * w)
            sum_w += w
        return sum_r / sum_w if sum_w else 0

    def predict_all(self, uid):
        neighbors, nweights = zip(*self.get_sorted_neighbors(uid)[:5])
        nscores = [self._user_scores(self._uidx(n)) for n in neighbors]

        result, sz = [], len(neighbors)
        for i in xrange(self.total_movies):
            l = [(nscores[n][i], nweights[n]) for n in xrange(sz)]
            result.append((self._mid(i), self._fn_predict(l)))
        return result

    def top_n_movies(self, uid, n):
        movie_scores = self.predict_all(uid)
        movie_scores.sort(key=operator.itemgetter(1), reverse=True)
        return movie_scores[:n]

if __name__ == '__main__':
    def main():
        from movie_score_dao import MovieScoreDao
        from user_correlation_dao import UserCorrelationDao

        movie_score_dao = MovieScoreDao('movie_row.csv')
        user_correlation_dao = UserCorrelationDao()

        recommender = RecommendService(
            movie_score_dao,
            user_correlation_dao)

        print '===== User correlations ====='
        for u1, u2 in [(1648, 5136), (918, 2824)]:
            print '({:4d}, {:4d}): {}'.format(u1, u2, recommender.get_correlation(u1, u2))

        print '===== Top 5 neighbors ====='
        for u in [3712, 3867, 89]:
            neighbors = recommender.get_sorted_neighbors(u)[:5]
            for neighbor, correl in neighbors:
                print '{:4d}: {:4d} {}'.format(u, neighbor, correl)

        print '===== Top 3 Movies ====='
        for u in [3712, 3525, 3867, 89]:
            for m, score in recommender.top_n_movies(u, 3):
                print '{:4d}: ({:5d}, {})'.format(u, m, score)

    main()
