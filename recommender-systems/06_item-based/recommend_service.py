import math
import operator

class RecommendService(object):
    def __init__(self, item_rating_dao, item_correlation_dao, normalized=False):
        object.__init__(self)

        self._item_rating_dao = item_rating_dao
        self._item_correlation_dao = item_correlation_dao

        self._build_item_correlation(normalized)

    @property
    def total_items(self):
        return self._item_rating_dao.total_movies()

    def _user_ratings(self, i):
        return self._item_rating_dao.get_user_ratings(i)

    def _item_ratings(self, i):
        return self._item_rating_dao.get_movie_ratings(i)

    def _norm_item_ratings(self, i):
        return self._item_rating_dao.get_norm_movie_ratings(i)

    def _item_correl(self, i, j):
        return self._item_correlation_dao.get_correlation(i, j)

    def _item_correls(self, i):
        return self._item_correlation_dao.get_correlations(i)

    def _dot_product(self, v1, v2):
        return sum(p * q for p, q in zip(v1, v2))

    def _magnitude(self, v):
        return math.sqrt(self._dot_product(v, v))

    def _cosine_sim(self, v1, v2):
        return self._dot_product(v1, v2) / (self._magnitude(v1) * self._magnitude(v2))

    def _build_item_correlation(self, normalized):
        _item_ratings = self._norm_item_ratings if normalized else self._item_ratings
        m = self.total_items
        for m1 in xrange(m):
            r1 = _item_ratings(m1)
            for m2 in xrange(m):
                r2 = _item_ratings(m2)
                sim = self._cosine_sim(r1, r2)
                self._item_correlation_dao.set_correlation(m1, m2, sim)
        """
        i, j = 0, 1
        print '[_build_item_correlation] sim({}, {})={}'.format(
            i, j, self._item_correlation_dao.get_correlation(i, j))
        """

    def _get_sorted_similiar_items(self, i):
        items = [(m, x) for m, x in enumerate(self._item_correls(i)) if m != i]
        items.sort(key=operator.itemgetter(1), reverse=True)
        return items

    def top_n_similiar_items(self, i, n):
        return self._get_sorted_similiar_items(i)[:n]

    def predict(self, uid, m):
        ratings = [(i, r) for i, r in enumerate(self._user_ratings(uid)) if r]
        ratings = [(r, self._item_correl(i, m)) for i, r in ratings]
        ratings = filter(lambda (r, w): w>0, ratings)
        return sum(r*w  for r, w  in ratings) / sum(w for _, w in ratings)

    def predict_all(self, uid):
        return [(m, self.predict(uid, m)) for m in xrange(self.total_items)]

    def top_n_recommended_items(self, uid, n):
        items = self.predict_all(uid)
        items.sort(key=operator.itemgetter(1), reverse=True)
        return items[:n]

if __name__ == '__main__':
    def main():
        from movie_rating_dao import MovieRatingDao
        from item_correlation_dao import ItemCorrelationDao

        movie_rating_dao = MovieRatingDao('ratings.csv')
        m = movie_rating_dao.total_movies()

        item_correlation_dao = ItemCorrelationDao(m)

        recommender = RecommendService(
            movie_rating_dao,
            item_correlation_dao)

        print '===== Top 5 Toy Story ====='
        toy_story = 0
        for i, x in recommender.top_n_similiar_items(toy_story, 5):
            print '({:2d}){:4s}: {}'.format(i, movie_rating_dao.movie_id(i), x)

        print '===== Top 5 for User 5277 ====='
        user = 1
        for i, x in recommender.top_n_recommended_items(user, 5):
            print '({:2d}){:4s}: {}'.format(i, movie_rating_dao.movie_id(i), x)

        print '\n\nNormalize Ratings'
        item_correlation_dao = ItemCorrelationDao(m)

        recommender = RecommendService(
            movie_rating_dao,
            item_correlation_dao,
            normalized=True)

        print '===== Top 5 Toy Story ====='
        toy_story = 0
        for i, x in recommender.top_n_similiar_items(toy_story, 5):
            print '({:2d}){:4s}: {}'.format(i, movie_rating_dao.movie_id(i), x)

        print '===== Top 5 for User 5277 ====='
        user = 1
        for i, x in recommender.top_n_recommended_items(user, 5):
            print '({:2d}){:4s}: {}'.format(i, movie_rating_dao.movie_id(i), x)

    main()
