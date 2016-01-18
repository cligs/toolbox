#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: activate_toolbox.py
# Author: Christof Schöch

"""
# Script to add the "toolbox" module to your syspath. 
# Run once with appropriate path to use the toolbox with "import".
"""

import sys
import os

## Enter the path to the folder in which your toolbox folder is located.
sys.path.append(os.path.abspath("//"))

## This is for checking whether the path was added correctly.
print(sys.path)

## Optional: Activate to remove a (mistaken or redundant path)    
#sys.path.remove(os.path.abspath("//"))