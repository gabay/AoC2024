from q15 import Board2, Point


def test_gps_sum():
    board = Board2(Point(0, 0), set([Point(5, 1)]), set())
    assert board.get_gps_sum() == 105


def test_move_right():
    board = Board2(Point(0, 0), set([Point(1, 0)]), set())
    board.move_right()
    assert board.robot == Point(1, 0)
    assert board.wide_barrels == set([Point(2, 0)])


def test_move_right_with_block():
    board = Board2(Point(0, 0), set([Point(1, 0)]), set([Point(3, 0)]))
    board.move_right()
    assert board.robot == Point(0, 0)
    assert board.wide_barrels == set([Point(1, 0)])


def test_move_left():
    board = Board2(Point(3, 0), set([Point(1, 0)]), set())
    board.move_left()
    assert board.robot == Point(2, 0)
    assert board.wide_barrels == set([Point(0, 0)])


def test_move_left_with_block():
    board = Board2(Point(3, 0), set([Point(1, 0)]), set([Point(0, 0)]))
    board.move_left()
    assert board.robot == Point(3, 0)
    assert board.wide_barrels == set([Point(1, 0)])


def test_move_up1():
    board = Board2(Point(1, 2), set([Point(0, 1)]), set())
    board.move_up()
    assert board.robot == Point(1, 1)
    assert board.wide_barrels == set([Point(0, 0)])


def test_move_up2():
    board = Board2(Point(1, 2), set([Point(1, 1)]), set())
    board.move_up()
    assert board.robot == Point(1, 1)
    assert board.wide_barrels == set([Point(1, 0)])


def test_move_up3():
    board = Board2(Point(1, 3), set([Point(1, 2), Point(0, 1), Point(2, 1)]), set())
    board.move_up()
    assert board.robot == Point(1, 2)
    assert board.wide_barrels == set([Point(1, 1), Point(0, 0), Point(2, 0)])


def test_move_up3_with_block():
    board = Board2(
        Point(1, 3), set([Point(1, 2), Point(0, 1), Point(2, 1)]), set([Point(0, 0)])
    )
    board.move_up()
    assert board.robot == Point(1, 3)
    assert board.wide_barrels == set([Point(1, 2), Point(0, 1), Point(2, 1)])


def test_move_down1():
    board = Board2(Point(1, 0), set([Point(0, 1)]), set())
    board.move_down()
    assert board.robot == Point(1, 1)
    assert board.wide_barrels == set([Point(0, 2)])


def test_move_down2():
    board = Board2(Point(1, 0), set([Point(1, 1)]), set())
    board.move_down()
    assert board.robot == Point(1, 1)
    assert board.wide_barrels == set([Point(1, 2)])


def test_move_down3():
    board = Board2(Point(1, 0), set([Point(1, 1), Point(0, 2), Point(2, 2)]), set())
    board.move_down()
    assert board.robot == Point(1, 1)
    assert board.wide_barrels == set([Point(1, 2), Point(0, 3), Point(2, 3)])


def test_move_down3_with_block():
    board = Board2(
        Point(1, 0), set([Point(1, 1), Point(0, 2), Point(2, 2)]), set([Point(0, 3)])
    )
    board.move_down()
    assert board.robot == Point(1, 0)
    assert board.wide_barrels == set([Point(1, 1), Point(0, 2), Point(2, 2)])
