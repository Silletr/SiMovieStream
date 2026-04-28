#!/bin/bash
set -e
cd src/movie_streaming_silletr/

python -m nuitka \
  --onefile \
  --msvc=latest \
  --enable-plugin=no-qt \
  --include-data-dir=.=movie_streaming_silletr \
  --include-data-file=core/genres.json=core/genres.json \
  --include-data-file=styles.tcss=styles.tcss \
  --include-data-file=../../.env=.env \
  --follow-import-to=flet.pubsub \
  --nofollow-import-to=flet.testing \
  gui/main_ui.py

mkdir -p ../../dist
mv gui/main_ui ../../dist/SiMovieStreaming-Linux
rm -rf gui/main_ui.build
cd ../..
