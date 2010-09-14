(function () {
  function externalLinks() {   
    if (!document.getElementsByTagName) return;   
    var anchors = document.getElementsByTagName("a");
    var len = anchors.length;   
    for (var i = 0; i < len; i++) {   
      var anchor = anchors[i];   
      if (anchor.getAttribute("href") &&   
          anchor.getAttribute("rel") == "external")   
        anchor.target = "_blank";   
    }   
  }
  if (jQuery)
    $(externalLinks);
  else {
    var old_onload = window.onload;
    window.onload = function () {
      if (old_onload)
        old_onload();
      externalLinks();
    };
  }
})();
