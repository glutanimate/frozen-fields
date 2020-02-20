# -*- coding: utf-8 -*-

"""
This file is part of the Frozen Fields add-on for Anki.

Configuration shim between Anki 2.0 and Anki 2.1

Copyright: (c) 2018 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import os

from aqt import mw

from .consts import *

defaults_path = os.path.join(addon_path, "config.json")
meta_path = os.path.join(addon_path, "meta.json")

def getConfig():
    return mw.addonManager.getConfig(__name__)

def writeConfig(config):
    mw.addonManager.writeConfig(__name__, config)

local_conf = getConfig()
