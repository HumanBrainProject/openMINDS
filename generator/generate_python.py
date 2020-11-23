import generator.openminds_helper
import generator.python_compiler

def _generate_all(module):
    for key in module.keys():
        generator.python_compiler.generate_file(module[key])

def generate_all_schemas():
    helper = generator.openminds_helper.OpenMINDS_helper()
    _generate_all(helper.core.schemas)
    _generate_all(helper.SANDS.schemas)
