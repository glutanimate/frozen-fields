# -*- coding: utf-8 -*-

# Frozen Fields Add-on for Anki
#
# Copyright (C) 2015-2020  Ankitects Pty Ltd and contributors
# Copyright (C) 2012-2015  Tiago Barroso <https://github.com/tmbb>
# Copyright (C) 2015-2020  Aristotelis P. <https://glutanimate.com/>
#                          and contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

import os

from anki.hooks import addHook, runHook, wrap
from anki.utils import json
from aqt import gui_hooks
from aqt.addcards import AddCards
from aqt.editor import Editor
from aqt.qt import *

from .config import local_conf
from .consts import *

icon_path = os.path.join(addon_path, "icons")

icon_path_frozen = os.path.join(icon_path, "frozen.png")
icon_path_unfrozen = os.path.join(icon_path, "unfrozen.png")

icon_frozen = QUrl.fromLocalFile(icon_path_frozen).toString()
icon_unfrozen = QUrl.fromLocalFile(icon_path_unfrozen).toString()

hotkey_toggle_field = local_conf["hotkeyOne"]
hotkey_toggle_all = local_conf["hotkeyAll"]

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "js21.js"), "r") as f:
    js_code_21 = f.read()


def loadNote(self, focusTo=None):
    if not self.note:
        return

    data = []
    for fld, val in list(self.note.items()):
        data.append((fld, self.mw.col.media.escapeImages(val)))
    self.widget.show()
    self.updateTags()

    def oncallback(arg):
        if not self.note:
            return
        self.setupForegroundButton()
        self.checkValid()
        if focusTo is not None:
            self.web.setFocus()
        gui_hooks.editor_did_load_note(self)

    # only modify AddCards Editor
    if not isinstance(self.parentWindow, AddCards):
        self.web.evalWithCallback("setFields(%s); setFonts(%s); focusField(%s); setNoteId(%s)" % (
            json.dumps(data),
            json.dumps(self.fonts()), json.dumps(focusTo),
            json.dumps(self.note.id)),
            oncallback)
    else:
        iconstr_frozen = self.resourceToData(icon_path_frozen)
        iconstr_unfrozen = self.resourceToData(icon_path_unfrozen)

        flds = self.note.model()["flds"]
        sticky = [fld["sticky"] for fld in flds]

        eval_definitions = js_code_21 % (hotkey_toggle_field, iconstr_frozen,
                                         iconstr_unfrozen)

        eval_calls = "setFrozenFields(%s, %s); setFonts(%s); focusField(%s); setNoteId(%s)" % (
            json.dumps(data), json.dumps(sticky),
            json.dumps(self.fonts()),
            json.dumps(focusTo),
            json.dumps(self.note.id))

        self.web.eval(eval_definitions)
        self.web.evalWithCallback(eval_calls, oncallback)


def onBridge(self, str, _old):
    """Extends the js<->py bridge with our pycmd handler"""

    if not str.startswith("frozen"):
        if str.startswith("blur"):
            self.lastField = self.currentField  # save old focus
        return _old(self, str)
    if not self.note or not runHook:
        # shutdown
        return

    (cmd, txt) = str.split(":", 1)
    cur = int(txt)
    flds = self.note.model()['flds']
    flds[cur]['sticky'] = not flds[cur]['sticky']


def frozenToggle(self, batch=False):
    """Toggle state of current field"""

    flds = self.note.model()['flds']
    cur = self.currentField
    if cur is None:
        cur = 0
    is_sticky = flds[cur]["sticky"]
    if not batch:
        flds[cur]["sticky"] = not is_sticky
    else:
        for n in range(len(self.note.fields)):
            try:
                flds[n]['sticky'] = not is_sticky
            except IndexError:
                break

    self.loadNoteKeepingFocus()


def onFrozenToggle(self, batch=False):
    self.web.evalWithCallback(
        "saveField('key');", lambda _: self.frozenToggle(batch=batch))


def onSetupShortcuts(cuts, self):
    cuts += [(hotkey_toggle_field, self.onFrozenToggle),
             (hotkey_toggle_all, lambda: self.onFrozenToggle(batch=True), True)]
    # third value: enable shortcut even when no field selected

# Add-on hooks, etc.


def initializeEditor():
    addHook("setupEditorShortcuts", onSetupShortcuts)
    Editor.onBridgeCmd = wrap(Editor.onBridgeCmd, onBridge, "around")
    Editor.loadNote = loadNote
    Editor.onFrozenToggle = onFrozenToggle

    Editor.frozenToggle = frozenToggle
