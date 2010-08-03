function fixFormat(format) {
  if (!(format instanceof String))
    return format;
  format = format.toLowerCase();
  switch (format) {
    case 'text': return 'text/plain';
    case 'url': return 'text/uri-list';
    default: return format;
  }
}




if (!window.console) {
  var console = {
      log : function (message) {}
    };
}

if (jQuery.browser.webkit) {
  Clipboard.prototype.__patch_data_object = {};
  
  Clipboard.prototype.clearData = function (format) {
      format = fixFormat(format);
      if (format !== undefined) {
        if (format in this.__patch_data_object)
          delete this.__patch_data_object[format];
      } else {
        var keys = this.__patch_data_object.keys();
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

} 
