#!/bin/bash

EXECUTABLE=./virtualmachine

pushd /autograder/source/ >/dev/null

# remove old files
rm -f *.{vm,asm,tst}

# copy test files over
cp /autograder/grader/tests/${1}.{vm,tst} .

# run student-submitted code (untrusted)
runuser -u student -- ${EXECUTABLE} $(pwd)/${1}.vm

popd >/dev/null
