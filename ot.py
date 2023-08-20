import json


class OperationalTransformation:
    """
    Operational Transformation (OT) takes in a document and starts at position zero.  OT Commands are passed into the
    `transform()` functions that modifies the document based on the json list of OT commands and returns the transformed
    document.

    OT Commands take the following form:
    - Skip - skips X count characters from the current position
        {"op": "skip", "count": 4}

    - Insert - inserts characters at the current position leaving position the same
        {"op": "insert", "chars": " day"}

    - Delete - deletes X number of characters at the current position leaving position the same
        {"op": "delete", "count": 3}
    """
    position = 0

    def __init__(self, document: str):
        self.transformDocument = document

    def skip(self, ot: json):
        """
        Skip the `count` number of positions in the current position

        :param ot: json string of Operational Transformation command
        """
        count = int(ot['count'])
        self.position += count
        self.transformDocument = self.transformDocument if len(self.transformDocument) > self.position else None

    def delete(self, ot: json):
        """
        Deletes X number of characters at the current position
        :param ot: json string of Operational Transformation command
        """
        count = int(ot['count'])
        self.transformDocument = self.transformDocument[:self.position] + self.transformDocument[self.position + count:]

    def insert(self, ot: json):
        """
        Inserts characters at the current position

        :param ot: json string of Operational Transformation command
        """
        chars = ot['chars']
        self.transformDocument = self.transformDocument[:self.position] + chars + self.transformDocument[self.position:]
        self.position += len(chars)

    def transform(self, otjson: json) -> str:
        """
        runs the OT commands against the document

        :param otjson: str  json string of list of Operational Transformation commands
        :return: transformed document string
        """
        otjson = json.loads(otjson)

        for ot in otjson:
            if ot['op'] == 'skip':
                self.skip(ot)
            elif ot['op'] == 'delete':
                self.delete(ot)
            elif ot['op'] == 'insert':
                self.insert(ot)
            else:
                # bad thing, unrecognized operation
                raise ValueError

        return self.transformDocument
