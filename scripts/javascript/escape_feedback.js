$(function () {
  $('form').submit(function () {
    var feedback = $('#feedback');
    feedback.attr('value', feedback.attr('value').replace(/\n/g, '\\n').replace(/\r/g, '\\r').replace(/\t/g, '\\t'));
    return true;
  });
});
