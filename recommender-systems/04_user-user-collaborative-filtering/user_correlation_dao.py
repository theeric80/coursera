import operator
from itertools import dropwhile

class UserCorrelationDao(object):
    def __init__(self):
        object.__init__(self)

        self._correl = {}  # correlation, similarity

    def add_correlation(self, uid, correlation):
        # TODO: sorted
        neighbor = correlation[0]
        if uid != neighbor:
            self._correl.setdefault(uid, []).append(correlation)

    def get_correlation(self, uid1, uid2):
        correlations = self._correl.get(uid1)
        return dropwhile(lambda (u, correl): u!=uid2, correlations).next()[1]

    def get_sorted_correlation(self, uid):
        correlations = self._correl.get(uid)[:]
        correlations.sort(key=operator.itemgetter(1), reverse=True)
        return correlations
