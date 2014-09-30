#!/bin/bash

if ! which lsb_release ; then
	echo "lsb-release needs to be installed to run this script"
	exit 1
fi

if [ ! -f debian/changelog ] ; then
	echo "Hmm can't find debian/changelog, in the wrong directory perhaps?"
	exit 2
fi

dist=$(lsb_release -c | awk '{print $2}')
echo "Found Dist: $dist"
echo "Updating debian/changelog"
sed -i "s/%DIST%/$dist/g" debian/changelog
echo "Building package"
dpkg-buildpackage -S
echo "Reverting Changelog"
git checkout debian/changelog
