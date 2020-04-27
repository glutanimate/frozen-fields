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


def loadNote(self):
    if not self.note:
        return
    if not isinstance(self.parentWindow, AddCards):
        return
    iconstr_frozen = self.resourceToData(icon_path_frozen)
    iconstr_unfrozen = self.resourceToData(icon_path_unfrozen)
    flds = self.note.model()["flds"]
    sticky = [fld["sticky"] for fld in flds]

    self.web.eval(f"""var hotkey_toggle_field = "{hotkey_toggle_field}";""")
    self.web.eval(f"""var src_unfrozen = "{iconstr_unfrozen}";""")
    self.web.eval(f"""var src_frozen = "{iconstr_frozen}";""")
    self.web.eval(f"setFrozenFields({json.dumps(sticky)});")


def onBridge(handled, str, editor):
    """Extends the js<->py bridge with our pycmd handler"""

    if not isinstance(editor, Editor) or not isinstance(editor.parentWindow, AddCards):
        return handled
    if not str.startswith("frozen"):
        if str.startswith("blur"):
            editor.lastField = editor.currentField  # save old focus
        return handled
    if not editor.note or not runHook:
        # shutdown
        return handled

    (cmd, txt) = str.split(":", 1)
    cur = int(txt)
    flds = editor.note.model()['flds']
    flds[cur]['sticky'] = not flds[cur]['sticky']
    return (True, None)


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

gui_hooks.editor_did_init_shortcuts.append(onSetupShortcuts)
gui_hooks.webview_did_receive_js_message.append(onBridge)
gui_hooks.editor_did_load_note.append(loadNote)
Editor.onFrozenToggle = onFrozenToggle

Editor.frozenToggle = frozenToggle
