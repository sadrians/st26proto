function splitString(as) {
    return as.match(/.{1,10}/g);
}

function writeSplitString(aStr) {
    var li = splitString(aStr);
    var cntr = 0;
    var groupIndex = 0;
    var currentString = "";
    var i;
    var list_length = li.length;

    for (i = 0; i < list_length; i++)
    {
        cntr += li[i].length;
        groupIndex += 1;
        currentString += li[i] + " ";
        if (groupIndex == 6)
        {
            document.write(currentString + cntr + "<br />");
            currentString = "";
            groupIndex = 0;
        }

    }
    if (currentString !== "") {
        document.write(currentString + cntr + "<br />");
    }
}

function getSplitString(aStr) {
    var res = "";
    var li = splitString(aStr);
    var cntr = 0;
    var groupIndex = 0;
    var currentString = "";
    var i;
    var list_length = li.length;

    for (i = 0; i < list_length; i++)
    {
        cntr += li[i].length;
        groupIndex += 1;
        currentString += li[i] + " ";
        if (groupIndex == 6)
        {
            res = res + currentString + cntr + "<br />";
            currentString = "";
            groupIndex = 0;
        }

    }
    if (currentString !== "") {
        res = res + currentString + cntr + "<br />";
    }

    return res;
}