import operator

class RecommendService(object):
    def __init__(self, user_like_dao, doc_profile_dao, user_profile_dao):
        object.__init__(self)

        self._user_like_dao = user_like_dao
        self._doc_profile_dao = doc_profile_dao
        self._user_profile_dao = user_profile_dao

        self._strategy = 'simple'

        self._build_IDF()
        self._build_user_profiles()

    def _dot_product(self, vector1, vector2):
        assert(len(vector1) == len(vector2))
        return sum(map(operator.mul, vector1, vector2))

    def _IDF(self, vector):
        # Inverse Document Frequency
        # vector: the vector contains the scores of each document for 1 keyword
        # IDF = 1 / DF, DF: # documents with keyword
        return 1.0 / sum(1 for x in vector if x > 0)

    @property
    def total_users(self):
        return self._user_like_dao.total_users()

    @property
    def total_documents(self):
        return self._doc_profile_dao.total_profiles()

    @property
    def total_keywords(self):
        return self._doc_profile_dao.total_keywords()

    @property
    def fn_predict(self):
        fn = self._dot_product
        if self._strategy == 'idf':
            fn = self._fn_predict_idf
        return fn

    def _fn_predict_idf(self, vector1, vector2):
        # three-way dot product: user vector * document vector * IDF
        assert(len(vector1) == len(vector2))
        return sum(map(lambda x, y, z: x*y*z, vector1, vector2, self._IDF))

    def _build_user_profiles(self):
        keyword_scores = self._doc_profile_dao.get_keyword_scores
        dot_product = self._dot_product

        for u in xrange(self.total_users):
            likes = self._user_like_dao.get_likes(u)
            user_profile = [dot_product(likes, keyword_scores(k)) for k in xrange(self.total_keywords)]
            self._user_profile_dao.add_profile(user_profile)

    def _build_IDF(self):
        keyword_scores = self._doc_profile_dao.get_keyword_scores
        self._IDF = [self._IDF(keyword_scores(i)) for i in xrange(self.total_keywords)]

    def set_strategy(self, strategy):
        self._strategy = strategy

    def print_user_profiles(self):
        for u in xrange(self.total_users):
            print '{0}: {1}'.format(u, self._user_profile_dao.get_profile(u))

    def predict(self, u, d):
        usr_vec = self._user_profile_dao.get_profile(u)
        doc_vec = self._doc_profile_dao.get_profile(d)
        return self.fn_predict(usr_vec, doc_vec)

    def predict_all(self, u):
        return [(d, self.predict(u, d)) for d in xrange(self.total_documents)]

    def top_n_docs(self, u, n):
        doc_scores = self.predict_all(u)
        doc_scores.sort(key=operator.itemgetter(1), reverse=True)
        return doc_scores[:n]

    def disliked_docs(self, u):
        return filter(lambda x: x[1] < 0, self.predict_all(u))

if __name__ == '__main__':
    def main():
        from profile_dao import ProfileDao
        from like_dao import LikeDao

        user_like_dao = LikeDao('user_like.csv')
        doc_profile_dao = ProfileDao('doc_profile.csv')
        user_profile_dao = ProfileDao('')

        recommender = RecommendService(
            user_like_dao,
            doc_profile_dao,
            user_profile_dao)

        print 'Simple'
        print '===== User profiles ====='
        recommender.print_user_profiles()
        print '===== Top 5 docs for U1 ====='
        for d, r in recommender.top_n_docs(0, 5):
            print 'D:{:2d}: {}'.format(d+1, r)
        print '===== Disliked docs for U2 ====='
        for d, r in recommender.disliked_docs(1):
            print 'D:{:2d}: {}'.format(d+1, r)


        print '\n\nNormalize scores'
        doc_profile_dao.normalize_scores()
        user_profile_dao = ProfileDao('')

        recommender = RecommendService(
            user_like_dao,
            doc_profile_dao,
            user_profile_dao)

        print '===== User profiles ====='
        recommender.print_user_profiles()
        print '===== Predictions ====='
        for u, d in [(0, 0), (1, 6), (1, 18)]:
            print '(U:{} D:{:2d}): {}'.format(u+1, d+1, recommender.predict(u, d))
        print '===== Top 5 docs for U1 ====='
        for d, r in recommender.top_n_docs(0, 5):
            print 'D:{:2d}: {}'.format(d+1, r)



        print '\n\nApply Inverse Document Frequency'
        recommender.set_strategy('idf')
        print '===== Predictions ====='
        for u, d in [(0, 0), (0, 8), (1, 5)]:
            print '(U:{} D:{:2d}): {}'.format(u+1, d+1, recommender.predict(u, d))

    main()
