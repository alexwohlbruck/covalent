#!/bin/sh

git filter-branch --env-filter '

ad=$(( ad + 8294400 ))
cd=$(( cd + 8294400 ))

export GIT_AUTHOR_DATE="$ad"
export GIT_COMMITTER_DATE="$cd"
'