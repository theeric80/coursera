from operator import itemgetter

class RecommendService(object):
    def __init__(self, user_feature_dao, item_feature_dao, weight_dao):
        object.__init__(self)

        self._user_feature_dao = user_feature_dao
        self._item_feature_dao = item_feature_dao
        self._weight_dao = weight_dao

    @property
    def total_items(self):
        return self._item_feature_dao.total_records()

    @property
    def total_features(self):
        return self._item_feature_dao.total_fields()

    def _user_features(self, i):
        return self._user_feature_dao.get_record(i)

    def _item_features(self, i):
        return self._item_feature_dao.get_record(i)

    def _feature_items(self, i):
        return self._item_feature_dao.get_field(i)

    def _weight(self, i):
        return self._weight_dao.get_field(i)[0]

    def item_id(self, i):
        return self._item_feature_dao.item_id(i)

    def _dot_product(self, v1, v2):
        return sum(p * q for p, q in zip(v1, v2))

    def top_n_movies_4_feature(self, feature, n):
        w = self._weight(feature)
        ratings = self._feature_items(feature)
        ratings = [(i, w*x) for i,x in enumerate(ratings)]
        ratings.sort(key=itemgetter(1), reverse=True)
        return ratings[:n]

    def top_n_movies_4_user(self, user, n):
        U = self._user_features(user)
        S = self._weight_dao.get_record(0)
        M = self.total_items

        ratings = U
        ratings = [p * q for p, q in zip(U, S)]
        ratings = [(m, self._dot_product(ratings, self._item_features(m))) for m in xrange(M)]
        ratings.sort(key=itemgetter(1), reverse=True)
        return ratings[:n]

if __name__ == '__main__':
    def main():
        from user_feature_dao import UserFeatureDao
        from movie_feature_dao import MovieFeatureDao
        from weight_dao import WeightDao

        user_feature_dao = UserFeatureDao('user_features.csv')
        movie_feature_dao = MovieFeatureDao('movie_features.csv')
        weight_dao = WeightDao('weights.csv')

        recommender = RecommendService(
            user_feature_dao,
            movie_feature_dao,
            weight_dao)

        print '===== Top Movies for feature 1 ====='
        feature = 0
        for i, x in recommender.top_n_movies_4_feature(feature, 5):
            print '{:2d}:{:4d}: {}'.format(i, recommender.item_id(i), x)

        print '===== Top Movies for feature 2 ====='
        feature = 1
        for i, x in recommender.top_n_movies_4_feature(feature, 5):
            print '{:2d}:{:4d}: {}'.format(i, recommender.item_id(i), x)

        print '===== Recommendations for user 4469 ====='
        uid = '4469'
        user = user_feature_dao.index_user(uid)
        for i, x in recommender.top_n_movies_4_user(user, 5):
            print '{:2d}:{:4d}: {}'.format(i, recommender.item_id(i), x)

    main()
