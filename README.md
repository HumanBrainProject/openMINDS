<a href="https://github.com/HumanBrainProject/openMINDS/blob/main/img/openMINDS_logo.png">
    <img src="https://github.com/HumanBrainProject/openMINDS/blob/main/img/openMINDS_logo.png" alt="openMINDS logo" title="openMINDS" align="right" height="70" />
</a>

# Welcome to openMINDS!

The **open** **M**etadata **I**nitiative for **N**euroscience **D**ata **S**tructures, short **openMINDS**, develops and maintains a set of metadata models for research products in the field of neuroscience. As research products, openMINDS considers data originating from human/animal studies or simulations (datasets), computational models (models), software tools (software), as well as metadata/data models (metaDataModels).

The openMINDS project is powered by [HBP](https://www.humanbrainproject.eu) (Human Brain Project) and [EBRAINS](https://ebrains.eu/). However, openMINDS is by design open-source and community-driven, looking for external contributions throughout the neuroscience community.

In order to facilitate contributions from all community member independent of their scientific background, all openMINDS metadata models are defined using a light-weighted schema template syntax. Although this schema template syntax is inspired by JSON-Schema, it outsources most technicalities, making the openMINDS schemas more human-readable, especially for untrained eyes. Behind the scenes, the openMINDS integration pipeline (cf.[openMINDS_generator](https://github.com/HumanBrainProject/openMINDS_generator) GitHub repository) interprets and exends this syntax to formal, well-known formats, such as JSON-Schema or HTML. For each openMINDS version (stable or development), you can browse through and download the resulting schema representations [here](https://humanbrainproject.github.io/openMINDS/).

We, the openMINDS development team, currently unite knowledge from the EBRAINS Curation, the EBRAINS Knowledge Graph, the EBRAINS Atlas, and the INCF Knowledge Space teams. If you have general feedback or a request for a new feature, want to report a bug or have a question, please get in touch with us via our support-email: openminds@ebrains.eu (not active yet). If you spot a bug and know how to fix it, if you want to extend existing schemas and/or metadata models, or develop new schemas and/or metadata models, feel always free to also contribute directly by raising an issue and making a pull request on the respective GitHub repository. For more information on how to contribute, please look [here](./CONTRIBUTING.md).

Note that within EBRAINS, the openMINDS metadata models are adopted by the EBRAINS Knowledge Graph and Interactive Brain Atlas. In addition, openMINDS is currently in the process of being adopted by the Japan Brain/MINDS project.

## Technical overview

In summary, the central openMINDS GitHub repository has a main branch (where you are right now) that hosts the general [README](./README.md) (this document), the [LICENSE document](./LICENSE), a [CONTRIBUTING document](./CONTRIBUTING.md), the openMINDS vocabulary ([vocab](./vocab)), the general [openMINDS logo](./img/openMINDS_logo.png) and a [bash script](./build.sh) that builds the content of the version branches (stable and development). 

On each version branch, a version-specific set of distributed GitHub repositories is ingested as git-submodules, each defining a particular metadata model for neuroscience. In contrast, the openMINDS vocabulary is maintained centrally, because it provides general definitions and references for schema types and properties used across all openMINDS metadata models and their versions.

We chose this modular design to facilitate extensions and maintenance of existing, as well as development and integration of new openMINDS metadata models and schemas. Currently, the following openMINDS metadata models exist (depending on the selected central openMINDS version): [openMINDS_core](https://github.com/HumanBrainProject/openMINDS_core), [openMINDS_SANDS](https://github.com/HumanBrainProject/openMINDS_SANDS), [openMINDS_controlledTerms](https://github.com/HumanBrainProject/openMINDS_controlledTerms), [openMINDS_computation](https://github.com/HumanBrainProject/openMINDS_computation) (in dev), and [openMINDS_ephys](https://github.com/HumanBrainProject/openMINDS_ephys) (in dev).

## How to get started

The stable versions of openMINDS are available as release packages, but are also tagged. The tag/name of a stable version uses the convention `vX.Y`, where `X` identifies the major version number and `Y` the minor version number (for backwards compatible subreleases).

The version branches for the major releases, `vX`, are unstable. On these branches backwards compatible changes are implemented. This can include corrections of typos in instructions, introduction of additional properties to schemas, loosening constraints on expected value numbers or formats, granting additional relations between schemas, and adding new schemas (if they do not require relational changes in existing schemas).

Non-backwards compatible changes are possible on a non-released version branch (no release tag available for this branch). This can include renaming of existing properties, increasing constraints on expected value numbers or formats, removing relations between schemas and adding new schemas, if they cause relational changes in existing schemas.

You can work locally with all stable and unstable version branches using `git clone` instead of downloading a release package:

    git clone https://github.com/HumanBrainProject/openMINDS.git

You can list now the availabel unstable version or feature branches:

	git branch -a
	
Note that you might also see some feature branches of current developments that on the long run will be merged into one of version branches. These feature branches do not follow any naming convention.

You can also list all available release tags:

	git tag -l
	
Next, you either need to checkout the unstable version branch you like to work with, e.g.,:

	git checkout v2

or you checkout a stable version branch via the release tag, e.g.,:

	git checkout tags/<tag_name>

As mentioned above, on each version branch, a version-specific set of distributed GitHub repositories is ingested as git-submodules, each defining a particular metadata model for neuroscience. To be able to use these metadata models, the submodules need to be initialised:

    git submodule init

and updated:

    git submodule update

After completion of this step your local repository is on the most recent state of the selected openMINDS version branch.

## License

openMINDS is licensed under the MIT License.

**Logo:** The openMINDS logo was created by U. Schlegel, based on an original sketch by C. Hagen Blixhavn and feedback by L. Zehl.

## Acknowledgements

The metadata model specification and corresponding open source code was developed in part or in whole in the Human Brain Project, funded from the European Union’s Horizon 2020 Framework Programme for Research and Innovation under Specific Grant Agreements No. 720270, No. 785907, and No. 945539 (Human Brain Project SGA1, SGA2, and SGA3).
