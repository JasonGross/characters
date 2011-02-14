var fixFormat;
var isMSIE = /*@cc_on!@*/false;
(function () {

  if (!window.console) {
    window.console = {
        log : function (message) {}
      };
  }
  
  fixFormat = function (format) {
    if (!(format instanceof String))
      return format;
    format = format.toLowerCase();
    switch (format) {
      case 'text': return 'text/plain';
      case 'url': return 'text/uri-list';
      default: return format;
    }
  }
  
  
  /*if (jQuery.browser.webkit) {
    Clipboard.prototype.__patch_data_object = {};
    
    Clipboard.prototype.clearData = function (format) {
        format = fixFormat(format);
        if (format !== undefined) {
          if (format in this.__patch_data_object)
            delete this.__patch_data_object[format];
        } else {
          var keys = keys(this.__patch_data_object);
          for (var keyI = 0; keyI < keys.length; keyI++)
            delete this.__patch_data_object[keys[keyI]];
        }
      };
    Clipboard.prototype.setData = function (format, data) {
        format = fixFormat(format);
        this.__patch_data_object[format] = data;
      };
    Clipboard.prototype.getData = function (format) {
        format = fixFormat(format);
        return this.__patch_data_object[format];
      };
  
  }*/
  
  /*var testInput = document.createElement("input");
  testInput.setAttribute("type", "datetime");
  if (!testInput.valueAsDate) {
    if (testInput.__addSetter__) {
      testInput.constructor.prototype.__addSetter__('valueAsDate', function (newDate) { this.value = convertDateToDateTimeInputString(newDate); });
      testInput.constructor.prototype.__addGetter__('valueAsDate', function (newDate) { this.value = convertDateToDateTimeInputString(newDate); });
      testInput.constructor.prototype.__addSetter__('valueAsDate', function (newDate) { this.value = convertDateToDateTimeInputString(newDate); });
      testInput.constructor.prototype.__addSetter__('valueAsDate', function (newDate) { this.value = convertDateToDateTimeInputString(newDate); });
    }
  }*/

  // from http://stackoverflow.com/questions/1181575/javascript-determine-whether-an-array-contains-a-value
  if (!Array.prototype.indexOf) {
    Array.prototype.indexOf = function(needle) {
      for (var i = 0; i < this.length; i++) {
        if (this[i] === needle) {
          return i;
        }
      }
      return -1;
    };
  }
})();
