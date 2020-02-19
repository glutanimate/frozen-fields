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
        txt += "<tr><td style='width:28px'></td><td class=fname>"+n+"</td></tr><tr>";

        if (frozen[i]) {
            txt += "<td style='width:28px'><div id=i"+i+" title='Unfreeze field (%s)' onclick='onFrozen(this);'><img src='%s'/></div></td>";
        }
        else {
            txt += "<td style='width:28px'><div id=i"+i+" title='Freeze field (%s)' onclick='onFrozen(this);'><img src='%s'/></div></td>";
        }

        txt += "<td width=100%%>"
        // -----------  mod end -----------
        
        txt += "<div id=f"+i+" onkeydown='onKey(window.event);' oninput='onInput()' onmouseup='onKey(window.event);'";
        txt += " onfocus='onFocus(this);' onblur='onBlur();' class='field clearfix' ";
        txt += "ondragover='onDragOver(this);' onpaste='onPaste(this);' ";
        txt += "oncopy='onCutOrCopy(this);' oncut='onCutOrCopy(this);' ";
        txt += "contentEditable=true class=field>"+f+"</div>";

        // ----------- mod start -----------
        txt += "</td>"
        // -----------  mod end -----------

        txt += "</td></tr>";
    }
    $("#fields").html("<table cellpadding=0 width=100%% style='table-layout: fixed;'>" + txt + "</table>");
    maybeDisableButtons();
}

