#!/bin/bash

modules=`find . | grep '.*tests\.py$' | sed s#\./## | sed s/.py// | sed s#/#.#g`

for m in $modules
do
    echo "Running tests from module "$m
    python -m unittest $m
done

