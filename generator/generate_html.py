import os

from generator.commons import JinjaGenerator, TEMPLATE_PROPERTY_TYPE, \
    type_to_schema_url, TEMPLATE_PROPERTY_LINKED_TYPES, type_to_html_url


class HTMLGenerator(JinjaGenerator):

    def __init__(self):
        super().__init__("html", ["html", "xml"], "documentation_template.html")

    def _pre_process_template(self, schema, version):
        schema["simpleTypeName"] = os.path.basename(schema[TEMPLATE_PROPERTY_TYPE])
        schema["schemaId"] = type_to_schema_url(version, schema[TEMPLATE_PROPERTY_TYPE])
        schema["schemaVersion"] = version
        for property, propertyValue in schema["properties"].items():
            if TEMPLATE_PROPERTY_LINKED_TYPES in propertyValue:
                propertyValue["typeInformation"] = []
                for linked_type in propertyValue[TEMPLATE_PROPERTY_LINKED_TYPES]:
                    propertyValue["typeInformation"].append({"url": type_to_html_url(version, linked_type),
                                                             "label": os.path.basename(linked_type)})
            elif "type" in propertyValue and "format" in propertyValue:
                propertyValue["typeInformation"] = [{"label": f"{propertyValue['type']} ({propertyValue['format']})"}]
            elif "type" in propertyValue:
                propertyValue["typeInformation"] = [{"label": propertyValue['type']}]
            else:
                propertyValue["typeInformation"] = [{"label": "unknown"}]


if __name__ == "__main__":
    HTMLGenerator().generate()
