#!/usr/bin/env bash

source config.sh

if [ ! -d ${SOURCE_DIRECTORY} ]; then
    mkdir ${SOURCE_DIRECTORY}
fi

python main.py
cd ${SOURCE_DIRECTORY}

# git commands
if [ ! -d '.git' ]; then
    git init
    git remote add origin ${GITHUB_REMOTE}
fi

git add *
git commit -m 'Auto committed'
git push -u origin master