String.prototype.trim = function () { return this.replace(/^\s\s*/, '').replace(/\s\s*$/, ''); };
if (Array.prototype.empty === undefined) Array.prototype.empty = function () { this.length = 0; };

//=============================================================
// From http://my.opera.com/GreyWyvern/blog/show.dml/1725165.
function clone (obj, alreadySeen) {
  var newObj = (obj instanceof Array) ? [] : {};
  if (alreadySeen === undefined)
    alreadySeen = {obj:newObj};
  for (var i in obj) {
    if (this[i] && typeof this[i] == "object") {
      if (!(i in alreadySeen))
	alreadySeen[i] = clone(this[i], alreadySeen);
      newObj[i] = alreadySeen[i];
    } else 
      newObj[i] = this[i]
  }
  return newObj;
};
//=============================================================

function keys(obj) {
  var rtn = [];
  if (obj instanceof Array) {
    for (var i = 0; i < obj.length; i++)
      if (!(obj[i] === undefined))
        rtn.push(i);
  } else {
    for (var i in obj)
      if (obj.hasOwnProperty(i)) //(!(i in this.constructor.prototype))
        rtn.push(i);
  }
  return rtn;
};

function deprecated(func, name, newName, warningFunc) {
  if (warningFunc === undefined) warningFunc = console.warn ? console.warn : console.log;
  if (newName === undefined) newName = func.name;
  return function () {
    warningFunc.call(console, 'Warning: ' + name + ' is deprecated.  Please use ' + newName + ' instead.');
    func.apply(this, arguments);
  };
}

var urlParameters = {
  'getURLParameters' : function getURLParameters(parameters) { // 'foo' : function foo(...) makes foo.name == 'foo'
    if (!(parameters instanceof Array)) parameters = [parameters];
    var rtn = {};
    jQuery.each(parameters, function (index, parameter) {
      if (urlParameters.hasURLParameter(parameter))
        rtn[parameter] = urlParameters.getURLParameter(parameter);
    });
    return rtn;
  },

  //=============================================================
  // From http://www.netlobo.com/url_query_string_javascript.html
  'getURLParameter' : function getURLParameter(name, ignoreCase, nullValue) {
    if (ignoreCase === undefined) ignoreCase = true;
    if (nullValue === undefined) nullValue = '';
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp(regexS, (ignoreCase ? 'i' : ''));
    var results = regex.exec(window.location.href);
    if (results == null)
      return nullValue;
    else
      return results[1];
  },

  'hasURLParameter': function hasURLParameter(name, ignoreCase) {
    if (ignoreCase === undefined) ignoreCase = true;
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"([&#=])";
    var regex = new RegExp(regexS, (ignoreCase ? 'i' : ''));
    var results = regex.exec(window.location.href+'#');
    return (results != null);
  }
  //=============================================================
};

var getURLParameter = deprecated(urlParameters.getURLParameter, 'getURLParameter', 'urlParameters.getURLParameter');
var hasURLParameter = deprecated(urlParameters.hasURLParameter, 'hasURLParameter', 'urlParameters.hasURLParameter');

function toBool(value, nullValue)
{
  if (nullValue === undefined) nullValue = null;
  if (value === true || value === false) return value;
  value = value.toLowerCase();
  value = value.trim();
  if (value.charAt(0) == 'f' || value.charAt(0) == '0' || value.charAt(0) == 'n') return false;
  if (value.charAt(0) == 't' || value.charAt(0) == '1' || value.charAt(0) == 'y') return true;
  return nullValue;
}


//=============================================================
// From http://laurens.vd.oever.nl/weblog/items2005/setsinjavascript/
function set ()
{
  var result = {};

  for (var i = 0; i < arguments.length; i++)
    result[arguments[i]] = true;

  return result;
}
//=============================================================

/*
function getIPAddress()
{
// http://www.kdcgrohl.com

// Depending on your server set-up,
// you may need to use the ".shtml"
// extension [instead of the "html"
// or "htm"] as the script uses Server
// Side Includes.
// This part gets the IP 
  var ip = '<!--#echo var="REMOTE_ADDR"-->';
  return ip;
}*/

function sample(population, k)
{
  /* Chooses k unique random elements from a population sequence.

     Returns a new list containing elements from the population while
     leaving the original population unchanged.  The resulting list is
     in selection order so that all sub-slices will also be valid random
     samples.  This allows raffle winners (the sample) to be partitioned
     into grand prize and second place winners (the subslices).

     Members of the population need not be hashable or unique.  If the
     population contains repeats, then each occurrence is a possible
     selection in the sample.
  */

  // Sampling without replacement entails tracking either potential
  // selections (the pool) in a list or previous selections in a set.

  // When the number of selections is small compared to the
  // population, then tracking selections is efficient, requiring
  // only a small set and an occasional reselection.  For
  // a larger number of selections, the pool tracking method is
  // preferred since the list takes less space than the
  // set and it doesn't suffer from frequent reselections.

  var n = population.length;
  if (k === undefined) k = n;
  if (!(0 <= k && k <= n))
    throw new Error("sample larger than population"); // ValueError
  //random = self.random
  //_int = int
  var result = new Array(k);
  var setsize = 21; // size of a small set minus size of an empty list
  if (k > 5)
    setsize += Math.pow(4, Math.ceil(Math.log(k * 3) / Math.log(4))); // table size for big sets
  if (n <= setsize) { // ||  hasattr(population, "keys"):
    // An n-length list is smaller than a k-length set, or this is a
    // mapping type so the other algorithm wouldn't work.
    var pool = population.slice(0); // Make a copy of population
    for (var i = 0; i < k; i++) { // invariant:  non-selected at [0,n-i)
      var j = Math.floor(Math.random() * (n-i));
      result[i] = pool[j];
      pool[j] = pool[n-i-1];  // move non-selected item into vacancy
    }
  } else {
    var selected = set();
    selected_add = function (value) { selected[value] = true; }
    for (var i = 0; i < k; i++) {
      var j = Math.floor(Math.random() * n);
      while (j in selected)
        j = Math.floor(Math.random() * n);
      selected_add(j);
      result[i] = population[j];
    }
  }
  return result;
}

function depth(array)
{
  if (array.length == null) return 0;
  else return 1 + depth(array[0]);
}

function transpose(matrix)
{
  var mDepth = depth(matrix);
  if (mDepth == 0) return matrix;
  if (mDepth == 1) return matrix;
  if (mDepth == 2) {
    var rtn = [];
    var cur;
    for (var i = 0; i < matrix.length; i++) {
      cur = [];
      for (var j = 0; j < matrix[i].length; j++) {
        cur.push(matrix[j][i]);
      }
      rtn.push(cur);
    }
    return rtn;
  }
  alert('Transposition of ' + mDepth + '-dimensional matrices is not currently supported.');
}


//=============================================================
// from http://javascript.about.com/library/blradio4.htm
// Radio Button Validation
// copyright Stephen Chapman, 15th Nov 2004,14th Sep 2005
// you may copy this function but please keep the copyright notice with it
function valButton(btn) {
    var cnt = -1;
    for (var i=btn.length-1; i > -1; i--) {
        if (btn[i].checked) {cnt = i; i = -1;}
    }
    if (cnt > -1) return btn[cnt];
    else return null;
}
//=============================================================


//=============================================================
// from python 2.6 urllib
function unquote(s) { // maybe just use unescape()?
	// unquote('abc%20def') -> 'abc def'.
    var res = s.split('%');
    for (var i = 1; i < res.length; i++) {
        var item = res[i];
        try {
			res[i] = String.fromCharCode(parseInt(item.slice(0, 2), 16)) + item.slice(2);
        } catch(err) { //KeyError:
            res[i] = '%' + item;
	    }
	}
    return res.join('');
}

var _safemaps = [];

function quote(s, safe) {// maybe just use escape()?
	/* quote('abc def') -> 'abc%20def'
     *
     * Each part of a URL, e.g. the path info, the query, etc., has a
     * different set of reserved characters that must be quoted.
     * 
     * RFC 2396 Uniform Resource Identifiers (URI): Generic Syntax lists
     * the following reserved characters.
     * 
     * reserved    = ";" | "/" | "?" | ":" | "@" | "&" | "=" | "+" |
     *               "$" | ","
     * 
     * Each of these characters is reserved in some component of a URL,
     * but not necessarily in all of them.
     * 
     * By default, the quote function is intended for quoting the path
     * section of a URL.  Thus, it will not encode '/'.  This character
     * is reserved, but in typical usage the quote function is being
     * called on a path where the existing slash characters are used as
     * reserved characters.
    **/
	if (safe === undefined) safe = '/';
	var always_safe = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-';
    var cachekey = [safe, always_safe];
    try {
		var safe_map = _safemaps[cachekey];
		if (safe_map === undefined) throw "KeyError";
    } catch(err) { // KeyError:
        safe += always_safe;
        var safe_map = [];
        for (var i = 0; i < 256; i++) {
            var c = String.fromCharCode(i);
            safe_map[c] = (safe.indexOf(c) != -1) && (c) || ('%' + i.toString(16));
		}
        _safemaps[cachekey] = safe_map;
	}
	var res = [];
	for (var i = 0; i < s.length; i++) 
		res[i] = safe_map[s[i]];
    return res.join('');
}
//=============================================================


//=============================================================
// From http://www.electrictoolbox.com/pad-number-zeroes-javascript/
function pad(number, length) {
   
  var str = '' + number;
  while (str.length < length) {
    str = '0' + str;
  }
 
  return str;
}
//=============================================================


function timeDelta(startTime, endTime) {
  var rtn = {};
  rtn.totalMilliseconds = endTime.valueOf() - startTime.valueOf();
  rtn.milliseconds = rtn.totalMilliseconds % 1000;
  rtn.totalSeconds = Math.floor(rtn.totalMilliseconds / 1000);
  rtn.seconds = rtn.totalSeconds % 60;
  rtn.totalMinutes = Math.floor(rtn.totalSeconds / 60);
  rtn.minutes = rtn.totalMinutes % 60;
  rtn.totalHours = Math.floor(rtn.totalMinutes / 60);
  rtn.hours = rtn.totalHours % 24;
  rtn.totalDays = Math.floor(rtn.totalHours / 24);
  rtn.days = rtn.totalDays % 365;
  rtn.totalYears = Math.floor(rtn.totalDays / 365);
  rtn.years = rtn.totalYears;
  return rtn;
}

function dateUTC(d) {
  return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(),                          
    d.getUTCDay(), d.getUTCHours(), d.getUTCMinutes(), d.getUTCSeconds(),             
    d.getUTCMilliseconds());
}

function convertDateToDateTimeInputString(date) {
  // Spec from http://www.whatwg.org/specs/web-apps/current-work/multipage/common-microsyntaxes.html#dates-and-times
  var rtn = '';
  var yearString = pad(date.getFullYear(), 4);
  var monthString = pad(date.getMonth(), 2);
  var dayString = pad(date.getDay(), 2);
  var hourString = pad(date.getHours(), 2);
  var minuteString = pad(date.getMinutes(), 2);
  var secondString = pad(date.getSeconds(), 2);
  var millisecondString = pad(date.getMilliseconds(), 3);
  var offsetSign = (date.getTimezoneOffset() > 0 ? '+' : '-');
  var offsetHours = pad(Math.abs(date.getTimezoneOffset()) / 60, 2);
  var offsetMinutes = pad(Math.abs(date.getTimezoneOffset()) % 60, 2);
  return yearString + '-' + monthString + '-' + dayString + 'T' + hourString + ':' + minuteString + ':' + secondString +
    '.' + millisecondString + offsetSign + offsetHours + ':' + offsetMinutes;
}

//=============================================================
// From http://www.shawnolson.net/a/503/altering-css-class-attributes-with-javascript.html.
if (this['changecss'] === undefined)
  changecss = function changecss(theClass, element, value, onError) {
    // Last Updated by original author on June 23, 2009
    // documentation for this script at
    // http://www.shawnolson.net/a/503/altering-css-class-attributes-with-javascript.html
    var cssRules;

    var added = false;

    var s;

    for (s = 0; s < document.styleSheets.length; s++) {
      if (document.styleSheets[s]['rules'])
	cssRules = document.styleSheets[s]['rules'];
      else if (document.styleSheets[s]['cssRules'])
	cssRules = document.styleSheets[s]['cssRules'];
      else if (document.styleSheets[s].length)
        cssRules = document.styleSheets[s];
      else { // no rules found... browser unknown
/*	if (onError !== undefined)
	  onError();*/
	continue;
      }

      for (var r = cssRules.length - 1; r >= 0; r--) {
	if (cssRules[r].selectorText == theClass) {
	  if (cssRules[r].style[element]) {
	    cssRules[r].style[element] = value;
	    added = (cssRules[r].style[element] == value);
	    break;
	  }
	}
      }
    }

    s = document.styleSheets.length - 1;
    if (!added) {
      if (document.styleSheets[s].addRule) {
	document.styleSheets[s].addRule(theClass, element+':'+value);
      } else if (document.styleSheets[s].insertRule) {
	document.styleSheets[s].insertRule(theClass + ' { ' + element + ': ' +
	  value + '; }', cssRules.length);
      } else if (onError !== undefined)
        onError();
    }
    console.log(document.styleSheets[s]);
  } 
//=============================================================


//===================================================================
// From http://www.somacon.com/p143.php

// return the value of the radio button that is checked
// return an empty string if none are checked, or
// there are no radio buttons
function getCheckedValue(radioObj) {
  if (!radioObj)
    return "";
  var radioLength = radioObj.length;
  if (radioLength === undefined)
    if (radioObj.checked)
      return radioObj.value;
    else
      return "";
  for (var i = 0; i < radioLength; i++) {
    if (radioObj[i].checked) {
      return radioObj[i].value;
    }
  }
  return "";
}

// set the radio button with the given value as being checked
// do nothing if there are no radio buttons
// if the given value does not exist, all the radio buttons
// are reset to unchecked
function setCheckedValue(radioObj, newValue) {
  if (!radioObj)
    return;
  var radioLength = radioObj.length;
  newValue = '' + newValue;
  if (radioLength === undefined) {
    radioObj.checked = (newValue == radioObj.value);
    return;
  }
  for (var i = 0; i < radioLength; i++) {
    radioObj[i].checked = (newValue == radioObj[i].value);
  }
}
//===================================================================

//===================================================================
//From http://skuld.bmsc.washington.edu/~merritt/gnuplot/canvas_demos/
function getMouseCoordsWithinTarget(event) {
  var coords = {x: 0, y: 0};

  if (!event) { // then we're in a non-DOM (probably IE) browser
    event = window.event;
    if (event) {
      coords.x = event.offsetX;
      coords.y = event.offsetY;
    }
  } else {		// we assume DOM modeled javascript
    var Element = event.target;
    var CalculatedTotalOffsetLeft = 0;
    var CalculatedTotalOffsetTop = 0;

    while (Element.offsetParent) {
      CalculatedTotalOffsetLeft += Element.offsetLeft;
      CalculatedTotalOffsetTop += Element.offsetTop;
      Element = Element.offsetParent;
    }

    coords.x = event.pageX - CalculatedTotalOffsetLeft;
    coords.y = event.pageY - CalculatedTotalOffsetTop;
  }

  return coords;
}
//===================================================================



function makeInput(id, value, type) {
  if (value === undefined) value = '';
  if (type === undefined) type = 'hidden';
  return $('<input>')
    .attr('type', type)
    .attr('value', value)
    .attr('id', id)
    .attr('name', id);
}
