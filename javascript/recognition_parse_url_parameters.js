var urlParameters = new (function () {
  var intURLParameters = ['numberOfTasks',
                          'trainingImagesPerTask',
                          'testImagesPerTask',
                          'distractorsPerTask',
                          'sameAlphabetDistractorsPerTask',
                          'otherAlphabetDistractorsPerTask'];
  var floatURLParameters = ['sameAlphabetDistractorDensity',
                            'otherAlphabetDistractorDensity',
                            'distractorDensity'];
  var boolURLParameters = ['distinctTaskAlphabets'];
  var validURLParameters = intURLParameters.concat(boolURLParameters, floatURLParameters,
                            ['alertStyle',
                             'alertBorderWidth',
                             'alertBorderColor',
                             'alertBorderStyle']);
  //==========================================================
  //Constants
  var IGNORE_CASE = true;
  var EPSILON = 0.05;
  //End Constants
  //==========================================================
  //Change default values here
  this.numberOfTasks = 5;
  this.trainingImagesPerTask = 1;
  this.testImagesPerTask = 10;
  var defaultDistractorsPerTask = 5;
  var defaultSameAlphabetDistractorDensity = 3.0 / defaultDistractorsPerTask;
  var defaultOtherAlphabetDistractorDensity = 1.0 - defaultSameAlphabetDistractorDensity;
  this.distinctTaskAlphabets = false;
  //var imageWidth = 75;
  //var imageHeight = 75;
  this.alertStyle = null;
  this.alertBorderWidth = 'thick';
  this.alertBorderColor = 'red';
  this.alertBorderStyle = 'solid';
  //End default values
  //==========================================================
  var urlParameterObject = this;
  jQuery.each(validURLParameters, function (index, urlParameter) {
      if (hasURLParameter(urlParameter))
        urlParameterObject[urlParameter] = getURLParameter(urlParameter, IGNORE_CASE, null);
    });
  
  jQuery.each(intURLParameters, function (index, urlParameter) {
      if (urlParameter in this)
        this[urlParameter] = parseInt(urlParameter);
    });
  
  jQuery.each(floatURLParameters, function (index, urlParameter) {
      if (urlParameter in this)
        this[urlParameter] = parseFloat(urlParameter);
    });
  
  jQuery.each(boolURLParameters, function (index, urlParameter) {
      if (urlParameter in this)
        this[urlParameter] = toBool(urlParameter, true);
    });
  
  // Calculating values from various ways of specifying things.
  // I assume that either both are densities, or both are numbers.  The output is otherwise not specified.
  
  // check for some unimplemented states
  if (('sameAlphabetDistractorsPerTask' in this || 'otherAlphabetDistractorsPerTask' in this) &&
      ('sameAlphabetDistractorDensity' in this || 'otherAlphabetDistractorDensity' in this))
    throw 'You are not allowed to specify both a density and a number for the distractors for a given task.';
  
  if (('sameAlphabetDistractorsPerTask' in this) && ('otherAlphabetDistractorsPerTask' in this) && !('distractorsPerTask' in this))
    this.distractorsPerTask = this.sameAlphabetDistractorsPerTask + this.otherAlphabetDistractorsPerTask;
  else if (('sameAlphabetDistractorsPerTask' in this) && !('otherAlphabetDistractorsPerTask' in this) && ('distractorsPerTask' in this))
    this.otherAlphabetDistractorsPerTask = this.distractorsPerTask - this.sameAlphabetDistractorsPerTask;
  else if (!('sameAlphabetDistractorsPerTask' in this) && ('otherAlphabetDistractorsPerTask' in this) && ('distractorsPerTask' in this))
    this.sameAlphabetDistractorsPerTask = this.distractorsPerTask - this.otherAlphabetDistractorsPerTask;
  
  if ('distractorDensity' in this) this.distractorsPerTask = Math.round(this.distractorDensity * this.testImagesPerTask);
  else if (!('distractorsPerTask' in this)) this.distractorsPerTask = defaultDistractorsPerTask;
  
  
  if (('sameAlphabetDistractorDensity' in this) && !('otherAlphabetDistractorDensity' in this))
    this.otherAlphabetDistractorDensity = 1.0 - this.sameAlphabetDistractorDensity;
  else if (!('sameAlphabetDistractorDensity' in this) && ('otherAlphabetDistractorDensity' in this))
    this.sameAlphabetDistractorDensity = 1.0 - this.otherAlphabetDistractorDensity;
  else if (!('sameAlphabetDistractorsPerTask' in this || 'otherAlphabetDistractorsPerTask' in this ||
             'sameAlphabetDistractorDensity' in this || 'otherAlphabetDistractorDensity' in this)) {
    this.sameAlphabetDistractorDensity = defaultSameAlphabetDistractorDensity;
    this.otherAlphabetDistractorDensity = defaultOtherAlphabetDistractorDensity;
  }

  if ('sameAlphabetDistractorsPerTask' in this)
    this.sameAlphabetDistractorDensity = this.sameAlphabetDistractorsPerTask / this.distractorsPerTask;
  else if ('sameAlphabetDistractorDensity' in this)
    this.sameAlphabetDistractorsPerTask = this.distractorsPerTask * this.sameAlphabetDistractorDensity;

  if ('otherAlphabetDistractorsPerTask' in this)
    this.otherAlphabetDistractorDensity = this.otherAlphabetDistractorsPerTask / this.distractorsPerTask;
  else if ('otherAlphabetDistractorDensity' in this)
    this.otherAlphabetDistractorsPerTask = this.distractorsPerTask * this.otherAlphabetDistractorDensity;
  
      
    
  if (this.distractorsPerTask != this.sameAlphabetDistractorsPerTask + this.otherAlphabetDistractorsPerTask)
    throw "You can't do math!  The number of distractors in a task should be the sum of the distractors from the same alphabet, and the distractors from the other alphabets.";
})();