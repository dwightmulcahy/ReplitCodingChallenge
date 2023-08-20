import unittest

from ot import isValid


class TestOperationalTransformations(unittest.TestCase):

    def test_SkipDelWorks(self):
        test = isValid(
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            'Repl.it uses operational transformations.',
            '[{"op": "skip", "count": 40}, {"op": "delete", "count": 47}]'
        )  # true
        assert test is True

    def test_DeletePastEnd(self):
        test = isValid(
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            'Repl.it uses operational transformations.',
            '[{"op": "skip", "count": 45}, {"op": "delete", "count": 47}]'
        )  # false, delete
        # past
        # end
        assert test is False

    def test_SkipPastEnd(self):
        test = isValid(
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            'Repl.it uses operational transformations.',
            '[{"op": "skip", "count": 40}, {"op": "delete", "count": 47}, {"op": "skip", "count": 2}]'
        )  # false, skip
        # past
        # end
        assert test is False

    def test_DeleteInsertWorks(self):
        test = isValid(
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            'We use operational transformations to keep everyone in a multiplayer repl in sync.',
            '[{"op": "delete", "count": 7}, {"op": "insert", "chars": "We"}, {"op": "skip", "count": 4}, {"op": "delete", "count": 1}]'
        )  # true
        assert test is True

    def test_DeleteInsertError(self):
        test = isValid(
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            'We can use operational transformations to keep everyone in a multiplayer repl in sync.',
            '[{"op": "delete", "count": 7}, {"op": "insert", "chars": "We"}, {"op": "skip", "count": 4}, {"op": "delete", "count": 1}]'
        )  # false
        assert test is False

    def test_NoOps(self):
        test = isValid(
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            '[]'
        )  # true
        assert test is True


if __name__ == '__main__':
    unittest.main()
