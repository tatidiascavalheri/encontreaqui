from app.services.proximity import distance_m


def test_distance_ordering():
    origin = (-23.56, -46.65)
    points = [
        (1, -23.5601, -46.6501),
        (2, -23.57, -46.65),
        (3, -23.58, -46.64),
    ]
    ranked = sorted([(pid, distance_m(origin[0], origin[1], lat, lng)) for pid, lat, lng in points], key=lambda x: x[1])
    assert [p[0] for p in ranked] == [1, 2, 3]
