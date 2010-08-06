// JavaScript Document
$(function () {
  $('form').submit(function () {
    var doAlert = false;
    var toURL;
    $('select').each(function() {
      if (this[this.selectedIndex].value < 0) {
        doAlert = true;
        if (!toURL)
          toURL = this.id;
        $(this).addClass('unfilled-form-element');
      }
    });
    $('select').change(function() { $(this).removeClass('unfilled-form-element'); });
    window.location.hash = toURL;
    if (doAlert)
      alert('You must categorize every character.  Please check the inputs outlined in red.');
    else {
      var feedback = $('#feedback');
      feedback.html(feedback.html().replace(/\n/g, '\\n').replace(/\r/g, '\\r'));
    }
    return !doAlert;
  });
});
