import json


class OperationalTransformation:
    position = 0

    def __init__(self, document: str):
        self.transformDocument = document

    def skip(self, document: str, ot: json) -> str:
        count = int(ot['count'])
        self.position += count
        return document if len(document) > self.position else None

    def delete(self, document: str, ot: json) -> str:
        count = int(ot['count'])
        return document[:self.position] + document[self.position + count:]

    def insert(self, document: str, ot: json) -> str:
        chars = ot['chars']
        transformedDocument = document[:self.position] + chars + document[self.position:]
        self.position += len(chars)
        return transformedDocument

    def transform(self, otjson: str) -> str:
        """
        runs the OT commands against the document

        :param otjson: json string
        :return: transformed document string
        """
        self.otjson = json.loads(otjson)

        transformed = self.transformDocument
        for ot in self.otjson:
            if ot['op'] == 'skip':
                transformed = self.skip(transformed, ot)
            elif ot['op'] == 'delete':
                transformed = self.delete(transformed, ot)
            elif ot['op'] == 'insert':
                transformed = self.insert(transformed, ot)
            else:
                # bad thing, unrecognized operation
                raise Exception

        return transformed


def isValid(document: str, latest: str, otjson: str):
    otDoc = OperationalTransformation(document).transform(otjson)
    return otDoc == latest
