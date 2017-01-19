#!/usr/bin/env bash
#Should work on debian 7 and Ubuntu 14.04 and 16.04

sudo apt-get install python-numpy swig python-dev python-wheel pkg-config zip unzip
wget https://github.com/bazelbuild/bazel/releases/download/0.2.2b/bazel_0.2.2b-linux-x86_64.deb
sudo dpkg -i bazel_0.2.2b-linux-x86_64.deb
cd tensorflow-models/syntaxnet/tensorflow
# in order to have https://github.com/tensorflow/tensorflow/issues/3092 fixed
wget https://github.com/fayeshine/tensorflow/commit/76f6e0a184b7d98a0eb9ae84670b45802a2116c5.patch
git apply --whitespace=warn 76f6e0a184b7d98a0eb9ae84670b45802a2116c5.patch
rm 76f6e0a184b7d98a0eb9ae84670b45802a2116c5.patch
./configure
cd ..
bazel test syntaxnet/... util/utf8/...
mkdir universal_models
cd universal_models
for LANG in Ancient_Greek-PROIEL Basque Bulgarian Chinese Croatian Czech Danish Dutch English Estonian Finnish French Galician German Greek Hebrew Hindi Hungarian Indonesian Italian Latin-PROIEL Norwegian Persian Polish Portuguese Russian Slovenian Spanish Swedish; do
    wget http://download.tensorflow.org/models/parsey_universal/${LANG}.zip
    unzip ${LANG}.zip
    rm ${LANG}.zip
done
cd ../..