var urlParameters = new (function () {
  this.getParameters(parameters) {
    if (!(parameters instanceof Array)) parameters = [parameters];
    var rtn = {};
    jQuery.each(parameters, function (index, parameter) {
      if (hasURLParameter(parameter))
        rtn[parameter] = getURLParameter(parameter);
    });
    return rtn;
  }
})();