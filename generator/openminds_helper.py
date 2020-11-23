from generator.schema_discovery import Schema_Discovery


class OpenMINDS_helper:
    '''
    Helper class for openMINDS schemas

    This class offers easy discoverability for the schemas of openMINDS core,
    SANDS and the controlledTerms.
    '''

    def __init__(self):
        '''
        Generate the objects that allow schema discovery.

        At the moment we only support the current versions of the schemas.
        '''

        # Set up the folder for schema discovery
        core_folder = "./target/schema.json/core/v3.0/"
        sands_folder = "./target/schema.json/SANDS/v1.0/"

        # Discover schemas available in the folders defined above
        self.core = Schema_Discovery(core_folder)
        self.SANDS = Schema_Discovery(sands_folder)
