
class ItemCorrelationDao(object):
    def __init__(self, total_items):
        object.__init__(self)

        m = total_items
        self._correl = [[0 for x in xrange(m)] for y in xrange(m)]

    def set_correlation(self, i, j, correl):
        self._correl[i][j] = correl

    def get_correlation(self, i, j):
        return self._correl[i][j]

    def get_correlations(self, i):
        return self._correl[i]
