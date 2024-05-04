#!/bin/bash

# Update package lists
apt update

# Install Redis server
apt install redis-server

# Install Python dependencies from requirements.txt
pip install -r requirements.txt

#run redis
redis-server --version
redis-server
redis-cli

