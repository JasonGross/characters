var _ie_patch_data_transfer_data_object = {};
DataTransfer.prototype.clearData = function (format) {
  format = fixFormat(format);
  if (format !== undefined) {
    if (format in _ie_patch_data_transfer_data_object)
      delete _ie_patch_data_transfer_data_object[format];
  } else {
    var keys = _ie_patch_data_transfer_data_object.keys();
    for (var keyI = 0; keyI < keys.length; keyI++)
      delete _ie_patch_data_transfer_data_object[keys[keyI]];
  }
}

DataTransfer.prototype.setData = function (format, data) {
  format = fixFormat(format);
  _ie_patch_data_transfer_data_object[format] = data;
}

DataTransfer.prototype.getData = function (format) {
  format = fixFormat(format);
  return _ie_patch_data_transfer_data_object[format];
}

var _ie_patches_global_data_transfer = DataTransfer;

$('*').live('ondragstart', function (ev) {
  if (!ev.originalEvent.dataTransfer)
    ev.originalEvent.dataTransfer = _ie_patches_global_data_transfer;
  if (this.dragstart)
    this.dragstart(ev.originalEvent)
}).live('ondrag', function (ev) {
  if (!ev.originalEvent.dataTransfer)
    ev.originalEvent.dataTransfer = _ie_patches_global_data_transfer;
  if (this.drag)
    this.drag(ev.originalEvent)
}).live('ondragenter', function (ev) {
  if (!ev.originalEvent.dataTransfer)
    ev.originalEvent.dataTransfer = _ie_patches_global_data_transfer;
  if (this.dragenter)
    this.dragenter(ev.originalEvent)
}).live('ondragover', function (ev) {
  if (!ev.originalEvent.dataTransfer)
    ev.originalEvent.dataTransfer = _ie_patches_global_data_transfer;
  if (this.dragover)
    this.dragover(ev.originalEvent)
}).live('ondragleave', function (ev) {
  if (!ev.originalEvent.dataTransfer)
    ev.originalEvent.dataTransfer = _ie_patches_global_data_transfer;
  if (this.dragleave)
    this.dragleave(ev.originalEvent)
}).live('ondragend', function (ev) {
  if (!ev.originalEvent.dataTransfer)
    ev.originalEvent.dataTransfer = _ie_patches_global_data_transfer;
  if (this.dragend)
    this.dragend(ev.originalEvent)
}).live('ondrop', function (ev) {
  if (!ev.originalEvent.dataTransfer)
    ev.originalEvent.dataTransfer = _ie_patches_global_data_transfer;
  if (this.drop)
    this.drop(ev.originalEvent)
});
