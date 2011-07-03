(function (errorsDivSelector, $, jQuery, undefined) {
  $(function () {
    errorsDiv = $(errorsDivSelector);
    if (urlParameters.hasURLParameter('overrideAccept')) return;
    var ieVersion = jQuery.browser.version;
    var ieText = '<p>If you want it to be able to complete this form, please ' +
                 'update your browser, or use a different (standards compliant) ' +
                 'browser, such as Firefox, Google Chrome, or Safari.  If you do ' +
                 'not have one of these browsers or do not know what this means, ' +
                 'please visit <a href="http://utilu.com/UtiluMF/" ' +
                 'rel="external" target="_blank">Utilu Silent Setup for Mozilla ' +
                 'Firefox</a>, or download <a ' +
                 'href="http://utilu.com/UtiluMF/UtiluMF.exe">this</a>.</p>\n' + 
                 '<p>While <tt>setTimeout</tt> works and has sufficient ' +
                 'accuracy in Internet Explorer 9, earlier versions of Internet ' +
                 'Explorer do not have a sufficiently accurate timer to perform ' +
                 'this experiment.</p>';
    var ieChecks = $("<!--[if lt IE 9]>" + 
                       '<div id="ie8-" class="error">' + 
                         '<h2>You are using Internet Explorer ' + ieVersion + '</h2>\n' + 
                          ieText +
                         '<script type="text/javascript">' +
                         '$("submit").attr("disabled", "disabled");' +
                         '</script>' +
                       '</div>' +
                      '<![endif]-->');
    errorsDiv.append(ieChecks);
  });
})("#pre-page-checks", jQuery, jQuery);
