#!/bin/bash

# The script requires the openMIINDS repository to be cloned in the same root directory into the directory "openMINDS_documentation".
# This needs to be done externally since we need to push back to it and this can only be achieved when the repo is cloned via the workflow action
if [ ! -d "openMINDS_documentation" ]; then
  echo "You need to clone openMINDS (SSH) to the directory openMINDS_documentation first, before you can run the build script"
  echo "In the console, execute git clone 'git@github.com:HumanBrainProject/openMINDS.git' openMINDS_documentation"
  exit 1
fi

commitAndPush(){
  git config user.name openMINDS
  git config user.email openMINDS@ebrains.eu
  if [[ $(git add . --dry-run | wc -l) -gt 0 ]]; then
     git add .
     git commit -m "Update submodule references"
     git push
  else
     echo "Nothing to commit"
  fi
}


FIRST_BUILD=1
build(){
  echo ""
  echo "*************************"
  echo "Building version $1 (out of $2)"
  echo "*************************"
  echo ""
  git checkout $1
  # Ensure submodules are properly fetched
  git pull
  # Make sure we're at the head of the branch
  git reset --hard origin/$1
  git submodule sync
  git submodule update --init --recursive --remote
  # We push the synchronized state of the repository
  commitAndPush

  #Use the vocab from the central repository - we remove an existing one (although there should be none)
  rm -rf vocab
  cp -r ../vocab .

  # Linting...
  # stop the build if there are Python syntax errors or undefined names
  flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
  # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
  flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

  # Run the generator logic
  if [[ $FIRST_BUILD == 1 ]]
    then
      echo "First build"
      python ../openMINDS_generator/openMINDS.py --path ../openMINDS --reinit --currentVersion "$1" --allVersions "$2"
    else
      python ../openMINDS_generator/openMINDS.py --path ../openMINDS --currentVersion "$1" --allVersions "$2"
  fi
  FIRST_BUILD=0
  # Copy expanded schemas into target
  echo "Copy expanded schemas into target"
  mkdir target/schema.tpl.json
  cp -r expanded/* target/schema.tpl.json

  # Copy documentation
  rm -rf ../openMINDS_documentation/$1
  mkdir -p ../openMINDS_documentation/$1

  # ZIP data
  cd target && zip -r ../../openMINDS_documentation/$1 . && cd ..
  cp -r target/html/* ../openMINDS_documentation/$1
  cp -r target/uml/* ../openMINDS_documentation/$1
  cp -r target/schema.json/* ../openMINDS_documentation/$1
  mv ./openMINDS_documentation/$1/central.html ./openMINDS_documentation/index.html
  cp -r vocab ..
}

echo "Clearing existing elements..."
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

cd openMINDS
echo "Building all versions"
ALL_VERSIONS=$(curl -s https://api.github.com/repos/HumanBrainProject/openMINDS/branches | grep -P -o "(?<=\"name\": \")v[0-9]+.*?(?=\")")
for version in $ALL_VERSIONS;
do if [[ $version =~ ^v[0-9]+.*$ ]]; then build $version "$(echo $ALL_VERSIONS | tr ' ', ',')"; fi; done
#build "v1"