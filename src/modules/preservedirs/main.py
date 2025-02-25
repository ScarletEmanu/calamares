#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <https://calamares.io> ===
#
#   SPDX-FileCopyrightText: 2014 Teo Mrnjavac <teo@kde.org>
#   SPDX-FileCopyrightText: 2017 Alf Gaida <agaida@siduction.org>
#   SPDX-FileCopyrightText: 2017 Adriaan de Groot <groot@kde.org>
#   SPDX-License-Identifier: GPL-3.0-or-later
#
#   Calamares is Free Software: see the License-Identifier above.
#

"""
=== Example Python jobmodule.

A Python jobmodule is a Python program which imports libcalamares and
has a function run() as entry point. run() must return None if everything
went well, or a tuple (str,str) with an error message and description
if something went wrong.
"""

import libcalamares
import os
import subprocess
from time import gmtime, strftime, sleep

import gettext
_ = gettext.translation("calamares-python",
                        localedir=libcalamares.utils.gettext_path(),
                        languages=libcalamares.utils.gettext_languages(),
                        fallback=True).gettext


def pretty_name():
    return _("Copying dirs job.")

status = _("Saving files for later…")

def pretty_status_message():
    return status

def run():
    root_mount_point = libcalamares.globalstorage.value("rootMountPoint")
    if not root_mount_point:
        return ("bad", "Errore: rootMountPoint non trovato")
    
    dirs_to_copy = libcalamares.job.configuration.get("dirs", [])
    for dir in dirs:
        try:
            chown_dir = ":".join(dir["perm"].rsplit(":", 1)[:-1])
            src = dir["src"]

            if not os.path.exists(src):
                libcalamares.utils.warning(f"Il percorso '{src}' non esiste, ignorato.")
                continue

            cmd = ["rsync", src, "-av", f"--chown={chown_dir}", dir["dest"]]

            subprocess.run(cmd, check=True)
        except:
            continue