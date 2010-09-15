var refcounter = {};

(function () {
  var counters = {};
  var counterChangeEvents = {};
  refcounter.setCounter = function (counter, value) {
    counters[counter] = value;
    if (counterChangeEvents[counter]) {
      var len = counterChangeEvents[counter].length;
      for (var i = 0; i < len; i++) {
        counterChangeEvents[counter][i](value, counter);
      }
    }
  };
  refcounter.initCounter = function (counter, value) {
    if (value === undefined) value = 0;
    refcounter.setCounter(counter, value);
  };
  
  refcounter.getCount = function (counter, defaultValue) {
    if (counters[counter] !== undefined) return counters[counter];
    return defaultValue;
  };

  refcounter.incrementCounter = function (counter) {
    refcounter.setCounter(counter, refcounter.getCount(counter, 0) + 1);
  };

  refcounter.decrementCounter = function (counter) {
    refcounter.setCounter(counter, refcounter.getCount(counter, 0) + 1);
  };
  
  refcounter.handleCounterChange = function (counter, func) {
    if (!counterChangeEvents[counter]) counterChangeEvents[counter] = [];
    counterChangeEvents[counter].push(func);
  };
  
  refcounter.handleCounterZero = function (counter, func) {
    var newFunc = function (value) {
      if (value == 0)
        return func.apply(this, newFunc.arguments);
    };
    refcounter.handleCounterChange(counter, newFunc);
})();