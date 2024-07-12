#!/bin/sh

# Check a release version is supplied as an argument
if [ -z "$1" ]; then
    echo "A release version must be supplied as an argument"
    exit
fi

# Clone GovCMS locally
cd /tmp
git clone git@github.com:govCMS/GovCMS.git
cd /tmp/GovCMS

# Create release branch with the correct name
git checkout -b release/3.x/"$1"

# Update the govcms.info.yml file to the new GovCMS version
sed -i '' -E "s/version: '(.+)'/version: '"$1"'/" /tmp/GovCMS/govcms.info.yml

# Push changes to repo and clean up
git add /tmp/GovCMS/govcms.info.yml
git commit -m "cut release branch "$1""
git push --set-upstream origin release/3.x/"$1"
rm -rf /tmp/GovCMS
