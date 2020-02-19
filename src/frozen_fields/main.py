# -*- coding: utf-8 -*-

"""
This file is part of the Frozen Fields add-on for Anki.

Main Module, hooks add-on methods into Anki.

Copyright: (c) 2012-2015 Tiago Barroso <https://github.com/tmbb>
           (c) 2015-2018 Glutanimate <https://glutanimate.com/>

License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""


import os

from anki.hooks import addHook, runHook, wrap
from anki.utils import json
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
with open(os.path.join(__location__, "js20.js"), "r") as f:
          js_code_20 = f.read() % (hotkey_toggle_field, icon_frozen, hotkey_toggle_field, icon_unfrozen)
with open(os.path.join(__location__, "js21.js"), "r") as f:
          js_code_21 = f.read()


def loadNote20(self):
    """Modified loadNote(), adds buttons to Editor"""
    if not self.note:
        return
    if self.stealFocus:
        field = self.currentField
    else:
        field = -1
    if not self._loaded:
        # will be loaded when page is ready
        return
    data = []
    for fld, val in self.note.items():
        data.append((fld, self.mw.col.media.escapeImages(val)))
    ###### ↓modified #########
    if isinstance(self.parentWindow, AddCards):  # only modify AddCards Editor
        flds = self.note.model()["flds"]
        sticky = [fld["sticky"] for fld in flds]
        self.web.eval(js_code_20)
        self.web.eval("setFrozenFields(%s, %s, %d);" % (
            json.dumps(data), json.dumps(sticky), field))
    else:
        self.web.eval("setFields(%s, %d);" % (
            json.dumps(data), field))
    ###########################
    self.web.eval("setFonts(%s);" % (
        json.dumps(self.fonts())))
    self.checkValid()
    self.widget.show()
    if self.stealFocus:
        self.web.setFocus()
        # self.stealFocus = False


def loadNote21(self, focusTo=None):
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
        try:
            from aqt import gui_hooks
            gui_hooks.editor_did_load_note(self)
        except:
            runHook("loadNote", self)

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
        if anki21 and str.startswith("blur"):
            self.lastField = self.currentField  # save old focus
        return _old(self, str)
    if not self.note or not runHook:
        # shutdown
        return

    (cmd, txt) = str.split(":", 1)
    cur = int(txt)
    flds = self.note.model()['flds']
    flds[cur]['sticky'] = not flds[cur]['sticky']

    if not anki21:
        self.loadNote()


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

    if anki21:
        self.loadNoteKeepingFocus()
    else:
        self.web.eval("saveField('key');")
        self.loadNote()


def onFrozenToggle21(self, batch=False):
    self.web.evalWithCallback(
        "saveField('key');", lambda _: self.frozenToggle(batch=batch))


def onSetupButtons20(self):
    """Set up hotkeys"""
    if not isinstance(self.parentWindow, AddCards):  # only modify AddCards Editor
        return

    QShortcut(QKeySequence(hotkey_toggle_field), self.parentWindow,
              activated=self.frozenToggle)
    QShortcut(QKeySequence(hotkey_toggle_all), self.parentWindow,
              activated=lambda: self.frozenToggle(batch=True))


def onSetupShortcuts21(cuts, self):
    cuts += [(hotkey_toggle_field, self.onFrozenToggle),
             (hotkey_toggle_all, lambda: self.onFrozenToggle(batch=True), True)]
    # third value: enable shortcut even when no field selected

# Add-on hooks, etc.


if anki21:
    addHook("setupEditorShortcuts", onSetupShortcuts21)
    Editor.onBridgeCmd = wrap(Editor.onBridgeCmd, onBridge, "around")
    Editor.loadNote = loadNote21
    Editor.onFrozenToggle = onFrozenToggle21
else:
    addHook("setupEditorButtons", onSetupButtons20)
    Editor.bridge = wrap(Editor.bridge, onBridge, 'around')
    Editor.loadNote = loadNote20

Editor.frozenToggle = frozenToggle
