import os.path


class Schema_Discovery:
    '''
    Schema Discovery in a given folder.

    This class walks through the available files in a given folder in search of
    json.schema files and adds them as attributes of itself.
    The idea is to offer an easy programmatical way to the schemas available.
    '''

    def __init__(self, folder, namespace):
        schemas = []
        subfolder = False
        for root, dirs, files in os.walk(folder):
            for name in files:
                schemas.append(os.path.join(root, name))

                # Right now we assume that we don't have a mixed situation with
                # schema files in root and in subfolders.
                #
                # If that should change in the future this needs to be updated.
                if root is not folder:
                    subfolder = True

        for schema_filename in schemas:
            stripped_filename = os.path.splitext(
                                    os.path.splitext(
                                        os.path.basename(schema_filename)
                                    )[0]
                                )[0]

            if subfolder:
                setattr(self,
                        schema_filename.split('/')[-2].upper() + "__" + stripped_filename.upper(),
                        {
                            "filename": schema_filename,
                            "name": stripped_filename,
                            "namespace": namespace,
                            "substructure": schema_filename.split('/')[-2]
                        }
                )
            else:
                setattr(self,
                        stripped_filename.upper(),
                        {
                            "filename": schema_filename,
                            "name": stripped_filename,
                            "namespace": namespace
                        }
                       )
