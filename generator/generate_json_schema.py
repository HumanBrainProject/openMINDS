import json
import copy

from generator.commons import TEMPLATE_PROPERTY_TYPE, type_to_schema_url, \
    TEMPLATE_PROPERTY_LINKED_TYPES, Generator


class JsonSchemaGenerator(Generator):

    def __init__(self):
        super().__init__("schema.json")

    @staticmethod
    def _resolve_jsonschema_templates(properties):
        for property_key in properties:
            property = properties[property_key]
            if TEMPLATE_PROPERTY_LINKED_TYPES in property:
                if "type" not in property:
                    # Make sure, that a type is defined - let's default to object
                    property["type"] = "object"
                target = property

                if property["type"] == "array":
                    target = {}
                    property["items"] = target

                target["if"] = {"required": ["@type"]}
                target["then"] = {
                    "properties": {
                        "@id": {
                            "type": "string",
                            "format": "iri"
                        },
                        "@type": {
                            "type": "string",
                            "format": "iri",
                            "enum": property[TEMPLATE_PROPERTY_LINKED_TYPES]
                        }},
                    "required": ["@id"]
                }
                target["else"] = {
                    "properties": {
                        "@id": {
                            "type": "string",
                            "format": "iri"
                        }
                    },
                    "required": ["@id"]
                }
                del property[TEMPLATE_PROPERTY_LINKED_TYPES]

    @staticmethod
    def _clear_template_properties(schema):
        if TEMPLATE_PROPERTY_TYPE in schema:
            del schema[TEMPLATE_PROPERTY_TYPE]

    def _process_template(self, schema, target_file, version):
        schema = copy.deepcopy(schema)
        schema["$schema"] = "http://json-schema.org/draft-07/schema#"

        required = schema["required"] if "required" in schema else []
        required.append("@id")
        required.append("@type")
        schema["required"] = list(set(required))

        if "properties" not in schema:
            schema["properties"] = {}

        properties = schema["properties"]
        properties["@id"] = {
            "type": "string",
            "description": "Metadata node identifier."
        }

        if TEMPLATE_PROPERTY_TYPE in schema:
            schema_id = type_to_schema_url(version, schema[TEMPLATE_PROPERTY_TYPE])
            schema["$id"] = schema_id
            schema["type"] = "object"
            properties["@type"] = {"type": "string", "const": schema[TEMPLATE_PROPERTY_TYPE]}

        self._resolve_jsonschema_templates(schema["properties"])
        self._clear_template_properties(schema)
        target_file.write(json.dumps(schema, indent=4, sort_keys=True))


if __name__ == "__main__":
    JsonSchemaGenerator().generate()
