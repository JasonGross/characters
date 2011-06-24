var HintedTasks;
(function (jQuery, $, undefined) {
  HintedTasks = function (defaultPauseToHints, defaultTagFuncs, defaultDoOnHints, defaultRecordInfo) {

    function doNextPrompt(cbdata, pauseToHints, tagFuncs, doOnHints, recordInfo) {
      if (doOnHints.length > 0 && doOnHints[0]) doOnHints[0](cbdata);
      if (tagFuncs.length > 0 && recordInfo && tagFuncs[0])
        recordInfo(tagFuncs[0], dateUTC(new Date()));
      if (pauseToHints.length > 0 && pauseToHints[0] >= 0)
        setTimeout(function () { doNextPrompt(cbdata, pauseToHints.slice(1), tagFuncs.slice(1), doOnHints.slice(1), recordInfo); },
                   pauseToHints[0]);
    }
    
    function fillIn(list, defaultList, overwrite) {
      if (overwrite === undefined) overwrite = false;
      if (list === undefined) return defaultList;
      if (!overwrite) list = list.slice(0); // copy array
      for (var i = 0; i < list.length; i++)
        if (list[i] === undefined)
          list[i] = defaultList[i];
      return list;
    }

    this.beginPrompting = function beginPrompting(cbdata, pauseToHints, tagFuncs, doOnHints, recordInfo) {
      pauseToHints = fillIn(pauseToHints, defaultPauseToHints);
      tagFuncs = fillIn(tagFuncs, defaultTagFuncs);
      doOnHints = fillIn(doOnHints, defaultDoOnHints);
      if (recordInfo === undefined) recordInfo = defaultRecordInfo;
      setTimeout(function () { doNextPrompt(cbdata, pauseToHints.slice(1), tagFuncs, doOnHints, recordInfo); },
                 pauseToHints[0]);
    }
    
    return this;
  };
})(jQuery, jQuery);
