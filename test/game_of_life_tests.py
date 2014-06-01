import unittest
import sys
import os

class GameOfLifeTestCase(unittest.TestCase):

    def test_any_cell_with_fewer_than_two_neighbours_dies(self):
        starting_state = {(0, 0), (0, 1), (0, 2),
                          (1, 0)}
        expected_dead_cells = {(0, 2)}
        game = game_of_life.game_of_life(starting_state)
        result = next(game)
        self.assertEqual(len(result & expected_dead_cells), 0)

    def test_any_cell_with_two_or_three_neighbours_lives(self):
        starting_state = {(0, 0), (0, 1), (0, 2),
                                  (1, 1)}
        game = game_of_life.game_of_life(starting_state)
        result = next(game)
        self.assertTrue(result.issuperset(starting_state))

    def test_any_cell_with_four_plus_neighbours_dies(self):
        starting_state = {(0, 0), (0, 1), (0, 2),
                          (1, 0), (1, 1), (1, 2)}
        expected_dead_cells = {(0, 1), (1, 1)}
        game = game_of_life.game_of_life(starting_state)
        result = next(game)
        self.assertEqual(len(result & expected_dead_cells), 0)

    def test_any_dead_cell_with_three_neighbours_is_born(self):
        starting_state = {(0, 0), (0, 1), (0, 2),
                          (1, 0), (1, 1), (1, 2)}
        expected_born_cells = {(-1, 1), (2, 1)}
        game = game_of_life.game_of_life(starting_state)
        result = next(game)
        self.assertTrue(expected_born_cells.issubset(result))

    def test_create_starting_set(self):
        starting_state_in_text = [
                '',
                '   -',
                '  - ',
                ' -  ',
                '']
        expected_set = {(1, 3), (2, 2), (3, 1)}
        actual_set = game_of_life.create_starting_set_of_cells(starting_state_in_text)
        self.assertEqual(expected_set, actual_set)

if __name__ == '__main__':
    path_of_test_file = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path_of_test_file)
    source_directory = os.path.join(path_of_test_file, '..', 'src')
    sys.path.append(source_directory)
    import game_of_life
    unittest.main()
