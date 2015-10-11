# Frozen Fields add-on for Anki
# 
# Original author: tmbb (https://github.com/tmbb)
# This version by: Glutanimate (https://github.com/Glutanimate)
#
# Modifications:
#  - added hotkeys for various actions

# Snowflake Icon
icon_name = "flake"
min_width = "28"

## Uncomment to use the Kubuntu icon instead of the snowflake icon
#icon_name = "frozen_26x28"
#min_width = "28"

from aqt import mw, editor
from aqt.qt import *
from anki.hooks import wrap, addHook
from anki.utils import json
import os

def addons_folder(): return mw.pm.addonFolder()

def icon_color(icon, ext="png"):
    return "'" + os.path.join(addons_folder(),
                              "frozen_fields_addon",
                              "icons",
                              (icon + "_color." + ext)).replace("\\","/") + "'"

def icon_grayscale(icon, ext="png"):
    return "'" + os.path.join(addons_folder(),
                              "frozen_fields_addon",
                              "icons",
                              (icon + "_grayscale." + ext)).replace("\\","/") + "'"


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
        txt += "<tr><td style='min-width:""" + min_width + """'></td><td class=fname>{0}</td></tr><tr>".format(n);
        if (frozen[i]) {
            txt += "<td style='min-width:""" + min_width + """'><div id=i{0} onclick='onFrozen(this);'><img src=""" + icon_color(icon_name) + """/></div></td>".format(i);
        }
        else {
            txt += "<td style='min-width:"""  + min_width + """'><div id=i{0} onclick='onFrozen(this);'><img src=""" + icon_grayscale(icon_name) + """/></div></td>".format(i);
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
"""

def myLoadNote(self):
    self.web.eval(js_code)
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
    ###########################################################
    sticky = []
    model = self.note.model()
    for fld in model['flds']:
        sticky.append(fld['sticky'])
    ###########################################################
    self.web.eval("setFrozenFields(%s, %s, %d);" % (
        json.dumps(data), json.dumps(sticky), field))
    self.web.eval("setFonts(%s);" % (
        json.dumps(self.fonts())))
    self.checkValid()
    self.widget.show()
    if self.stealFocus:
        self.web.setFocus()

def myBridge(self, str):
    if str.startswith("frozen"):
        (cmd, txt) = str.split(":", 1)
        field_nr = int(txt)
        model = self.note.model()
        is_sticky = model['flds'][field_nr]['sticky']
        model['flds'][field_nr]['sticky'] = not is_sticky
        self.loadNote()

def resetFrozen(editor):
    myField = editor.currentField
    flds = editor.note.model()['flds']
    for n in range(len(editor.note.fields)):
        try:
            if  flds[n]['sticky']:
                flds[n]['sticky'] = not flds[n]['sticky']
        except IndexError:
            break
    editor.loadNote()
    editor.web.eval("focusField(%d);" % myField)

def toggleFrozen(editor):
    # myField = editor.currentField
    # flds = editor.note.model()['flds']
    # flds[myField]['sticky'] = not flds[myField]['sticky']
    myField = editor.currentField
    editor.web.eval("""py.run("frozen:%d");""" % myField)
    editor.loadNote()
    editor.web.eval("focusField(%d);" % myField)

def onSetupButtons(editor):
    # insert custom key sequences here:
    # e.g. QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_F) for Alt+Shift+F
    s = QShortcut(QKeySequence(Qt.Key_F9), editor.parentWindow)
    s.connect(s, SIGNAL("activated()"),
              lambda : toggleFrozen(editor))
    t = QShortcut(QKeySequence(Qt.SHIFT + Qt.Key_F9), editor.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda : resetFrozen(editor))

addHook("setupEditorButtons", onSetupButtons)
editor.Editor.loadNote = myLoadNote
editor.Editor.bridge = wrap(editor.Editor.bridge, myBridge, 'before')
