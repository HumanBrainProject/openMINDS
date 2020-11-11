import glob
import json
import os
import re

from generator.commons import EXPANDED_DIR, SCHEMA_FILE_ENDING, TEMPLATE_PROPERTY_TYPE

root_path = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
properties_file = os.path.join(root_path, "properties.json")
types_file = os.path.join(root_path, "types.json")


def _camel_case_to_human_readable(value:str):
    return re.sub("([a-z])([A-Z])","\g<1> \g<2>",value).capitalize()

class VocabExtractor(object):

    def _load_properties(self):
        if os.path.exists(properties_file):
            with open(properties_file, "r") as properties_f:
                self.properties = json.load(properties_f)
            for p in self.properties:
                # We want to make sure that only current (not previously existing) schema definitions are reported. This is why we need to clear the array first
                self.properties[p]["schemas"] = []
        else:
            self.properties = {}

    def _load_types(self):
        if os.path.exists(types_file):
            with open(types_file, "r") as types_f:
                self.types = json.load(types_f)
        else:
            self.types = {}

    def _handle_property(self, p, schema):
        if p not in self.properties:
            self.properties[p] = {"name": _camel_case_to_human_readable(p), "description": None, "schemas": []}
        self.properties[p]["schemas"].append(schema)
        self.properties[p]["schemas"] = sorted(set(self.properties[p]["schemas"]))
        self.properties[p]["found"] = True

    def _handle_type(self, type):
        if type not in self.types:
            self.types[type] = {"name": _camel_case_to_human_readable(os.path.basename(type)), "description": None}
        self.types[type]["found"] = True

    def _cleanup_properties(self):
        for p in self.properties:
            if "found" in self.properties[p] and self.properties[p]["found"]:
                del self.properties[p]["found"]
            else:
                self.properties[p]["deprecated"] = True

    def _cleanup_types(self):
        for t in self.types:
            if "found" in self.types[t] and self.types[t]["found"]:
                del self.types[t]["found"]
            else:
                self.types[t]["deprecated"] = True

    def extract(self):
        self._load_types()
        self._load_properties()
        expanded_path = os.path.join(root_path, EXPANDED_DIR)
        for schema_path in glob.glob(os.path.join(expanded_path, f'**/*{SCHEMA_FILE_ENDING}'), recursive=True):
            relative_schema_path = schema_path[len(expanded_path)+1:-len(SCHEMA_FILE_ENDING)]
            with open(schema_path, "r") as schema_file:
                schema = json.load(schema_file)
            type = schema[TEMPLATE_PROPERTY_TYPE]
            self._handle_type(type)
            if "properties" in schema:
                for p in schema["properties"]:
                    self._handle_property(p, relative_schema_path)
        self._cleanup_types()
        self._cleanup_properties()

        with open(types_file, "w") as types_f:
            types_f.write(json.dumps(self.types, sort_keys=True, indent=4))
        with open(properties_file, "w") as properties_f:
            properties_f.write(json.dumps(self.properties, sort_keys=True, indent=4))


if __name__ == "__main__":
    VocabExtractor().extract()
