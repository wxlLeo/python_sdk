# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

"""
https://docs.djangoproject.com/en/1.8/topics/settings/
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os

from .base import *


local_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local.py')
if os.path.exists(local_py):
    execfile(local_py)
