import glob
import os
import json
import shutil

from jinja2 import Environment, select_autoescape, FileSystemLoader

TEMPLATE_PROPERTY_TYPE = "_type"
TEMPLATE_PROPERTY_EXTENDS = "_extends"
TEMPLATE_PROPERTY_LINKED_TYPES = "_linkedTypes"

EXPANDED_DIR = "expanded"

SCHEMA_FILE_ENDING = ".schema.tpl.json"


def find_resource_directories(root_path):
    resource_directories = set()
    for schema_source in glob.glob(os.path.join(root_path, f'**/*{SCHEMA_FILE_ENDING}'), recursive=True):
        schema_resource_dir = os.path.dirname(schema_source)[len(root_path) + 1:]
        if "target" not in schema_resource_dir and EXPANDED_DIR not in schema_resource_dir:
            path_split = schema_resource_dir.split("/")
            resource_directories.add("/".join([path_split[0], path_split[1]]))
    return list(resource_directories)


def type_to_schema_url(version, t):
    type_base = os.path.dirname(t)
    type_name = os.path.basename(t)
    schema_name = type_name[0].lower()+type_name[1:]
    return f"{type_base}/{version}/{schema_name}?format=json-schema"


def type_to_html_url(version, t):
    type_base = os.path.dirname(t)
    type_name = os.path.basename(t)
    schema_name = type_name[0].lower()+type_name[1:]
    return f"{type_base}/{version}/{schema_name}?format=html"


class Generator(object):

    def __init__(self, format):
        self.format = format
        self.root_path = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
        self.target_path = os.path.join(self.root_path, "target", self.format)

    def generate(self):
        if os.path.exists(self.target_path):
            print("clearing previously generated files")
            shutil.rmtree(self.target_path)
        expanded_path = os.path.join(self.root_path, EXPANDED_DIR)
        for schema_group in find_resource_directories(expanded_path):
            print(f"handle {schema_group}")
            schema_group_path = os.path.join(expanded_path, schema_group)
            version_number = os.path.basename(schema_group_path)
            for schema_path in glob.glob(os.path.join(schema_group_path, f'**/*{SCHEMA_FILE_ENDING}'), recursive=True):
                relative_schema_path = os.path.dirname(schema_path[len(schema_group_path) + 1:])
                schema_file_name = os.path.basename(schema_path)
                schema_file_name_without_extension = schema_file_name[:-len(SCHEMA_FILE_ENDING)]
                with open(schema_path, "r") as schema_file:
                    schema = json.load(schema_file)
                self._pre_process_template(schema, version_number)
                os.makedirs(os.path.join(self.target_path, schema_group, relative_schema_path), exist_ok=True)
                target_file_path = os.path.join(self.target_path, schema_group, relative_schema_path,
                                                f"{schema_file_name_without_extension}.{self.format}")
                print(f"Rendering {target_file_path}")
                with open(target_file_path, "w") as target_file:
                    self._process_template(schema, target_file, version_number)

    def _process_template(self, schema, target_file, version):
        pass

    def _pre_process_template(self, schema, version):
        pass


class JinjaGenerator(Generator):

    def __init__(self, format, autoescape, template_name):
        super().__init__(format)
        self.template_name = template_name
        self.env = Environment(
            loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))),
            autoescape=select_autoescape(autoescape) if autoescape is not None else select_autoescape()
        )

    def _process_template(self, schema, target_file, version):
        target_file.write(self.env.get_template(self.template_name).render(schema))

    def _pre_process_template(self, schema, version):
        pass
