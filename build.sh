#!/bin/bash

# The script requires the openMIINDS repository to be cloned in the same root directory into the directory "openMINDS_documentation".
# This needs to be done externally since we need to push back to it and this can only be achieved when the repo is cloned via the workflow action
if [ ! -d "openMINDS_documentation" ]; then
  echo "You need to clone openMINDS (SSH) to the directory openMINDS_documentation first, before you can run the build script"
  echo "In the console, execute git clone 'git@github.com:HumanBrainProject/openMINDS.git' openMINDS_documentation"
  exit 1
fi

build(){
  echo "Building version $version"
  git checkout $version
  # Ensure submodules are properly fetched
  git pull
  git submodule sync
  git submodule update --init --recursive --remote

  # Linting...
  # stop the build if there are Python syntax errors or undefined names
  flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
  # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
  flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

  # Run the generator logic
  python ../openMINDS_generator/openMINDS.py --path ../openMINDS

  # Copy expanded schemas into target
  mkdir target/schema.tpl.json
  cp -r expanded/* target/schema.tpl.json
  cd target

  # ZIP data
  zip -r ../../openMINDS_documentation/$version .

  # Copy documentation
  rm -rf ../../openMINDS_documentation/$version
  mkdir -p ../../openMINDS_documentation/$version
  cp -r html/* ../../openMINDS_documentation/$version
  cp -r uml/* ../../openMINDS_documentation/$version
  cp -r schema.json/* ../../openMINDS_documentation/$version
  cd ..
}

echo "Clearing existing elements..."
rm -rf openMINDS
rm -rf openMINDS_generator

echo "Cloning openMINDS_generator and installing requirements"
git clone https://github.com/HumanBrainProject/openMINDS_generator.git
cd openMINDS_generator
git pull
git reset --hard origin/main
python -m pip install --upgrade pip
pip install flake8 pytest
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
cd ..

echo "Ensure documentation branch in openMINDS_documentation"
cd openMINDS_documentation
git checkout documentation
git pull
git reset --hard origin/documentation
#Remove all content since it should be fully reconstructed
rm -rf *
cd ..

echo "Cloning into openMINDS"
git clone https://github.com/HumanBrainProject/openMINDS.git
cd openMINDS
git pull
git reset --hard origin/v2 #TODO change to master branch once it's available

echo "Building all versions"
for version in $(curl -s https://api.github.com/repos/HumanBrainProject/openMINDS/branches | grep -P -o "(?<=\"name\": \").*?(?=\")");
do if [[ "$version" != "main" && "$version" != "documentation" ]]; then build $version; fi; done