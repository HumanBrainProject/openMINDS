import glob
import json
import os
import shutil

from commons import TEMPLATE_PROPERTY_EXTENDS, TEMPLATE_PROPERTY_TYPE, find_resource_directories, EXPANDED_DIR

DEEP_MERGE_PROPERTIES = ["properties", "required"]
root_path = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

class Expander(object):

    @staticmethod
    def expand():
        absolute_target_dir = os.path.realpath(os.path.join(root_path, EXPANDED_DIR))
        if os.path.exists(absolute_target_dir):
            print("clearing previously generated expanded sources")
            shutil.rmtree(absolute_target_dir)
        for schema_group in find_resource_directories(root_path):
            print(f"handling schemas of {schema_group}")
            absolute_schema_group_target_dir = os.path.realpath(os.path.join(absolute_target_dir, schema_group))
            absolute_schema_group_src_dir = os.path.join(root_path, schema_group)
            os.makedirs(absolute_schema_group_target_dir)
            for schema_path in glob.glob(os.path.join(root_path, schema_group, '**/*.schema.json'), recursive=True):
                relative_schema_path = schema_path[len(absolute_schema_group_src_dir)+1:]
                print(f"process {relative_schema_path}")
                with open(schema_path, "r") as schema_file:
                    schema = json.load(schema_file)
                if TEMPLATE_PROPERTY_TYPE not in schema:
                    print(f"Skipping schema {relative_schema_path} because it doesn't contain a valid type")
                else:
                    schema_target_path = os.path.join(absolute_schema_group_target_dir, relative_schema_path)
                    Expander._process_schema(schema, absolute_schema_group_src_dir)
                    os.makedirs(os.path.dirname(schema_target_path), exist_ok=True)
                    with open(schema_target_path, "w") as target_file:
                        target_file.write(json.dumps(schema, indent=4))

    @staticmethod
    def _process_schema(schema, absolute_schema_group_src_dir):
        if TEMPLATE_PROPERTY_EXTENDS in schema:
            extension_path = os.path.realpath(os.path.join(absolute_schema_group_src_dir, schema[TEMPLATE_PROPERTY_EXTENDS]))
            if extension_path.startswith(absolute_schema_group_src_dir):
                # Only load the extension if it is part of the same schema group
                # (prevent access of resources outside of the directory structure)
                with open(extension_path, "r") as extension_file:
                    extension = json.load(extension_file)
                Expander._apply_extension(schema, extension)
            del schema[TEMPLATE_PROPERTY_EXTENDS]
        return schema

    @staticmethod
    def _apply_extension(source, extension):
        for extension_key in extension:
            if extension_key in DEEP_MERGE_PROPERTIES and extension_key in source:
                if type(source[extension_key]) is list and type(extension[extension_key]) is list:
                    source[extension_key] = source[extension_key]+extension[extension_key]
                elif type(source[extension_key]) is dict and type(extension[extension_key]) is dict:
                    for property_key in extension[extension_key]:
                        if property_key not in source[extension_key]:
                            source[extension_key][property_key] = extension[extension_key][property_key]
            if extension_key not in source:
                source[extension_key] = extension[extension_key]


if __name__ == "__main__":
    Expander().expand()
