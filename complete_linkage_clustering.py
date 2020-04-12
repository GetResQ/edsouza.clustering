import dataclasses
import itertools
import pdb

points = [
    0,
    1,
    2,
    10,
    12,
    15,
]


def first(l):
    return next(iter(l))


def distance(p1, p2):
    return abs(p1 - p2)


class Cluster:
    def __init__(self, *, clusters=None, points=None):
        self.clusters = frozenset()
        self.points = frozenset()
        if points:
            self.points = self.points | set(points)
        if clusters:
            self.clusters = self.clusters | clusters
            for cluster in clusters:
                self.points = self.points | cluster.points

    def __eq__(self, other):
        return self.points == other.points

    def __hash__(self):
        return hash((
            self.points,
            self.clusters,
        ))

    def __repr__(self):
        return f'[{", ".join(map(str, self.points))}]'

    def distanceTo(self, c):
        max_distance = distance(first(self.points), first(c.points))

        for (p1, p2) in zip(self.points, c.points):
            max_distance = max(max_distance, distance(p1, p2))

        return max_distance

    def mergeWith(self, c):
        new_cluster = Cluster(
            clusters=frozenset([self, c]),
            points=self.points | c.points,
        )
        return new_cluster


@dataclasses.dataclass
class DistanceMatrix:
    columns: frozenset
    rows: frozenset

    def __post_init__(self):
        self.columns = frozenset(self.columns)
        self.rows = frozenset(self.rows)

    def __str__(self):
        return f'D({self.columns})'

    def pairs(self):
        return [(c1, c2)
                for (c1, c2) in itertools.product(self.columns, self.rows)
                if c1 != c2]

    def closest_cluster_pair(self):
        pairs = self.pairs()
        if not pairs:
            pdb.set_trace()

        smallest = pairs[0]

        for (c1, c2) in pairs:
            if c1.distanceTo(c2) < smallest[0].distanceTo(smallest[1]):
                smallest = (c1, c2)

        return smallest

    def remove(self, cluster):
        assert cluster in self.columns
        assert cluster in self.rows

        return DistanceMatrix(
            columns=self.columns - frozenset([cluster]),
            rows=self.rows - frozenset([cluster]),
        )

    def add(self, cluster):
        return DistanceMatrix(
            columns=self.columns | frozenset([cluster]),
            rows=self.rows | frozenset([cluster]),
        )


def get_initial_D(points):
    return DistanceMatrix(
        columns=[Cluster(points=[x]) for x in points],
        rows=[Cluster(points=[x]) for x in points],
    )


def get_D_prime(D):
    smallest = D.closest_cluster_pair()
    new_cluster = smallest[0].mergeWith(smallest[1])
    D_prime = D.remove(smallest[0]).remove(smallest[1]).add(new_cluster)
    return D_prime


def get_cluster():
    D1 = get_initial_D(points)
    Ds = [D1]

    D = D1
    while True:
        print(D)
        if len(D.columns) == 1:
            break
        D_prime = get_D_prime(D)
        Ds.append(D_prime)
        D = D_prime

    return Ds


# import pdb; pdb.set_trace() # yapf: disable

cluster = get_cluster()
print(cluster)
