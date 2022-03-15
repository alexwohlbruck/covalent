#!/bin/bash
yarn install --production=false # installs only dev dependencies
yarn install            # installs prod dependencies
yarn build          # builds the Vue.js app