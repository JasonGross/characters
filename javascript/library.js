String.prototype.trim = function() { return this.replace(/^\s\s*/, '').replace(/\s\s*$/, ''); }

//=============================================================
// From http://my.opera.com/GreyWyvern/blog/show.dml/1725165
Object.prototype.clone = function() {
  var newObj = (this instanceof Array) ? [] : {};
  for (i in this) {
    if (i == 'clone') continue;
    if (this[i] && typeof this[i] == "object") {
      newObj[i] = this[i].clone();
    } else newObj[i] = this[i]
  } return newObj;
};
//=============================================================

Object.prototype.keys = function() {
  var rtn = [];
  if (this instanceof Array) {
    for (var i = 0; i < this.length; i++)
      if (!(this[i] === undefined))
        rtn.push(i);
  } else {
    for (var i in this)
      if (!(i in this.constructor.prototype))
        rtn.push(i);
  }
  return rtn;
};

//=============================================================
// From http://www.netlobo.com/url_query_string_javascript.html
function getURLParameter( name, ignoreCase)
{
  if (ignoreCase === undefined) ignoreCase = true;
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS, (ignoreCase ? 'i' : ''));
  var results = regex.exec( window.location.href );
  if( results == null )
    return '';
  else
    return results[1];
}
function hasURLParameter( name, ignoreCase )
{
  if (ignoreCase === undefined) ignoreCase = true;
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"([&#])";
  var regex = new RegExp( regexS, (ignoreCase ? 'i' : ''));
  var results = regex.exec( window.location.href+'#' );
  return ( results != null );
}

//=============================================================


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
  rtn.totalYears = Math.floor(rtn.totalDats / 365);
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
