#!/bin/bash

# Update package lists
sudo apt update

# Install Redis server
sudo apt install redis-server

# Install Python dependencies from requirements.txt
pip install -r requirements.txt
