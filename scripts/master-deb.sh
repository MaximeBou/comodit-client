#!/bin/bash

set e

echo
echo "# Build comodit-client ... "
./build-deb.sh

echo
echo "# Build comodit-client for all distributions in config file ... "
./build-all-deb.sh
