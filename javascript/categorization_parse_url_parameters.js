//==========================================================
//Constants
//End Constants
//==========================================================
//Change default values here
var trainingCharactersPerAlphabet = 2;
var numberOfGroups = 5;
var alphabetsPerGroup = 10;
var questionsPerGroup = 1;
//var imageWidth = 75;
//var imageHeight = 75;
var alertStyle = null;
var alertBorderWidth = 'thick';
var alertBorderColor = 'red';
var alertBorderStyle = 'solid';

//End default values
//==========================================================


function setTrainingCharactersPerAlphabet(newCount) { trainingCharactersPerAlphabet = parseInt(newCount); }
function getTrainingCharactersPerAlphabet() { return trainingCharactersPerAlphabet; }

function setNumberOfGroups(newCount) { numberOfGroups = parseInt(newCount); }
function getNumberOfGroups() { return numberOfGroups; }

function setAlphabetsPerGroup(newCount) { alphabetsPerGroup = parseInt(newCount); }
function getAlphabetsPerGroup() { return alphabetsPerGroup; }

function setQuestionsPerGroup(newCount) { questionsPerGroup = parseInt(newCount); }
function getQuestionsPerGroup() { return questionsPerGroup; }


if (getURLParameter('trainingCharactersPerAlphabet') != '')
  setTrainingCharactersPerAlphabet(getURLParameter('trainingCharactersPerAlphabet'));

if (getURLParameter('numberOfGroups') != '')
  setNumberOfGroups(getURLParameter('numberOfGroups'));

if (getURLParameter('alphabetsPerGroup') != '')
  setAlphabetsPerGroup(getURLParameter('alphabetsPerGroup'));

if (getURLParameter('questionsPerGroup') != '')
  setQuestionsPerGroup(getURLParameter('questionsPerGroup'));


if (getURLParameter('alertStyle') != '') setAlertStyle(getURLParameter('alertStyle'));
if (getURLParameter('alertBorderWidth') != '') setAlertBorderWidth(getURLParameter('alertBorderWidth'));
if (getURLParameter('alertBorderStyle') != '') setAlertBorderStyle(getURLParameter('alertBorderStyle'));
if (getURLParameter('alertBorderColor') != '') setAlertBorderColor(getURLParameter('alertBorderColor'));

