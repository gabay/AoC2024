import q6


def test_rotate_right():
    assert q6.rotate_right(q6.UP) == q6.RIGHT
    assert q6.rotate_right(q6.RIGHT) == q6.DOWN
    assert q6.rotate_right(q6.DOWN) == q6.LEFT
    assert q6.rotate_right(q6.LEFT) == q6.UP


def test_direction_rotate_right():
    assert q6.Direction.UP.rotate_right() == q6.Direction.RIGHT
    assert q6.Direction.RIGHT.rotate_right() == q6.Direction.DOWN
    assert q6.Direction.DOWN.rotate_right() == q6.Direction.LEFT
    assert q6.Direction.LEFT.rotate_right() == q6.Direction.UP
