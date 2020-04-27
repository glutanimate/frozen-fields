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
from aqt import gui_hooks, mw
from aqt.addcards import AddCards
from aqt.editor import Editor
from aqt.qt import *
from aqt.webview import WebContent

from .config import local_conf
from .consts import *

icon_path = os.path.join(addon_path, "icons")
addon_package = mw.addonManager.addonFromModule(__name__)

icon_path_frozen = os.path.join(icon_path, "frozen.png")
icon_path_unfrozen = os.path.join(icon_path, "unfrozen.png")

icon_frozen = QUrl.fromLocalFile(icon_path_frozen).toString()
icon_unfrozen = QUrl.fromLocalFile(icon_path_unfrozen).toString()

hotkey_toggle_field = local_conf["hotkeyOne"]
hotkey_toggle_all = local_conf["hotkeyAll"]

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


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
        self.web.eval(
            f"""var hotkey_toggle_field = "{hotkey_toggle_field}";""")
        self.web.eval(f"""var src_unfrozen = "{iconstr_unfrozen}";""")
        self.web.eval(f"""var src_frozen = "{iconstr_frozen}";""")

        flds = self.note.model()["flds"]
        sticky = [fld["sticky"] for fld in flds]

        eval_calls = "setFrozenFields(%s, %s); setFonts(%s); focusField(%s); setNoteId(%s)" % (
            json.dumps(data), json.dumps(sticky),
            json.dumps(self.fonts()),
            json.dumps(focusTo),
            json.dumps(self.note.id))

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
mw.addonManager.setWebExports(__name__, r".*(css|js)")
def on_webview_will_set_content(web_content: WebContent, context):
    if not isinstance(context, Editor) or not isinstance(context.parentWindow, AddCards):
        return
    web_content.js.append(
        f"/_addons/{addon_package}/js.js")

gui_hooks.webview_will_set_content.append(on_webview_will_set_content)

addHook("setupEditorShortcuts", onSetupShortcuts)
Editor.onBridgeCmd = wrap(Editor.onBridgeCmd, onBridge, "around")
Editor.loadNote = loadNote
Editor.onFrozenToggle = onFrozenToggle

Editor.frozenToggle = frozenToggle
