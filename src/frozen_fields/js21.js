function onFrozen(elem, idx) {
    wasFrozen = frozenFields[idx];
    pycmd("frozen:" + idx);
    wasFrozen = frozenFields[idx];
    frozenFields[idx] = !wasFrozen;
    $div = $(elem);
    $img = $div.find("img");
    if (wasFrozen) {
        elem.title = "Freeze field ("+hotkey_toggle_field+")";
        $img.attr("src", src_unfrozen);
    } else {
        elem.title = "Unfreeze field ("+hotkey_toggle_field+")";
        $img.attr("src", src_frozen);
    }
}

var hotkey_toggle_field = "%s";
var src_frozen = "%s";
var src_unfrozen = "%s";

var frozenFields = null;

function setFrozenFields(fields, frozen) {
    frozenFields = frozen;
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
            txt += "<td style='width:28px'><div id=i"+i+" title='Unfreeze field ("+hotkey_toggle_field+")' onclick='onFrozen(this, "+i+");'><img src='"+src_frozen+"'/></div></td>";
        }
        else {
            txt += "<td style='width:28px'><div id=i"+i+" title='Freeze field ("+hotkey_toggle_field+")' onclick='onFrozen(this, "+i+");'><img src='"+src_unfrozen+"'/></div></td>";
        }

        txt += "<td width=100%%>"
        // -----------  mod end -----------
        
        txt += "<div id=f"+i+" onkeydown='onKey(window.event);' oninput='onInput()' onmouseup='onKey(window.event);'";
        txt += " onfocus='onFocus(this);' onblur='onBlur();' class='field clearfix' ";
        txt += "ondragover='onDragOver(this);' onpaste='onPaste(this);' ";
        txt += "oncopy='onCutOrCopy(this);' oncut='onCutOrCopy(this);' ";
        txt += "contentEditable=true class=field>"+f+"</div>";

        // -----------  mod end -----------

        txt += "</td></tr>";
    }
    $("#fields").html("<table cellpadding=0 width=100%% style='table-layout: fixed;'>" + txt + "</table>");
    maybeDisableButtons();
}

