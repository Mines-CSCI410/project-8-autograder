#!/bin/bash

EXECUTABLE=./VMtranslator

pushd /autograder/source/ >/dev/null

# remove old files
rm -rf ./${1}

# copy test files over
mkdir -p ./${1}
chmod -R ugo+rw ./${1}
cp /autograder/grader/tests/${1}/* ./${1}
cp /autograder/grader/tests/expected-outputs/${1}/*.cmp ./${1}

# run student-submitted code (untrusted)
runuser -u student -- ${EXECUTABLE} ${1}

popd >/dev/null
