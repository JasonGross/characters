// JavaScript Document

var unansweredInput;
var answeredInput;
var doOnUnansweredInput;
var doOnAnsweredInput;

(function () {
  $('input[type=submit]').removeAttr('disabled');
  var inputsLeft = {};
  var unansweredInputFunctions = [];
  var answeredInputFunctions = [];
  doOnUnansweredInput = function (func) { unansweredInputFunctions.push(func); };
  doOnAnsweredInput = function (func) { answeredInputFunctions.push(func); };
  unansweredInput = function (key) {
    if (!(key in inputsLeft)) inputsLeft[key] = 0;
    inputsLeft[key]++;
    jQuery.each(unansweredInputFunctions, function (index, func) { func(key); });
  };
  answeredInput = function (key) {
    if (!(key in inputsLeft)) inputsLeft[key] = 0;
    inputsLeft[key]--;
    if (inputsLeft[key] == 0)
      jQuery.each(answeredInputFunctions, function (index, func) { func(key); });
  };
  doOnUnansweredInput(function () { $('input[type=submit]').attr('disabled', 'disabled'); });
  doOnAnsweredInput(function () { $('input[type=submit]').removeAttr('disabled'); });
})();

$(function () {
  $('form').submit(function () {
    var feedback = $('#feedback');
    feedback.html(feedback.html().replace(/\n/g, '\\n').replace(/\r/g, '\\r'));
    $('#form-submit-time').attr('value', dateUTC(new Date()));
    var duration = timeDelta(formFinishedLoadingTime, new Date());
    $('#duration').attr('value', duration.years + 'y ' + duration.days + 'd ' + duration.hours + 'h ' + 
      duration.minutes + 'm ' + duration.seconds + 's ' + duration.milliseconds + 'ms');
    return true;
  });
});
