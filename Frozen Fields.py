# -*- coding: utf-8 -*-

"""
Frozen Fields Add-on for Anki

Allows you to conveniently sticky and unsticky a field right
from the note editor. Sticky fields are preserved when 
switching to a new note.

Copyright: (c) 2012-2015 Tiago Barroso (https://github.com/tmbb)
           (c) 2015-2017 Glutanimate (https://github.com/Glutanimate)

License: GNU AGPL, version 3 or later; https://www.gnu.org/licenses/agpl-3.0.en.html
"""

##### USER CONFIGURATION START ######

hotkey_toggle_field = "F9" # Toggle status for current field
hotkey_toggle_all = "Shift+F9" # Toggle status for all fields

##### USER CONFIGURATION END ######


import os

from aqt.qt import *

from aqt import mw
from aqt.editor import Editor
from aqt.addcards import AddCards

from anki.hooks import wrap, addHook
from anki.utils import json

icon_path = os.path.join(mw.pm.addonFolder(), "frozen_fields")
icon_frozen = QUrl.fromLocalFile(os.path.join(icon_path, "frozen.png")).toString()
icon_unfrozen = QUrl.fromLocalFile(os.path.join(icon_path, "unfrozen.png")).toString()

js_code = """
function onFrozen(elem) {
    currentField = elem;
    py.run("frozen:" + currentField.id.substring(1));
}

function setFrozenFields(fields, frozen, focusTo) {
    var txt = "";
    for (var i=0; i<fields.length; i++) {
        var n = fields[i][0];
        var f = fields[i][1];
        if (!f) {
            f = "<br>";
        }
        txt += "<tr><td style='min-width: 28'></td><td class=fname>{0}</td></tr><tr>".format(n);
        if (frozen[i]) {
            txt += "<td style='min-width: 28'><div id=i{0} title='Unfreeze field (%s)' onclick='onFrozen(this);'><img src='%s'/></div></td>".format(i);
        }
        else {
            txt += "<td style='min-width: 28'><div id=i{0} title='Freeze field (%s)' onclick='onFrozen(this);'><img src='%s'/></div></td>".format(i);
        }
        txt += "<td width=100%%>"
        txt += "<div id=f{0} onkeydown='onKey();' onmouseup='onKey();'".format(i);
        txt += " onfocus='onFocus(this);' onblur='onBlur();' class=field ";
        txt += "ondragover='onDragOver(this);' ";
        txt += "contentEditable=true class=field>{0}</div>".format(f);
        txt += "</td>"
        txt += "</td></tr>";
    }
    $("#fields").html("<table cellpadding=0 width=100%%>"+txt+"</table>");
    if (!focusTo) {
        focusTo = 0;
    }
    if (focusTo >= 0) {
        $("#f"+focusTo).focus();
    }
};
""" % (hotkey_toggle_field, icon_frozen, hotkey_toggle_field, icon_unfrozen)

def myLoadNote(self):
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
    if isinstance(self.parentWindow, AddCards): # only modify AddCards Editor
        flds = self.note.model()["flds"]
        sticky = [fld["sticky"] for fld in flds]
        self.web.eval(js_code)
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
        self.stealFocus = False

def myBridge(self, str):
    """Extends the js<->py bridge with our py.link command"""
    if str.startswith("frozen"):
        (cmd, txt) = str.split(":", 1)
        cur = int(txt)
        flds = self.note.model()['flds']
        flds[cur]['sticky'] = not flds[cur]['sticky']
        self.loadNote()

def frozenToggleAll(self):
    """Toggle state of all fields"""
    cur = self.currentField
    flds = self.note.model()['flds']
    is_sticky = flds[cur]["sticky"]
    self.web.eval("saveField('key');")
    for n in range(len(self.note.fields)):
        try:
            flds[n]['sticky'] = not is_sticky
        except IndexError:
            break
    self.loadNote()
    self.web.eval("focusField(%d);" % cur)

def frozenToggle(self):
    """Toggle state of current field"""
    cur = self.currentField
    flds = self.note.model()['flds']
    flds[cur]["sticky"] = not flds[cur]["sticky"]
    self.web.eval("saveField('key');")
    self.loadNote()
    self.web.eval("focusField(%d);" % cur)

def onSetupButtons(self):
    """Set up hotkeys"""
    s = QShortcut(QKeySequence(hotkey_toggle_field), self.parentWindow,
        activated=self.frozenToggle)
    s = QShortcut(QKeySequence(hotkey_toggle_all), self.parentWindow,
        activated=self.frozenToggleAll)

# Add-on hooks, etc.

Editor.frozenToggle = frozenToggle
Editor.frozenToggleAll = frozenToggleAll
addHook("setupEditorButtons", onSetupButtons)
Editor.loadNote = myLoadNote
Editor.bridge = wrap(Editor.bridge, myBridge, 'before')
