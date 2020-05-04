function onFrozen(idx) {
    wasFrozen = frozenFields[idx];
    pycmd("frozen:" + idx);
    wasFrozen = frozenFields[idx];
    frozenFields[idx] = !wasFrozen;
    $img = $(`#i${idx}`);
    if (wasFrozen) {
        $img.attr("src", src_unfrozen);
        $img.attr("title", "Freeze field ("+hotkey_toggle_field+")");
    } else {
        $img.attr("src", src_frozen);
        $img.attr("title", "Unfreeze field ("+hotkey_toggle_field+")");
    }
}

var frozenFields = null;

function setFrozenFields(frozen) {
    frozenFields = frozen;
    $fnames = $(".fname");
    for (var i=0; i<frozen.length; i++) {
        var $div_field = $(`#f${i}`);
        var src = (frozen[i])?src_frozen:src_unfrozen;
        var un_freeze = (frozen[i])?"Unfreeze":"Freeze";
        var img = `<img id=i${i} src='${src}' title='${un_freeze} field (${hotkey_toggle_field})' onclick='onFrozen(${i});'/>`
        var td_img = `<td style="width:28px" id="frozen${i}">${img}</td>`;
        $td_field = $div_field.parent();
        var colspan = $td_field.attr("colspan");
        if (colspan == undefined) {
            colspan = 1;
        }
        // Each field normally uses twice as much column than before
        // So we double the number of column for this field, and
        // remove one column that we reserve for the ice.
        $td_field.attr("colspan", colspan * 2 - 1);
        $td_field.before(td_img);

        var $td_name = $(`#name${i}`);
        var colspan = $td_name.attr("colspan");
        if (colspan == undefined) {
            colspan = 1;
        }
        $td_name.attr("colspan", colspan * 2 - 1);
        $td_name.before("<td style='width:28px'></td>");
    }
}
