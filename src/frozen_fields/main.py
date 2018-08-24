# -*- coding: utf-8 -*-

"""
This file is part of the Frozen Fields add-on for Anki.

Main Module, hooks add-on methods into Anki.

Copyright: (c) 2012-2015 Tiago Barroso <https://github.com/tmbb>
           (c) 2015-2018 Glutanimate <https://glutanimate.com/>

License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""


import os

from aqt.qt import *

from aqt.editor import Editor
from aqt.addcards import AddCards

from anki.hooks import wrap, addHook, runHook
from anki.utils import json

from .consts import *
from .config import local_conf

icon_path = os.path.join(addon_path, "icons")

icon_path_frozen = os.path.join(icon_path, "frozen.png")
icon_path_unfrozen = os.path.join(icon_path, "unfrozen.png")

icon_frozen = QUrl.fromLocalFile(icon_path_frozen).toString()
icon_unfrozen = QUrl.fromLocalFile(icon_path_unfrozen).toString()

hotkey_toggle_field = local_conf["hotkeyOne"]
hotkey_toggle_all = local_conf["hotkeyAll"]


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

function addFreezeButtons(frozen, nfld) {
    let hotkey = '%s';
    let icon_frozen = '%s';
    let icon_unfrozen = '%s';
    let template = document.createElement("template");

    // dummy elements to preserve table layout
    document.querySelectorAll("td.fname").forEach((td) => {
        template.innerHTML = "<td style='width:28px'></td>";
        td.parentElement.insertBefore(template.content.firstChild, td);
    });

    let fstr = `<td style='width:28px'><div id=i{0} title='{1} field (${hotkey})' onclick='onFrozen(this);'><img src='{2}'/></div></td>`;
    for (let i=0; i<nfld; i++) {
        let field = document.querySelector(`#f${i}.field`);
        let flake_html;
        if (frozen[i]) {
            flake_html = fstr.format(i, "Unfreeze", icon_frozen);
        }
        else {
            flake_html = fstr.format(i, "Freeze", icon_unfrozen);
        }

        let td = field.parentElement;
        template.innerHTML = flake_html;
        td.parentElement.insertBefore(template.content.firstChild, td);
    }
}
"""


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
    # only modify AddCards Editor
    if not isinstance(self.parentWindow, AddCards):
        return

    iconstr_frozen = self.resourceToData(icon_path_frozen)
    iconstr_unfrozen = self.resourceToData(icon_path_unfrozen)

    flds = self.note.model()["flds"]
    sticky = [fld["sticky"] for fld in flds]

    eval_definitions = js_code_21 % (hotkey_toggle_field, iconstr_frozen, iconstr_unfrozen)
    self.web.eval(eval_definitions)

    def oncallback(arg):
        if focusTo is not None:
            self.web.setFocus()

    self.web.evalWithCallback("addFreezeButtons(%s, %s)" % (json.dumps(sticky), len(flds)), oncallback)


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

    if anki21:
        # load and restore old focus
        self.loadNote(focusTo=getattr(self, "lastField", None))
    else:
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
    self.web.evalWithCallback("saveField('key');", lambda _: self.frozenToggle(batch=batch))


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
    addHook("loadNote", loadNote21)
    Editor.onFrozenToggle = onFrozenToggle21
else:
    addHook("setupEditorButtons", onSetupButtons20)
    Editor.bridge = wrap(Editor.bridge, onBridge, 'around')
    Editor.loadNote = loadNote20

Editor.frozenToggle = frozenToggle
