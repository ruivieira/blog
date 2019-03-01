#!/usr/bin/env bash
cd ../ruivieira.github.io.output
git init
git remote add origin git@github.com:ruivieira/ruivieira.github.io.git
git add --all
git commit -m "Automated update"
git push --set-upstream origin master -f
cd ../ruivieira.github.io