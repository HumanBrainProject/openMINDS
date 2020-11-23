from generator.expander import Expander
from generator.generate_html import HTMLGenerator
from generator.generate_json_schema import JsonSchemaGenerator
from generator.vocab_extractor import VocabExtractor
from generator.generate_python import generate_all_schemas


def main():
    print("***************************************")
    print("Triggering the generation of sources...")
    print("***************************************")
    print()
    print("Expanding the schemas...")
    Expander().expand()
    print("Extracting the vocabulary...")
    VocabExtractor().extract()
    print("Generating JSON schemas...")
    JsonSchemaGenerator().generate()
    print("Generating HTML documentation...")
    HTMLGenerator().generate()
    print("Generating Python classes...")
    generate_all_schemas()



if __name__ == "__main__":
    main()
