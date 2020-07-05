/*
�2010 - 2016 SAP SE or an SAP affiliate company.  All rights reserved.

SAP and other SAP products and services mentioned herein as well as their respective logos are trademarks or registered trademarks of SAP SE in Germany and other countries.  Please see http://www.sap.com/corporate-en/legal/copyright/index.epx#trademark for additional trademark information and notices.
*/

if ("undefined" == typeof businessobjects) {
    var businessobjects = {};
}
businessobjects.opendocument = businessobjects.opendocument || {};
businessobjects.opendocument.findCallback = function (functionName) {
    return businessobjects.opendocument.findCallbackHelper({sourceWindow: window, functionName: functionName});
};
businessobjects.opendocument.findCallbackHelper = function (args) {
    var sourceWindow = args.sourceWindow;
    var functionName = args.functionName;
    if (!sourceWindow || !functionName) {
        return null;
    }
    if (sourceWindow[functionName]) {
        return sourceWindow[functionName];
    } else {
        var callback;
        if (sourceWindow.opener && sourceWindow != sourceWindow.opener) {
            try {
                callback = businessobjects.opendocument.findCallbackHelper({
                    sourceWindow: sourceWindow.opener,
                    functionName: functionName
                });
            } catch (e) {
                callback = null;
            }
            if (callback) {
                return callback;
            }
        }
        if (sourceWindow.parent && sourceWindow != sourceWindow.parent) {
            try {
                callback = businessobjects.opendocument.findCallbackHelper({
                    sourceWindow: sourceWindow.parent,
                    functionName: functionName
                });
            } catch (e) {
                callback = null;
            }
            if (callback) {
                return callback;
            }
        }
    }
    return null;
};
businessobjects.opendocument.uriEncode = function (s) {
    if ((typeof (encodeURIComponent)).toLowerCase() == "function") {
        return encodeURIComponent(s);
    }
    var tmp = escape(s);
    return tmp.replace(/\+/g, "%2b");
};
if (Array.prototype.containsValue == undefined) {
    Array.prototype.containsValue = function (val) {
        for (var i = 0; i < this.length; i++) {
            if (this[i] === val) {
                return true;
            }
        }
        return false;
    };
}
businessobjects.opendocument.sendURLViaPOST = function (url, target) {
    var actionUrl = url.substring(0, url.lastIndexOf("?"));
    var formPost = document.createElement("form");
    formPost.setAttribute("method", "post");
    formPost.setAttribute("action", actionUrl);
    var subParams = url.substring(url.lastIndexOf("?") + 1);
    var params = subParams.split("&");
    for (var i = 0; i < params.length; i++) {
        var urlParamName = params[i].substring(0, params[i].lastIndexOf("="));
        var urlParamValue = params[i].substring(params[i].lastIndexOf("=") + 1);
        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        if (urlParamName != null) {
            urlParamName = decodeURIComponent(urlParamName.replace(/\+/g, "%20"));
        }
        hiddenField.setAttribute("name", urlParamName);
        if (urlParamValue != null) {
            urlParamValue = decodeURIComponent(urlParamValue.replace(/\+/g, "%20"));
        }
        hiddenField.setAttribute("value", urlParamValue);
        formPost.appendChild(hiddenField);
    }
    document.body.appendChild(formPost);
    if (target != undefined && target != null) {
        formPost.target = target;
    }
    formPost.submit();
    document.body.removeChild(formPost);
};

/*
�2010 - 2016 SAP SE or an SAP affiliate company.  All rights reserved.

SAP and other SAP products and services mentioned herein as well as their respective logos are trademarks or registered trademarks of SAP SE in Germany and other countries.  Please see http://www.sap.com/corporate-en/legal/copyright/index.epx#trademark for additional trademark information and notices.
*/

if ("undefined" == typeof businessobjects) {
    var businessobjects = {};
}
businessobjects.webutil = businessobjects.webutil || {};
businessobjects.webutil.caf = businessobjects.webutil.caf || {};

function modifyRelativeUrl(url, path) {
    return businessobjects.webutil.caf.modifyRelativeUrl({url: url, path: path});
}

businessobjects.webutil.caf.modifyRelativeUrl = function (args) {
    var url = args.url;
    var relUrl = url;
    var force = args.force === true;
    var modify = force;
    if (!force) {
        var userAgent = window.navigator.userAgent;
        if (userAgent.indexOf("MSIE") > -1) {
            var ind = userAgent.indexOf("Trident/");
            if (ind == -1 || userAgent.charAt(ind + 8) < "5") {
                modify = true;
            }
        }
        if (userAgent.indexOf("Edge") > -1 || userAgent.indexOf("edge") > -1) {
            modify = true;
        }
    }
    if (modify) {
        var startLoc = url.lastIndexOf("../");
        if (startLoc >= 0) {
            relUrl = args.path + url.substring(startLoc + 2);
        }
    }
    return relUrl;
};
businessobjects.webutil.caf.defaultRefreshAction = function (args) {
    getUniversalRepositoryExplorer(args.ureId).doAction("refresh", 0);
};
businessobjects.webutil.caf.ieFixWindowProps = function (args) {
    var windowProps = args.windowProps;
    if (null == windowProps) {
        windowProps = "";
    }
    if (windowProps.indexOf("fullscreen") > -1) {
        var newFullScreenString = "left=0,top=0,width=" + (screen.width - 10) + ",height=" + (screen.height - 70);
        var fullIndex = windowProps.indexOf("fullscreen");
        if (windowProps.indexOf(",", fullIndex) > -1) {
            windowProps = windowProps.substring(0, fullIndex - 1) + newFullScreenString + windowProps.substring(windowProps.indexOf(",", fullIndex));
        } else {
            windowProps = windowProps.substring(0, fullIndex - 1) + newFullScreenString;
        }
    }
    return windowProps;
};
businessobjects.webutil.caf.getTopmostAccessibleWindow = function (args) {
    return businessobjects.webutil.caf.getAncestorFrame(null);
};
businessobjects.webutil.caf.getAppropriateOpenDocContainerFrame = function () {
    return businessobjects.webutil.caf.getAncestorFrame({propertyName: "isOpenDocContainerFrame"});
};
businessobjects.webutil.caf.getAncestorFrame = function (args) {
    var mywin = window;
    var topmostAccessibleWindow = window;
    try {
        while (mywin != mywin.parent && (!args || !args.propertyName || !mywin[args.propertyName])) {
            var test = mywin.name;
            topmostAccessibleWindow = mywin;
            mywin = mywin.parent;
        }
        var test = mywin.name;
        topmostAccessibleWindow = mywin;
    } catch (e) {
        return topmostAccessibleWindow;
    }
    return topmostAccessibleWindow;
};
businessobjects.webutil.isEnterKeyPressed = function (args) {
    var e = args.event;
    var keynum = 0;
    if (window.event) {
        keynum = e.keyCode;
    } else {
        if (e.which) {
            keynum = e.which;
        }
    }
    return (keynum == 13);
};
businessobjects.webutil.getCaretPosition = function (textCtrl) {
    var caretPosition = 0;
    if (document.selection) {
        textCtrl.focus();
        var caret = "\001";
        var selectionRange = document.selection.createRange();
        var selectedText = selectionRange.text;
        selectionRange.text = caret + selectedText;
        caretPosition = textCtrl.value.indexOf(caret);
        selectionRange.moveStart("character", -1);
        selectionRange.text = selectedText;
    } else {
        if (textCtrl.selectionStart || textCtrl.selectionStart == "0") {
            caretPosition = textCtrl.selectionStart;
        }
    }
    return caretPosition;
};
businessobjects.webutil.removeSelection = function (textCtrl) {
    if (document.selection) {
        var selectionRange = document.selection.createRange();
        selectionRange.text = "";
    } else {
        if (textCtrl.selectionStart || textCtrl.selectionStart == "0") {
            var selectedText = textCtrl.value.substring(textCtrl.selectionStart, textCtrl.selectionEnd);
            var newValue = textCtrl.value.replace(selectedText, "");
            textCtrl.value = newValue;
        }
    }
};
businessobjects.webutil.getActIDFromURL = function (url) {
    if (!url) {
        return "";
    }
    url = url.substring(url.indexOf("?"));
    url = url.replace(/%26/g, "&");
    url = url.replace(/%3D/g, "=");
    var actIdParam = "actId=";
    var actIdIndex = url.indexOf(actIdParam);
    var actId = "";
    if (actIdIndex >= 0) {
        var afterActId = url.substring(url.indexOf(actIdParam) + actIdParam.length);
        actId = afterActId.substring(0, afterActId.indexOf("&"));
    }
    return actId;
};
businessobjects.webutil.cafCallbackShowDialog = function (config) {
    return businessobjects.webutil.dialogservice.DialogService.showDialog(config);
};
businessobjects.webutil.addQueryStringSeperator = function (url) {
    if (url.length == 0) {
        return "?";
    }
    if (url.indexOf("?") == -1) {
        return url + "?";
    } else {
        if ("&" != url.charAt(url.length - 1)) {
            return url + "&";
        } else {
            return url;
        }
    }
};
businessobjects.webutil.mask;
businessobjects.webutil.spinner;
businessobjects.webutil.labelDiv;
businessobjects.webutil.hideLoadingStatus = function () {
    if (businessobjects.webutil.mask != undefined && businessobjects.webutil.spinner != undefined) {
        businessobjects.webutil.mask.style.display = "none";
        businessobjects.webutil.labelDiv.display = "none";
        businessobjects.webutil.spinner.style.display = "none";
    }
};
businessobjects.webutil.showLoadingStatus = function (thisDocument, loadingLabel, showSpinner) {
    if (showSpinner == null) {
        showSpinner = true;
    }
    if (businessobjects.webutil.mask) {
        businessobjects.webutil.mask.style.display = "block";
        businessobjects.webutil.spinner.style.display = "block";
    } else {
        var doc = thisDocument;
        businessobjects.webutil.mask = doc.createElement("div");
        businessobjects.webutil.mask.className = "spinnerMask";
        businessobjects.webutil.mask.style.width = YAHOO.util.Dom.getViewportWidth() + "px";
        businessobjects.webutil.mask.style.height = YAHOO.util.Dom.getViewportHeight() * 1.1 + "px";
        document.body.style.overflow = "hidden";
        doc.body.appendChild(businessobjects.webutil.mask);
        var w = 200;
        var h = 40;
        var left = Math.floor((YAHOO.util.Dom.getViewportWidth() - w) / 2);
        if (left < 0) {
            left = 0;
        }
        var top = Math.floor((YAHOO.util.Dom.getViewportHeight() - h) / 2);
        if (top < 0) {
            top = 0;
        }
        businessobjects.webutil.labelDiv = doc.createElement("div");
        if (loadingLabel) {
            var label = doc.createTextNode(loadingLabel);
            businessobjects.webutil.labelDiv.appendChild(label);
        }
        if (showSpinner) {
            businessobjects.webutil.spinner = doc.createElement("div");
            businessobjects.webutil.spinner.className = "spinner";
            businessobjects.webutil.spinner.style.left = left + "px";
            businessobjects.webutil.spinner.style.top = top + "px";
            if (loadingLabel) {
                businessobjects.webutil.spinner.title = loadingLabel;
            }
            businessobjects.webutil.spinner.appendChild(businessobjects.webutil.labelDiv);
            doc.body.appendChild(businessobjects.webutil.spinner);
        } else {
            businessobjects.webutil.labelDiv.className = "loading";
            businessobjects.webutil.labelDiv.style.left = left + "px";
            businessobjects.webutil.labelDiv.style.top = top + "px";
            doc.body.appendChild(businessobjects.webutil.labelDiv);
        }
    }
};