from src.maths.gaussian import gaussian


def test_gaussian() -> None:
    assert gaussian(1) == 0.24197072451914337
    assert gaussian(15) == 5.530709549844416e-50
    assert gaussian(24) == 3.342714441794458e-126
    assert gaussian(1, 4, 2) == 0.06475879783294587
    assert gaussian(1, 5, 3) == 0.05467002489199788
    assert gaussian(10 ** -326) == 0.3989422804014327
    assert gaussian(2523, mu=234234, sigma=3425) == 0.0
