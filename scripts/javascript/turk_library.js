function isTurk() {
  return urlParameters.hasURLParameter('assignmentId') && urlParameters.hasURLParameter('hitId');
}

function isTurkPreview() {
  return isTurk() && urlParameters.getURLParameter('assignmentId') == 'ASSIGNMENT_ID_NOT_AVAILABLE';
}

function isTurkSandbox() {
  if (!isTurk()) return false;
  var submitTo = urlParameters.getURLParameter('turkSubmitTo');
  return submitTo.substring(submitTo.length - 'workersandbox.mturk.com'.length) == 'workersandbox.mturk.com';
}
