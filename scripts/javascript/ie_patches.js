(function () {
  var _ie_patch_data_transfer_data_object = {};
  var addOwnDataTransfer = !window['DataTransfer'];
  if (addOwnDataTransfer)
    window['DataTransfer'] = {};
  var dt = (DataTransfer.prototype ? DataTransfer.prototype : DataTransfer);
  function fixDataTransfer(dt) {
    dt.clearData = function (format) {
      format = fixFormat(format);
      if (format !== undefined) {
        if (format in _ie_patch_data_transfer_data_object)
          delete _ie_patch_data_transfer_data_object[format];
      } else {
        var keys = keys(_ie_patch_data_transfer_data_object);
        for (var keyI = 0; keyI < keys.length; keyI++)
          delete _ie_patch_data_transfer_data_object[keys[keyI]];
      }
    }
    
    dt.setData = function (format, data) {
      format = fixFormat(format);
      _ie_patch_data_transfer_data_object[format] = data;
    }
    
    dt.getData = function (format) {
      format = fixFormat(format);
      return _ie_patch_data_transfer_data_object[format];
    }
  }
  fixDataTransfer(dt);

  //try {
  //  var _ie_patches_global_data_transfer = new DataTransfer();
  //} catch(err) {
  var _ie_patches_global_data_transfer = DataTransfer;
  //}
  
  // This is a terrible hack, and I really shouldn't be doing this,
  // but I don't know any other way to get to IE's DataTransfer object
  jQuery.fn.oldBind = jQuery.fn.bind;
  jQuery.fn.bind = function (type, data, fn) {
    if (type == 'dragstart' || type == 'drop') {
      this.oldBind(type, function (ev) {
        var newOriginalEvent = {}
        for (var i in ev.originalEvent)
          if (i != 'dataTransfer')
            newOriginalEvent[i] = ev.originalEvent[i];
        ev.originalEvent = newOriginalEvent;
        ev.originalEvent['dataTransfer'] = dt;
      });
    }
    return this.oldBind(type, data, fn);
  };

})();
