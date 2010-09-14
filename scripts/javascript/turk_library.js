function isTurk() {
  return hasURLParameter('assignmentId') && hasURLParameter('hitId');
}

function isTurkSandbox() {
  return isTurk() && getURLParameter('assignmentId') == 'ASSIGNMENT_ID_NOT_AVAILABLE';
}
