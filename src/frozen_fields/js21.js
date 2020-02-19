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
        // ----------- mod start -----------
        txt += "<tr><td style='width:28px'></td><td class=fname>{0}</td></tr><tr>".format(n);

        if (frozen[i]) {
            txt += "<td style='width:28px'><div id=i{0} title='Unfreeze field (%s)' onclick='onFrozen(this);'><img src='%s'/></div></td>".format(i);
        }
        else {
            txt += "<td style='width:28px'><div id=i{0} title='Freeze field (%s)' onclick='onFrozen(this);'><img src='%s'/></div></td>".format(i);
        }

        txt += "<td width=100%%>"
        // -----------  mod end -----------
        
        txt += "<div id=f{0} onkeydown='onKey(window.event);' oninput='onInput()' onmouseup='onKey(window.event);'".format(i);
        txt += " onfocus='onFocus(this);' onblur='onBlur();' class='field clearfix' ";
        txt += "ondragover='onDragOver(this);' onpaste='onPaste(this);' ";
        txt += "oncopy='onCutOrCopy(this);' oncut='onCutOrCopy(this);' ";
        txt += "contentEditable=true class=field>{0}</div>".format(f);

        // ----------- mod start -----------
        txt += "</td>"
        // -----------  mod end -----------

        txt += "</td></tr>";
    }
    $("#fields").html("<table cellpadding=0 width=100%% style='table-layout: fixed;'>" + txt + "</table>");
    maybeDisableButtons();
}

