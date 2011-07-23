//==========================================================
//Constants
var ROWS_FIRST = 0;
var COLS_FIRST = 1;
var HEIGHT = 0;
var WIDTH = 1;
//End Constants
//==========================================================
//Change default values here
var lineWidth = 5;
var imageSize = 'fitHeight';
var canvasWidth = 'fit';
var canvasHeight = 'fit';
var lineCap = 'butt';
var sampleCount = 1;
var _isHorizontal = false;
//var numRows = 3;
//var numCols = null;
//var characterOrder = ROWS_FIRST;
var alertStyle = null;
var alertBorderWidth = 'thick';
var alertBorderColor = 'red';
var alertBorderStyle = 'solid';
var randomizeOrder = true;
var checkAll = true;
var askFeedback = true;
var askInputDevice = true;
var askSeenBefore = true;

var backupCanvasHeight = '200px';
var backupCanvasWidth = '300px';
var defaultFallBackDimen = HEIGHT;

var formAction = 'scripts/python/record-request-submission.py';


function getCharacterId(tag) 
{
  if (urlParameters.getURLParameter('character'+tag+'ID') != '')
    return 'character_'+urlParameters.getURLParameter('character'+tag+'ID');
  if (urlParameters.getURLParameter('image'+tag+'ID') != '')
    return 'character_'+urlParameters.getURLParameter('image'+tag+'ID');
  return 'character-'+tag;
}

function defaultFeedbackString() { return 'Please enter any feedback you have here.'; }

//End default values
//==========================================================

function setLineWidth(newWidth) { lineWidth = newWidth; }
function getLineWidth() { return lineWidth; }

function setHorizontal() { _isHorizontal = true; }
function isHorizontal() { return _isHorizontal; }

function setVertical() { setHorizontal(false); }
function isVertical() { return !isHorizontal(); }

function setImageSize(newSize) { imageSize = newSize; }
function getImageSize()
{
  if (imageSize.toLowerCase() == 'fitheight') {
    if (getCanvasHeight() != 'fit')
      return ' height="' + getCanvasHeight() + '"';
    else if (getCanvasWidth() != 'fit')
      return ' width="' + getCanvasWidth() + '"';
  } else if (imageSize.toLowerCase() == 'fitwidth') {
    if (getCanvasWidth() != 'fit')
      return ' width="' + getCanvasWidth() + '"';
    else if (getCanvasHeight() != 'fit')
      return ' height="' + getCanvasHeight() + '"';
  } else return imageSize;
  switch (defaultFallBackDimen)
  {
    case HEIGHT: return ' height="' + backupCanvasHeight + '"';
    case WIDTH: return ' width="' + backupCanvasWidth + '"';
  }
}

function setCanvasWidth(newWidth) { canvasWidth = (newWidth.toLowerCase() != 'fit' ? newWidth : 'fit'); }
function getCanvasWidth() { return canvasWidth; }

function setCanvasHeight(newHeight) { canvasHeight = (newHeight.toLowerCase() != 'fit' ? newHeight : 'fit'); }
function getCanvasHeight() { return canvasHeight; }

function setLineCap(newCap) { lineCap = newCap; }
function getLineCap() { return lineCap; }

function setSampleCount(newCount) { sampleCount = parseInt(newCount); }
function getSampleCount() { return sampleCount; }


function setCharacterOrder(newOrder) { characterOrder = newOrder; }
function getCharacterOrder() { return characterOrder; }


//function setNumRows(newNum) { numRows = numRows; }
//function getNumRows() { return numRows; }

//function setNumCols(newNum) { numCols = numCols; }
//function getNumCols() { return numCols; }

function setRandomizeOrder(newVal) { randomizeOrder = toBool(newVal, randomizeOrder); }
function getRandomizeOrder() { return randomizeOrder; }

function setCheckAll(newVal) { checkAll = toBool(newVal, checkAll); }
function getCheckAll() { return checkAll; }

function setAskSeenBefore(newVal) { askSeenBefore = toBool(newVal, askSeenBefore); }
function getAskSeenBefore() { return askSeenBefore; }

function setAskInputDevice(newVal) { askInputDevice = toBool(newVal, askInputDevice); }
function getAskInputDevice() { return askInputDevice; }

function setAskFeedback(newVal) { askFeedback = toBool(newVal, askFeedback); }
function getAskFeedback() { return askFeedback; }

var canvases = [];

function getCanvases() { return canvases; }
function addCanvas(newCanvas) { canvases.push(newCanvas); }

function setAlertStyle(newStyle) { alertStyle = newStyle; }
function setAlertBorderWidth(newWidth) { alertBorderWidth = newWidth; }
function setAlertBorderStyle(newStyle) { alertBorderStyle = newStyle; }
function setAlertBorderColor(newColor) { alertBorderColor = newColor; }
//solid #FF0000'
function getAlertStyle() {
  if (alertStyle != null) return alertStyle;
  return 'border: '+alertBorderWidth+' '+alertBorderStyle+' '+alertBorderColor;
}

function getFormAction() { return formAction; }
function setFormAction(newFormAction) { formAction = newFormAction; }

function toBool(value, nullValue)
{
  if (nullValue === undefined) nullValue = null;
  if (value === true || value === false) return value;
  value = value.toLowerCase();
  value = value.trim();
  if (value.charAt(0) == 'f' || value.charAt(0) == '0') return false;
  if (value.charAt(0) == 't' || value.charAt(0) == '1') return true;
  return nullValue;
}


if (urlParameters.getURLParameter('thickness') != '')
  setLineWidth(urlParameters.getURLParameter('thickness'));
  
if (urlParameters.getURLParameter('sampleCount') != '')
  setSampleCount(urlParameters.getURLParameter('sampleCount'));
  
if (urlParameters.getURLParameter('globalLineWidth') != '')
  setLineWidth(parseFloat(urlParameters.getURLParameter('globalLineWidth')));


  
if (urlParameters.getURLParameter('orientation') != '') {
  orient = urlParameters.getURLParameter('orientation').toLowerCase()
  if (orient == '0') // horizontal
    setHorizontal();
  else if (orient == '1') // vertical
    setVertical();
  else if (orient.charAt(0) == 'h') // horizontal
    setHorizontal();
  else if (orient.charAt(0) == 'v') // horizontal
    setVertical();
}

if (urlParameters.getURLParameter('alertStyle') != '') setAlertStyle(urlParameters.getURLParameter('alertStyle'));
if (urlParameters.getURLParameter('alertBorderWidth') != '') setAlertBorderWidth(urlParameters.getURLParameter('alertBorderWidth'));
if (urlParameters.getURLParameter('alertBorderStyle') != '') setAlertBorderStyle(urlParameters.getURLParameter('alertBorderStyle'));
if (urlParameters.getURLParameter('alertBorderColor') != '') setAlertBorderColor(urlParameters.getURLParameter('alertBorderColor'));

if (urlParameters.getURLParameter('globalWidth') != '' || urlParameters.getURLParameter('globalHeight') != '' || 
    urlParameters.getURLParameter('globalImageHeight') != '' || urlParameters.getURLParameter('globalImageWidth') != '')
   setImageSize('');

if (urlParameters.getURLParameter('globalWidth') != '') {
  if (urlParameters.getURLParameter('globalImageWidth') == '') 
    setImageSize(getImageSize()+' width="'+urlParameters.getURLParameter('globalWidth')+'"');
  setCanvasWidth(urlParameters.getURLParameter('globalWidth'));
}

if (urlParameters.getURLParameter('globalHeight') != '') {
  if (urlParameters.getURLParameter('globalImageHeight') == '') 
    setImageSize(getImageSize()+' height="'+urlParameters.getURLParameter('globalHeight')+'"');
  setCanvasHeight(urlParameters.getURLParameter('globalHeight'));
}

if (urlParameters.getURLParameter('globalImageWidth') != '')
  setImageSize(getImageSize()+' width="'+urlParameters.getURLParameter('globalImageWidth')+'"');
if (urlParameters.getURLParameter('globalImageHeight') != '')
  setImageSize(getImageSize()+' height="'+urlParameters.getURLParameter('globalImageHeight')+'"');


if (urlParameters.getURLParameter('globalCanvasWidth') != '')
  setCanvasWidth(urlParameters.getURLParameter('globalCanvasWidth'));
if (urlParameters.getURLParameter('globalCanvasHeight') != '')
  setCanvasHeight(urlParameters.getURLParameter('globalCanvasHeight'));
if (urlParameters.getURLParameter('globalCanvasSize') != '') {
  setCanvasHeight(urlParameters.getURLParameter('globalCanvasSize'));
  setCanvasWidth(urlParameters.getURLParameter('globalCanvasSize'));
}

if (urlParameters.getURLParameter('submitTo') != '')
  setFormAction(unquote(urlParameters.getURLParameter('submitTo')));
else if (urlParameters.getURLParameter('turkSubmitTo') != '')
  setFormAction(unquote(urlParameters.getURLParameter('turkSubmitTo')) + '/mturk/externalSubmit');
//alert(getFormAction());
//.replace('%3A%2F%2F','://')

/*var row_params = ['numRows', 'num_rows', 'number_of_rows', 'numberOfRows'];
var col_params = ['numCols', 'num_cols', 'number_of_cols', 'numberOfCols',
                  'numColumns', 'num_columns', 'number_of_columns', 'numberOfColumns'];

var has_row_param = false; var has_col_param = false;

for (var i = 0; i < row_params.length; i++) {
  if (urlParameters.getURLParameter(row_params[i]) != '') {
    has_row_param = true;
    setNumRows(parseInt(urlParameters.getURLParameter(row_params[i])));
  }
}

for (var i = 0; i < col_params.length; i++) {
  if (urlParameters.getURLParameter(col_params[i]) != '') {
    has_col_param = true;
    setNumCols(parseInt(urlParameters.getURLParameter(col_params[i])));
  }
}

if (has_row_param && !has_col_param) setNumCols(null);
if (!has_row_param && has_col_param) setNumRows(null);

if (urlParameters.getURLParameter('characterOrder') != '') {
  if (urlParameters.getURLParameter('characterOrder').toLowerCase().charAt(0) == 'r')
    setCharacterOrder(ROWS_FIRST);
  if (urlParameters.getURLParameter('characterOrder').toLowerCase().charAt(0) == 'c')
    setCharacterOrder(COLS_FIRST); 
}*/


setRandomizeOrder(urlParameters.getURLParameter('randomize'));
setCheckAll(urlParameters.getURLParameter('checkAll'));

setAskFeedback(urlParameters.getURLParameter('askFeedback'));
setAskInputDevice(urlParameters.getURLParameter('askInputDevice'));
setAskSeenBefore(urlParameters.getURLParameter('askSeenBefore'));
