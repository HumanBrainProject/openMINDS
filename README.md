<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/HumanBrainProject/openMINDS/blob/main/img/dark_openMINDS-logo.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/HumanBrainProject/openMINDS/blob/main/img/light_openMINDS-logo.svg">
  <img alt="openMINDS controlledTerms logo" src="https://github.com/HumanBrainProject/openMINDS/blob/main/img/dark_openMINDS-logo.svg"  title="openMINDS" align="right" height="70">
</picture>

# Welcome to openMINDS! <a name="welcome"/>

The **open** **M**etadata **I**nitiative for **N**euroscience **D**ata **S**tructures, short **openMINDS**, is a metadata framework that develops and maintains a set of metadata models as well as libraries of controlled terminologies, brain atlases, and common coordinate spaces for neuroscience graph databases.

Note that this GitHub only hosts a summary of the openMINDS documentation. For a full documenation please navigate to the [**openMINDS Collab**](https://wiki.ebrains.eu/bin/view/Collabs/openminds/). For browsing through schemas and lists of all controlled terminologies, brain atlases, and common coordinate spaces please navigate to the [**openMINDS HTML docu**](https://humanbrainproject.github.io/openMINDS/).

**You need help?** Just get in touch via GitHub issue trackers, or our support email: **`openminds@ebrains.eu`**

## Documentation (summary) <a name="docu-summary"/>

Depending on the version (cf. GitHub branches), openMINDS currently ingests the following metadata models:  

[openMINDS_core](https://github.com/HumanBrainProject/openMINDS_core) - covers general origin, location and content of research products.  
[openMINDS_SANDS](https://github.com/HumanBrainProject/openMINDS_SANDS) - covers brain atlases, as well as anatomical locations and relations of non-atlas data.  
[openMINDS_controlledTerms](https://github.com/HumanBrainProject/openMINDS_controlledTerms) - covers consistent definitions of neuroscience terms.  
[openMINDS_computation](https://github.com/HumanBrainProject/openMINDS_computation)<sup> (in dev)</sup> - covers provenance of simulations, data analysis and visualizations in neuroscience.  
[openMINDS_publications](https://github.com/HumanBrainProject/openMINDS_publications)<sup> (in dev)</sup> - covers definitions for scholarly publications, including live papers.  
[openMINDS_chemicals](https://github.com/HumanBrainProject/openMINDS_chemicals)<sup> (in dev)</sup> - covers consistent definitions of chemical substances and mixtures.  
[openMINDS_ephys](https://github.com/HumanBrainProject/openMINDS_ephys)<sup> (in dev)</sup> - covers provenance of electrophysiology experiments.  

#### What you can find below:
1. [How to contribute](#how-to-contribute) 
2. [Technical overview & guidelines](#technical-overview-and-guidelines)
3. [How to get started](#how-to-get-started)
4. [License, adoptions & acknowledgements](#license-adoptions-acknowledgements)

---

## How to contribute <a name="how-to-contribute"/>

The openMINDS development team currently unites knowledge from the EBRAINS Curation Service, the EBRAINS Knowledge Graph, the EBRAINS Atlas Service, and the INCF Knowledge Space teams. **Contributions from the whole community are welcome and highly appreciated!**

In order to facilitate contributions from all community members independent of their scientific background, all openMINDS metadata models are defined using a light-weighted schema template syntax. Although this schema template syntax is inspired by JSON-Schema, it outsources most technicalities, making the openMINDS schemas more human-readable, especially for untrained eyes. 

If you have general feedback or a request for a new feature, want to report a bug or have a question, please get in touch with us via our support-email (**`openminds@ebrains.eu`**) or via the issue tracker on one of our GitHub repositories. You can also follow or actively participate in the discussions on the [openMINDS Community Forum](https://neurostars.org/t/openminds-community-forum-virtual/20156) on INCF NeuroStars.

If you spot a bug and know how to fix it, if you want to extend existing schemas and/or metadata models, or develop new schemas and/or metadata models, feel always free to contribute directly by raising an issue and making a pull request on the respective GitHub repository. 

For more information on how to contribute, please have a look at our [CONTRIBUTING](./CONTRIBUTING.md) document.

[BACK TO TOP](#welcome)

## Technical overview & guidelines <a name="technical-overview-and-guidelines"/>

In summary, the central openMINDS GitHub repository has a **main** branch (where you are right now), a **documentation** branch, and **version** branches (naming convention: `vX`; e.g., `v1`). Official releases (naming convention: `vX.Y`; e.g., `v1.0`) are tagged and provided as release packages.

The **main** branch hosts the general [README](./README.md) (this document), the [LICENSE](./LICENSE) document, the [CONTRIBUTING](./CONTRIBUTING.md) document,  and the general [openMINDS logo](./img/openMINDS_logo.png). In addition, it maintains the openMINDS vocabulary ([vocab](./vocab)) which provides general definitions and references for schema types and properties used across all openMINDS metadata models and their versions, and the [bash script](./build.sh) that builds the content of the documentation and version branches.

The **documentation** branch hosts the HTML files that build the [openMINDS GitHub pages](https://humanbrainproject.github.io/openMINDS/), as well as a ZIP file for each version branch and official release containing the respective openMINDS schemas in the currently supported formats, such as the openMINDS syntax (`.schema.tpl.json`), JSON-Schema (`.schema.json`), or HTML (`.html`).

The **version** branches host the respective openMINDS schemas of a major version by ingesting the corresponding metadata models as git-submodules. We chose this modular design to facilitate extensions and maintenance of existing, as well as development and integration of new openMINDS metadata models and schemas. Note that the version branches can have official release tags. 

If a version branch has an official release tag, only backwards compatible changes can be merged on this branch. This can include corrections of typos in instructions, introduction of additional properties to schemas, loosening constraints on expected value numbers or formats, granting additional relations between schemas, and adding new schemas (if they do not require relational changes in existing schemas). Except for typo corrections, these changes are typically tagged as sub-releases for the respective major version (e.g., v1.1). 

If a version branch does not have an official release tag, yet, also non-backwards compatible changes can be merged on this branch. This can include renaming of existing properties, increasing constraints on expected value numbers or formats, removing relations between schemas and adding new schemas, if they cause relational changes in existing schemas. In case all version branches have official release tags, a new non-backwards compatible change would lead to the creation of a new version branch (with a respectively increased major version number).

The setup of the central openMINDS GitHub repository is maintained by the openMINDS integration pipeline (cf. [openMINDS_generator](https://github.com/HumanBrainProject/openMINDS_generator) GitHub repository). The pipeline is configured in such a way, that each commit on one of the openMINDS submodules will trigger a new build of the central openMINDS repository ensuring that its content is always up-to-date. This pipeline also interprets and extends the openMINDS schema syntax to other schema representation formats (such as JSON-Schema, see above).

[BACK TO TOP](#welcome)

## How to get started <a name="how-to-get-started"/>

You can either download one of the release packages, or use `git clone` to be able to work locally with released versions or the "unstable" version branches:
	
	git clone https://github.com/HumanBrainProject/openMINDS.git

Once, you cloned the repository, you can list the availabel version branches:

	git branch -a
	
and checkout the one you like to work on, e.g.,:

	git checkout v2
	
Note that you might also see some feature branches of current developments that on the long run will be merged into one of version branches. These feature branches do not follow any naming convention.

If you rather like to work with a stable release, you can also list all available release tags:

	git tag -l
	
and checkout the stable version branch you like to work with via the respective release tag, e.g.,:

	git checkout tags/<tag_name>

As mentioned above, on each version branch, a version-specific set of distributed GitHub repositories is ingested as git-submodules, each defining a particular metadata model for neuroscience. To be able to use these metadata models, the submodules need to be initialised:

	git submodule init

and updated:
	
	git submodule update

After completion of this step your local repository is on the most recent state of the selected openMINDS version branch.

[BACK TO TOP](#welcome)

## License, adoptions & acknowledgements <a name="license-adoptions-acknowledgements"/>

openMINDS is licensed under the MIT License.

Within EBRAINS, the openMINDS metadata models are adopted by the EBRAINS Knowledge Graph and Interactive Brain Atlas. In addition, openMINDS is currently in the process of being adopted by the Japan Brain/MINDS project.

**Logo:** The openMINDS logo was created by U. Schlegel, based on an original sketch by C. Hagen Blixhavn and feedback by L. Zehl.

The openMINDS project is powered by [HBP](https://www.humanbrainproject.eu) (Human Brain Project) and [EBRAINS](https://ebrains.eu/): The metadata model specifications as well as surrounding code and tools were developed developed in part or in whole in the Human Brain Project, funded from the European Union’s Horizon 2020 Framework Programme for Research and Innovation under Specific Grant Agreements No. 720270, No. 785907, and No. 945539 (Human Brain Project SGA1, SGA2, and SGA3).

[BACK TO TOP](#welcome)
