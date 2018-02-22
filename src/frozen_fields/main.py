# -*- coding: utf-8 -*-

"""
This file is part of the Frozen Fields add-on for Anki.

Main Module, hooks add-on methods into Anki.

Copyright: (c) 2012-2015 Tiago Barroso <https://github.com/tmbb>
           (c) 2015-2018 Glutanimate <https://glutanimate.com/>

License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

##### USER CONFIGURATION START ######

hotkey_toggle_field = "F9"  # Toggle status for current field
hotkey_toggle_all = "Shift+F9"  # Toggle status for all fields

##### USER CONFIGURATION END ######


import os

from aqt.qt import *

from aqt.editor import Editor
from aqt.addcards import AddCards
from aqt.utils import tooltip

from anki.hooks import wrap, addHook, runHook
from anki.utils import json

from .consts import *

icon_path = os.path.join(addon_path, "icons")
icon_frozen = QUrl.fromLocalFile(
    os.path.join(icon_path, "frozen.png")).toString()
icon_unfrozen = QUrl.fromLocalFile(
    os.path.join(icon_path, "unfrozen.png")).toString()



js_code_20 = """
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


js_code_21 = """
function onFrozen(elem) {
    currentField = elem;
    pycmd("frozen:" + currentField.id.substring(1));
}

function setFrozenFields(fields, frozen) {
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
        txt += "<div id=f{0} onkeydown='onKey();' oninput='checkForEmptyField()' onmouseup='onKey();'".format(i);
        txt += " onfocus='onFocus(this);' onblur='onBlur();' class=field ";
        txt += "ondragover='onDragOver(this);' onpaste='onPaste(this);' ";
        txt += "oncopy='onCutOrCopy(this);' oncut='onCutOrCopy(this);' ";
        txt += "contentEditable=true class=field>{0}</div>".format(f);
        txt += "</td>"
        txt += "</td></tr>";
    }
    $("#fields").html("<table cellpadding=0 width=100%% style='table-layout: fixed;'>" + txt + "</table>");
    maybeDisableButtons();

setFrozenFields(%s, %s); setFonts(%s); focusField(%s)
};

"""


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
        runHook("loadNote", self)

    # only modify AddCards Editor
    if not isinstance(self.parentWindow, AddCards):
        print("Not Addcards instance")
        self.web.evalWithCallback("setFields(%s); setFonts(%s); focusField(%s)" % (
            json.dumps(data),
            json.dumps(self.fonts()), json.dumps(focusTo)),
                                  oncallback)
    else:
        flds = self.note.model()["flds"]
        sticky = [fld["sticky"] for fld in flds]
        evaljs = js_code_21 % (hotkey_toggle_field, icon_frozen,
                                                hotkey_toggle_field, icon_unfrozen,
                                                json.dumps(data), json.dumps(sticky),
                                                json.dumps(self.fonts()),
                                                json.dumps(focusTo))
        print(evaljs)
        self.web.evalWithCallback(evaljs,
                                  oncallback)


def myBridge(self, str, _old):
    """Extends the js<->py bridge with our py command"""
    if not str.startswith("frozen"):
        return _old(self, str)
    if not self.note or not runHook:
        # shutdown
        return
    
    (cmd, txt) = str.split(":", 1)
    cur = int(txt)
    flds = self.note.model()['flds']
    flds[cur]['sticky'] = not flds[cur]['sticky']
    
    if anki21:
        self.loadNoteKeepingFocus()
    else:
        self.loadNote()


def frozenToggle(self, batch=False):
    """Toggle state of current field"""
    tooltip("frozenToggle")
    cur = self.currentField
    flds = self.note.model()['flds']
    is_sticky = flds[cur]["sticky"]
    if not batch:
        flds[cur]["sticky"] = not is_sticky
        self.web.eval("saveField('key');")
    else:
        self.web.eval("saveField('key');")
        for n in range(len(self.note.fields)):
            try:
                flds[n]['sticky'] = not is_sticky
            except IndexError:
                break
    self.loadNote()
    self.web.eval("focusField(%d);" % cur)


def onSetupButtons20(self):
    """Set up hotkeys"""
    if not isinstance(self.parentWindow, AddCards):  # only modify AddCards Editor
        return

    QShortcut(QKeySequence(hotkey_toggle_field), self.parentWindow,
              activated=self.frozenToggle)
    QShortcut(QKeySequence(hotkey_toggle_all), self.parentWindow,
              activated=lambda: self.frozenToggle(batch=True))


def onSetupShortcuts21(cuts, self):
    cuts += [(hotkey_toggle_field, self.frozenToggle),
             (hotkey_toggle_all, lambda: self.frozenToggle(batch=True))]

# Add-on hooks, etc.

if anki21:
    addHook("setupEditorShortcuts", onSetupShortcuts21)
    Editor.onBridgeCmd = wrap(Editor.onBridgeCmd, myBridge, "around")
    Editor.loadNote = loadNote21
else:
    addHook("setupEditorButtons", onSetupButtons)
    Editor.bridge = wrap(Editor.bridge, myBridge, 'around')
    Editor.loadNote = myLoadNote

Editor.frozenToggle = frozenToggle

