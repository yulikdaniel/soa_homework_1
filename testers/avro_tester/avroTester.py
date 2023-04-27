import serializable
from avro.schema import parse
from avro.io import BinaryEncoder, BinaryDecoder, DatumReader, DatumWriter
from io import BytesIO
import logging

schema = parse('''
{
    "namespace": "stress.avro",
    "type": "record",
    "name": "TPerson",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "age", "type": "int"},
        {"name": "contacts",  "type":
            {
                "type": "record",
                "name": "TContacts",
                "fields": [
                    {"name": "phone", "type": "int"},
                    {"name": "email", "type": "string"}
                ]
            }
        },
        {"name": "friends", "type": {
            "type": "array", "items":
            [{
                "name": "friend", "type": "string"
            }]
            }
        },
        {"name": "apeIndex", "type": "float"}
    ]
}''')

class AvroChecker(serializable.Checker):
    def __init__(self, schema):
        self.schema = schema

    def serialize(self, arg):
        bytes_writer = BytesIO()
        encoder = BinaryEncoder(bytes_writer)
        writer1 = DatumWriter(self.schema)
        writer1.write(arg, encoder)
        return bytes_writer.getvalue()

    def deserialize(self, string):
        bytes_reader = BytesIO(string)
        decoder = BinaryDecoder(bytes_reader)
        reader = DatumReader(self.schema)
        return reader.read(decoder)
    
def run_tests():
    return serializable.run_tests(AvroChecker(schema))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(run_tests())