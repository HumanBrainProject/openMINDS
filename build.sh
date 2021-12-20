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
  echo "Building $1"
  echo "*************************"
  echo ""
  git checkout $1
  # Ensure submodules are properly fetched
  if [[ $4 == 'branch' ]]
    then
      git fetch
      # If it's a branch build, we need to make sure we're at the head of the branch
      git reset --hard origin/$1
      git submodule sync
      git submodule update --init --recursive --remote
      git clean -dffx
      # We push the synchronized state of the repository to follow the head of the submodules
      commitAndPush
  elif [[ $4 == 'tag' ]]
    then
      git fetch
      git reset --hard $1
      git submodule sync
      #For tags we explicitly don't set the "--remote" flag (since we want the commit which is recorded as part of the tag
      git submodule update --init --recursive
      git clean -dffx
      # And obviously we don't push back since we don't want to change the tag
  fi

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
      python ../openMINDS_generator/openMINDS.py --path ../openMINDS --reinit --current "$1" --allVersionBranches "$2" --allTags "$3"
    else
      python ../openMINDS_generator/openMINDS.py --path ../openMINDS --current "$1" --allVersionBranches "$2" --allTags "$3"
  fi
  FIRST_BUILD=0
  # Copy expanded schemas into target
  echo "Copy expanded schemas into target"
  mkdir target/schema.tpl.json
  cp -r expanded/* target/schema.tpl.json

  #Also move the version specific property and types files
  mv properties-$1.json target/properties.json
  mv types-$1.json target/types.json
  
  # Copy instances to target
  cp -r instances/* target/instances/
  for d in *
  do 
    if [ -d $d ] && [ "$d" != "target" ] && [ -d "$d/instances" ]
      then 
        TARGET="target/instances/$d/$(cat $d/version.txt)/"
        mkdir -p $TARGET
        echo "Copy instances to target"
        cp -r $d/instances/* $TARGET
      fi
  done

  # Copy documentation
  rm -rf ../openMINDS_documentation/$1
  mkdir -p ../openMINDS_documentation/$1

  # ZIP data
  cd target && zip -r "../../openMINDS_documentation/openMINDS-$1.zip" . && cd ..

  cp -r target/html/* ../openMINDS_documentation/$1
  cp -r target/uml/* ../openMINDS_documentation/$1
  cp -r target/schema.json/* ../openMINDS_documentation/$1
  mv ../openMINDS_documentation/$1/central.html ../openMINDS_documentation/index.html
  cp -r vocab ..
  rm -rf

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

ALL_VERSION_BRANCHES=$(curl -s https://api.github.com/repos/HumanBrainProject/openMINDS/branches | grep -P -o "(?<=\"name\": \")v[0-9]+.*?(?=\")")
ALL_TAGS=$(curl -s https://api.github.com/repos/HumanBrainProject/openMINDS/tags | grep -P -o "(?<=\"name\": \")v[0-9]+.*?(?=\")")
VERSION_BRANCH_LABELS=$(echo $ALL_VERSION_BRANCHES, | tr ' ' ',' | sed 's/.$//')
TAG_LABELS=$(echo $ALL_TAGS | tr ' ' ',')

echo "Building all version-branches (head)"
for version in $ALL_VERSION_BRANCHES;
do if [[ $version =~ ^v[0-9]+.*$ ]]; then build $version "$VERSION_BRANCH_LABELS" "$TAG_LABELS" 'branch'; fi; done

echo "Building all tags"
for version in $ALL_TAGS;
do if [[ $version =~ ^v[0-9]+.*$ ]]; then build $version "$VERSION_BRANCH_LABELS", "$TAG_LABELS" 'tag'; fi; done

#build v1 "v1,v2,v3" "v1.0.0,v2.0.0" 'branch'
