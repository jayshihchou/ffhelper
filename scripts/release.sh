#!/bin/sh

rm -R ./build
rm -Rf ./dist
sudo docker rmi build-ffhelper
mkdir -p ./dist
sudo docker build -t build-ffhelper -f docker/Dockerfile .
sudo docker create --name build_ffhelper build-ffhelper --entrypoint /
sudo docker cp build_ffhelper:/app/dist ./
sudo docker rm -f build_ffhelper

python3 -m pip install --upgrade twine
python3 -m twine upload ./dist/ffhelper*.whl --verbose
