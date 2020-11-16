# open Metadata Initiative for Neuroscience Data Structures

openMINDS is currently comprised of the following collections of schemas:
- **openMINDS core**: https://github.com/HumanBrainProject/openMINDS_core
- **openMINDS SANDS**: https://github.com/HumanBrainProject/openMINDS_SANDS
- **openMINDS controlledTerms**: https://github.com/HumanBrainProject/openMINDS_controlledTerms

## Template processing
The openMINDS repositories are defining JSON-schema inspired templates with a few custom properties (prefixed with "_") which allow us to simplify the readability and increase the 
reusability. 
To make sure those templates can be used as standard-compliant JSON-schema templates as well as translated into other target formats, we've introduced a small template processing 
pipeline.

### Prerequisites
As pre-requisites, we expect in this repository the template structure to be grouped in a **subdirectory by topic** (e.g. "core" or "SANDS" -> this usually is a GIT submodule to 
allow an easy, individual development of the separate parts of the standards) which contain one **version directory** (e.g. "v1.0") followed by an arbitrary directory structure
allowing to group the templates by topic or anything which allows to simplify the navigation inside the templates. If it is a simple structure, you can also put the templates
immediately to the root level of the version directory. Additionally, we expect the templates to contain the file-ending 
**.schema.json**. Please note that only templates including a **_type** property (see below) will be processed. Templates not containing this property are usually seen as "abstract"
e.g. for the use of the *expansion*.

### 1. Expansion
One of the custom elements introduced is the **_extends** property. It allows to define another (partial) template file (with its relative path to the *version directory*) to be taken
into account as its expansion point. Please note that all defined properties of the referenced template file will be taken into account unless they are overwritten by the template
extending them. This is true for all properties except for **properties** and **required** -> the resulting document will contain a merge of the two documents allowing to define
a basic set of properties and/or required properties in the abstract template and to extend them later on.

The expansion is handled in the **expander.py** which produces a temporary directory called "expanded" which contains the resulting templates. It shall be regarded the source for 
all further generation of code.

### 2. Generation
In a second step, the generation of code is executed. As stated above, the templates follow the JSON-schema standard which can also be interpreted e.g. to generate HTML documentation,
python code or anything you could imagine. The extension points of the JSON-schema standards are the following:

- **_type**: This property expects a single value containing the "type" declaration of a JSON-LD entity. It can be seen as a shortcut for not needing to state *$schema*, *$id* and 
*type* as well as **@type** and **@id** in both, *properties* and *required* - since they can be automatically defined by the applied conventions

- **_linkedTypes**: This property allows to define a JSON-LD link to a restricted set of elements. It expects an array of strings defining potential target types. of this link. 
The default interpretation of this array is *anyOf* allowing the value to be mixed arrays. Please note, that there is also a default to *type: object* - allowing to add only one link. 
If you want to specify an array of links, please specify so by declaring *type: array* explicitly.


There are multiple generators which can be applied to generate various formats such as valid JSON schemas, HTML documentation, wrapper code, etc.
Currently, the following generators are available:

- *generate_json_schema.py*
- *generate_python.py*
- *generate_html.py*
