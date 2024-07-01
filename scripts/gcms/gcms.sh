#!/bin/sh

echo "Removing previous GovCMS directory."
rm -rf ~/dev/GovCMS

echo "Creating fresh repository."
cd ~/dev
git clone git@github.com:jackwrfuller/GovCMS.git
cd ~/dev/GovCMS

echo "Adding parent fork as remote."
git remote add govcms git@github.com:govCMS/GovCMS.git
git fetch govcms

echo "Done."
