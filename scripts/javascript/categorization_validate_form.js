// JavaScript Document
$(function () {
  $('form').submit(function () {
    var doAlert = false;
    var toURL;
    $('select').each(function() {
      if (this[this.selectedIndex].value < 0) {
        doAlert = true;
        if (!toURL)
          toURL = this.id.slice(0, this.id.indexOf('_number_test_')).replace(/_group_/g, '-set-');
        $(this).addClass('unfilled-form-element');
      }
    });
    $('select').change(function() { $(this).removeClass('unfilled-form-element'); });
    if (toURL !== undefined)
      window.location.hash = toURL;
    if (doAlert)
      alert('You must categorize every character.  Please check the inputs outlined in red.');
    else {
      var feedback = $('#feedback');
      feedback.html(feedback.html().replace(/\n/g, '\\n').replace(/\r/g, '\\r'));
      $('#form-submit-time').attr('value', dateUTC(new Date()));
      var duration = timeDelta(formFinishedLoadingTime, new Date());
      $('#duration').attr('value', duration.years + 'y ' + duration.days + 'd ' + duration.hours + 'h ' + 
        duration.minutes + 'm ' + duration.seconds + 's ' + duration.milliseconds + 'ms');
    }
    return !doAlert;
  });
});
