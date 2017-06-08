#!/bin/bash
str=$( eval "git ls-remote --tags https://github.com/nwmqpa/OVH")
if echo "$str" | grep 'v$TRAVIS_BUILD_NUMBER'; then
    exit
else
  git config --global user.email "$BUILDEREMAIL"
  git config --global user.name "$BUILDERNAME"
  export GIT_TAG=v$TRAVIS_BUILD_NUMBER
  git tag $GIT_TAG -a -m "Build #$TRAVIS_BUILD_NUMBER"
  git push -q https://$TAGPERM@github.com/nwmqpa/OVH --tags
fi
