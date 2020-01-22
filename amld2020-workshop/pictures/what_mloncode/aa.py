


def nearest_neighbors(self, origin, k=10):
    # origin can be either a text query or an id
    if isinstance(origin, (tuple, list)):
        ...