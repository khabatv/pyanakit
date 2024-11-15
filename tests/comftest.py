# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 10:50:45 2024

@author: past
"""
#ausführen vor tests, damit test den src ordner mit den einzlenen Modulen findet

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
