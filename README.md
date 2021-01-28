<a href="https://github.com/HumanBrainProject/openMINDS/blob/v1/img/openMINDS_logo.png">
    <img src="https://github.com/HumanBrainProject/openMINDS/blob/v1/img/openMINDS_logo.png" alt="openMINDS logo" title="openMINDS" align="right" height="70" />
</a>

# Welcome to openMINDS!

The **open** **M**etadata **I**nitiative for **N**euroscience **D**ata **S**tructures, short **openMINDS**, develops and maintains a set of metadata models for research products in the field of neuroscience. As research products, openMINDS considers data originating from human/animal studies or simulations (datasets), computational models (models), software tools (software), as well as metadata/data models (metaDataModels).

Currently, openMINDS is comprised of the following metadata graph models:  
- [**openMINDS_core**](https://github.com/HumanBrainProject/openMINDS_core) metadata model contains schemas that can be used to describe the general origin, location and content of research products. The openMINDS_core schemas cover the basic integration of research products into the EBRAINS Knowledge Graph.
- [**openMINDS_SANDS**](https://github.com/HumanBrainProject/openMINDS_SANDS) metadata model contains schemas that can be used to identify and describe brain atlases, as well as describe the anatomical anchoring or registration of datasets to these brain atlases. The openMINDS_SANDS schemas cover the spatial integration of research products (in particular datasets) into the EBRAINS Atlases.
- [**openMINDS_controlledTerms**](https://github.com/HumanBrainProject/openMINDS_controlledTerms) metadata model contains schemas and the corresponding terminologies (as JSON-LDs) to be use (within the EBRAINS Knowledge Graph and Atlases). Where applicable, the defined terms are connected to a matching ontological term. Schemas of openMINDS_core as well as openMINDS_SANDS reference to these controlled terms.

The openMINDS project is powered by [HBP](https://www.humanbrainproject.eu) (Human Brain Project) and [EBRAINS](https://ebrains.eu/) (European Brain ReseArch INfraStructure) and maintained by a small development team. Within EBRAINS, the openMINDS metadata models are adopted by the EBRAINS Knowledge Graph and Atlases.

## How to get started
To get started the first step is to either clone the repository or download a
release.

    git clone https://github.com/HumanBrainProject/openMINDS.git

The repository is structured in a way that the different metadata models are provided via the following submodules
* openMINDS_core
* openMINDS_SANDS
* openMINDS_controlledTerms

To be able to use the collection the submodules need to be initialised

    git submodule init

and updated

    git submodule update

After completion of this step your local repository is on the current state of
all collections.
Now you are able to run the script to generate the JSON-schema-files,
HTML-files and Python files.

    python openMINDS.py

The generated files can be found in the `target` folder.

## Processing pipeline
The metadata schemas in the openMINDS repositories are first defined as JSON-schema inspired schema-templates with a few custom template-properties (prefixed with `"_"`) which allow us to simplify their readability and increase their reusability.

To make sure those schema-templates can be used as standard-compliant JSON-schemas or translated into other target formats (e.g., HTML), we've introduced a small processing pipeline.

### Prerequisites
As prerequisites, we expect the schema-templates to be grouped in **schema collections** (e.g., the openMINDS_core or openMINDS_SANDS) and managed as GIT submodules to allow an easy, individual development of the separate parts of the standards.

Each schema collection has to contain a **version directory** (e.g. "v1.0") followed by an arbitrary directory structure. Within a version directory, the schema-templates can either be further grouped for simplifying navitation, or listed directly at the root level.

All schema-templates in the openMINDS collections need to contain the file-ending **.schema.tpl.json**. In addition, please note that only templates including a **`"_type"`** property (see below) will be processed. Schema-templates not containing this property are interpreted as "abstract", which need to be extended by other (partial) schema-templates (cf. *1. Expansion*).

### 1. Expansion
Within the schema-templates, one of the introduced custom template-properties is the **`"_extends"`** property. It allows us to define an "abstract" schema-template file (with its relative path to the *version directory*) to be taken into account as expansion.

Please note that all defined template-properties of the referenced "abstract" schema-template file will be taken into account unless they are overwritten by the schema-template extending them. This is true for all template-properties except for **`"properties"`** and **`"required"`** which are merged in the combined document ("abstract" schema-template + expansion schema-template). This facilitates the maintenance of the schemas in cases where a subset of **`"properties"`** (required or not) remains the same across several templates.

The expansion processing is handled in the **expander.py** which produces a temporary directory called "expanded" which contains the correspondingly merged schema-templates. It shall be regarded the source for all further generation of code.

### 2. Generation
In a second step, the generation of valid JSON-Schemas, HTML documentation, and other wrapper code is executed. The extension points of the JSON-schema standards are the following:

- **`"_type"`**: This template-property expects a single value containing the "type" declaration of a JSON-LD entity. It can be seen as a shortcut for not needing to state the JSON-schema properties `"$schema"`, `"$id"` and `"type"` as well as the JSON-LD properties `"@type"` and `"@id"` in the schema-templates - since they can be automatically defined by the applied conventions.

- **`"_linkedTypes"`**: This template-property allows to define a JSON-LD link to a restricted set of elements. It expects an array of strings defining potential target types of this link. The default interpretation of this array is `"anyOf"` allowing the value to be mixed arrays. Please note, that there is also a default to `"type": "object"` - allowing to add only one link. If you want to specify an array of links, please specify so by declaring `"type": "array"` explicitly.


There are multiple generators which can be applied to generate various formats such as valid JSON schemas, HTML documentation, wrapper code, etc.
Currently, the following generators are available:

- *generate_json_schema.py*
- *generate_python.py*
- *generate_html.py*

## How to contribute
Please check our [contribution document](./CONTRIBUTING.md).

## License
This work is licensed under the MIT License.
