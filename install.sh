#!/bin/bash

# Conda install env
conda env create -f env.yml

# Source profile
source $HOME/.bash_profile

# Activate the env
conda activate yt_env

# Install PDF gen module suite
pip install fpdf

