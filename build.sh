#!/bin/bash

cd src/movie_streaming_silletr

pyinstaller --onefile \
  --name="SiMovieStreaming" \
  --add-data="core/genres.json:core" \
  --add-data="styles.tcss:." \
  --paths="." \
  gui/main_ui.py

mv dist/SiMovieStreaming ../../dist/SiMovieStreaming-linux
rm -rf dist/ build/ *.spec
cd ../..
