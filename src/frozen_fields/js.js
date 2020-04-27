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
        var $td_name = $(`#name${i}`);
        if ($td_name.length == 0) {
            // no multi column. Get the i-th fname
            var td_name = $fnames[i];
            $td_name = $(td_name);
        }
        var src = (frozen[i])?src_frozen:src_unfrozen;
        var un_freeze = (frozen[i])?"Unfreeze":"Freeze";
        var div = `<img id=i${i} src='${src}' title='${un_freeze} field (${hotkey_toggle_field})' style="height:.9em" onclick='onFrozen(${i});'/>`;
        $td_name.prepend(div);
    }
}
