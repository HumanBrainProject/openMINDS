import glob
import json
import os

import jsonschema
from jsonschema import Draft7Validator, ValidationError

from generator.commons import find_resource_directories


def _parse_example_filename(file_name):
    schema_name = f"{file_name.split('-')[0]}.schema.json"
    expect_failure = file_name.endswith("-nok.json")
    return schema_name, expect_failure


def _do_validate(schema_path, example_path, expect_failure):
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
    Draft7Validator.check_schema(schema)
    with open(example_path, 'r') as example_file:
        example = json.load(example_file)
    if expect_failure:
        try:
            jsonschema.validate(example, schema)
            raise ValidationError(AssertionError(f"Was expecting a validation error for {os.path.basename(example_path)}"))
        except ValidationError:
            print(f"Validation failed as expected for {os.path.basename(example_path)}")
    else:
        try:
            jsonschema.validate(example, schema)
            print(f"Validation succeeded as expected for {os.path.basename(example_path)}")
        except ValidationError as e:
            print(f"Validation failed for {os.path.basename(example_path)}")
            raise e


def test_examples():
    script_path = os.path.dirname(os.path.realpath(__file__))
    for schema_group in find_resource_directories(script_path):
        schema_group_dir = os.path.join(script_path, schema_group)
        for example in glob.glob(os.path.join(schema_group_dir, '**/test/*.json'), recursive=True):
            relative_example_path = os.path.realpath(example)[len(schema_group_dir) + 1:]
            file_name = os.path.basename(relative_example_path)
            schema_name, expect_failure = _parse_example_filename(file_name)
            print(f"Testing {example} against the schema {schema_name}")
            json_schema = os.path.join(script_path, "target/schema.json",
                                       schema_group, os.path.dirname(os.path.dirname(relative_example_path)), schema_name)
            _do_validate(json_schema, example, expect_failure)


if __name__ == "__main__":
    test_examples()
