function isTurk() {
  return urlParameters.hasURLParameter('assignmentId') && urlParameters.hasURLParameter('hitId');
}

function isTurkSandbox() {
  return isTurk() && urlParameters.getURLParameter('assignmentId') == 'ASSIGNMENT_ID_NOT_AVAILABLE';
}
