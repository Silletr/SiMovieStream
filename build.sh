#!/bin/bash
set -e
cd src/movie_streaming_silletr
pyinstaller --onefile \
  --name="SiMovieStreaming" \
  --add-data="core/genres.json:core" \
  --add-data="styles.tcss:." \
  --collect-all=python_dotenv \
  --collect-all=dotenv \
  --hidden-import=python_dotenv \
  --hidden-import=dotenv \
  --hidden-import=load_dotenv \
  --paths="." \
  gui/main_ui.py
mkdir -p ../../dist
mv dist/SiMovieStreaming ../../dist/SiMovieStreaming-linux
rm -rf dist/ build/ *.spec
cd ../..
