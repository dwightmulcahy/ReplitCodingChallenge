import json
import unittest

from ot import OperationalTransformation


def isValid(document: str, expected: str, otjson: json):
    """
    Helper function used for unittests to run the OT commands against the `document` and verify expected results

    :param document: string of the starting document
    :param expected: string of the resulting transformed document expected
    :param otjson: json list of OT commands
    :return: bool, True if matched `expected`, False if not
    """
    transformedDocument = OperationalTransformation(document).transform(otjson)
    return transformedDocument == expected


class TestOperationalTransformations(unittest.TestCase):

    #
    # Tests from coding challenge text
    #
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
        # past end
        assert test is False

    def test_SkipPastEnd(self):
        test = isValid(
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            'Repl.it uses operational transformations.',
            '[{"op": "skip", "count": 40}, {"op": "delete", "count": 47}, '
            '{"op": "skip", "count": 2}]'
        )  # false, skip
        # past end
        assert test is False

    def test_DeleteInsertWorks(self):
        test = isValid(
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            'We use operational transformations to keep everyone in a multiplayer repl in sync.',
            '[{"op": "delete", "count": 7}, {"op": "insert", "chars": "We"}, '
            '{"op": "skip", "count": 4}, {"op": "delete", "count": 1}]'
        )  # true
        assert test is True

    def test_DeleteInsertError(self):
        test = isValid(
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            'We can use operational transformations to keep everyone in a multiplayer repl in sync.',
            '[{"op": "delete", "count": 7}, {"op": "insert", "chars": "We"}, '
            '{"op": "skip", "count": 4}, {"op": "delete", "count": 1}]'
        )  # false
        assert test is False

    def test_NoOps(self):
        test = isValid(
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
            '[]'
        )  # true
        assert test is True

    #
    # Examples from README.md.
    #
    def test_exampleInsert(self):
        # Input document: ""
        # Starting cursor position: 0
        # Operation: {"op": "insert", "chars": "Hello, human!"}
        # Output document: "Hello, human!"
        # Ending cursor position: 13
        test = isValid(
            '',
            'Hello, human!',
            '[{"op": "insert", "chars": "Hello, human!"}]'
        )  # true
        assert test is True

    def test_exampleForwardDelete(self):
        # Input document: "What is up?"
        # Starting cursor position: 7
        # Operation: {"op": "delete", "count": 3}
        # Output document: "What is?"
        # Ending cursor position: 7
        test = isValid(
            'What is up?',
            'What is?',
            '[{"op": "skip", "count": 7},{"op": "delete", "count": 3}]'
        )  # true
        assert test is True

    def test_exampleTwoTransformations(self):
        # Input document: "Nice!"
        # Starting cursor position: 0
        # Operation(1): {"op": "skip", "count": 4}
        # Operation(2): {"op": "insert", "chars": " day"}
        # Output document: "Nice day!"
        # Ending cursor position: 8
        test = isValid(
            'Nice!',
            'Nice day!',
            '[{"op": "skip", "count": 4},{"op": "insert", "chars": " day"}]'
        )  # true
        assert test is True

    #
    # extra tests
    #
    def test_unknownOtCommand(self):
        # we expect `ValueError` exception to be raised for an unknown OT command
        self.assertRaises(
            ValueError,
            isValid,
            '',
            '',
            '[{"op": "UNKNOWN_OT_COMMAND"}]'  # bad OT command
        )


if __name__ == '__main__':
    unittest.main()
