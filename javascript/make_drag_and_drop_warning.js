(function (warningDivId) {
  if (document.createElement('div').ondragstart === undefined) {
    var heading = '';
    var message = $('<p>').append('The drag-and-drop functionality ' + 
      'will not work.  If you want it to be able to use drag-and-drop ' +
      'to complete this form, please update your browser, or use a ' +
      'different (standards compliant) browser, such as Firefox, ' +
      'Google Chrome, or Safari.  If you do not have one of these ' + 
      'browsers or do not know what this means, please visit ' + 
      '<a href="http://utilu.com/UtiluMF/" rel="external" ' +
      'target="_blank">Utilu Silent Setup for Mozilla Firefox</a>, ' + 
      'or download <a href="http://utilu.com/UtiluMF/UtiluMF.exe">this</a>.');
    var postMessage = $('<p>').append('Please note that drag-and-drop functionality is <em>not</em> required to complete this form.');
    if (jQuery.browser.opera) {
      heading = $('<h2>').append('You are using Opera.');
    } else if (jQuery.browser.msie) {
      heading = $('<h2>').append('You are using Internet Explorer.');
    }
    $(function () {
      $('#' + warningDivId)
        .append(heading)
        .append(message)
        .append(postMessage);
    });
  } else {
    $(function () { $('#' + warningDivId).remove(); });
  }    
})("drag-and-drop-warnings");
