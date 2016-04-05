#! /usr/bin/env bash

data_dir="data/"
target_dir="20_newgroups"
target_tar=$target_dir".tar.gz"
data_url="http://www.cs.cmu.edu/afs/cs/project/theo-11/www/naive-bayes/20_newsgroups.tar.gz"

pip install -r requirements.txt

if [ ! -n $data_dir]
then
    mkdir -p $data_dir
fi

cd $data_dir
wget $data_url -O $target_tar
tar xf $target_tar
cd ..

chmod +x 20newsgroups.py
./20newsgroups.py $data_dir$target_dir
