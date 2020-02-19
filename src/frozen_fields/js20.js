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
        txt += "<div id=f{0} onkeydown='onKey(window.event);' onmouseup='onKey(window.event);'".format(i);
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
