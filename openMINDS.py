from expander import Expander
from generate_html import HTMLGenerator
from generate_json_schema import JsonSchemaGenerator


def main():
    print("***************************************")
    print("Triggering the generation of sources...")
    print("***************************************")
    print()
    print("Expanding the schemas...")
    Expander().expand()
    print("Generating JSON schemas")
    JsonSchemaGenerator().generate()
    print("Generating HTML documentation...")
    HTMLGenerator().generate()


if __name__ == "__main__":
    main()
