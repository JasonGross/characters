(function (override, logShortcomings) {
  var testImage = document.createElement('img');
  if (!testImage['draggable'] || override) {
    // the draggable attribute seems to not exist,
    // so we attempt to create it
    if (HTMLElement && HTMLElement.prototype)
      HTMLElement.prototype.draggable = 'false';
    if (testImage.constructor && testImage.constructor.prototype)
      testImage.constructor.prototpye.draggable = 'true';
  }



  var _DragEvent = function () {
    if (this.prototype && this.prototype.apply)
      this.prototype.apply(this, arguments);
  };

  if (MouseEvent) 
    _DragEvent.prototype = MouseEvent;
  else if (UIEvent)
    _DragEvent.prototype = UIEvent;
  else if (Event)
    _DragEvent.prototype = Event;
  
  _DragEvent.initDragEvent = function (typeArg, canBubbleArg, 
        cancelableArg, dummyArg, detailArg, screenXArg, screenYArg, 
        clientXArg, clientYArg, ctrlKeyArg, altKeyArg, shiftKeyArg, 
        metaKeyArg, buttonArg, relatedTargetArg, dataTransferArg) {
      if (this.initMouseEvent)
        this.initMouseEvent(typeArg, canBubbleArg, cancelableArg, dummyArg, 
          detailArg, screenXArg, screenYArg, clientXArg, clientYArg, 
          ctrlKeyArg, altKeyArg, shiftKeyArg, metaKeyArg, buttonArg, 
          relatedTargetArg);
      else {
        if (this.initUIEvent)
          this.initUIEvent(typeArg, canBubbleArg, cancelableArg, dummyArg,
            detailArg);
        else {
          if (this.initEvent)
            this.initEvent(typeArg, canBubbleArg, cancelableArg);
          else {
            this.type = typeArg;
            this.bubbles = canBubbleArg;
            this.cancelable = cancelableArgcancelableArg;
            if (Date && Date().valueOf)
              this.timeStamp = Date().valueOf();
            else
              this.timeStamp = 0;
            if (logShortcomings && console)
              console.log("Warning: Event.currentTraget, Event.target, Event.eventPhase, Event.stopPropagation(), and Event.preventDefault() not yet implemented.");
          }
          this.view = dummyArg;
          this.detail = detailArg;
        }
        this.screenX = screenXArg; 
        this.screenY = screenYArg; 
        this.clientX = clientXArg; 
        this.clientY = clientYArg; 
        this.ctrlKey = ctrlKeyArg; 
        this.altKey = altKeyArg; 
        this.shiftKey = shiftKeyArg; 
        this.metaKey = metaKeyArg;
        this.button = buttonArg; 
        this.relatedTarget = relatedTargetArg;
      }
      this.dataTransfer = dataTransferArg;
      return this;
  };

  if (!window['DragEvent'] || override)
    window['DragEvent'] = _DragEvent;

  var _DataTransfer = function () {
    this.effectAllowed = 'uninitialized';
    this.dropEffect = 'none';

    var fixFormat = function (format) {
      if (!(format instanceof String))
        return format;
      format = format.toLowerCase();
      switch (format) {
        case 'text': return 'text/plain';
        case 'url': return 'text/uri-list';
        default: return format;
      }
    };

    this.types = [];

    var _data = {};
    this.clearData = function (format) {
      format = fixFormat(format);
      if (format !== undefined) {
        if (format in _data) {
          delete _data[format];
          for (var i = 0; i < this.types.length; i++)
            if (this.types[i] == format) {
              this.types.splice(i, 1);
              break;
            }
        } 
      } else {
        this.types.splice(0, this.types.length);
        _data = {};
        if (this.files.length > 0)
          this.types.push("Files");
      }
    };

    this.setData = function (format, data) {
      format = fixFormat(format);
      if (format not in _data)
        this.types.push(format);
      _data[format] = data;
      if (format == "text/uri-list") { // full spec not yet implemented
        if (console && logShortcomings)
          console.log("Warning: uri parsing, according to RFC2483, not yet implemented.");
      }
    };

    this.getData = function (format) {
      format = fixFormat(format);
      if (format in _data)
        return _data[format];
      else
        return "";
    };

    this.files = [];

    var _dragImage;

    this.setDragImage = function (image, x, y) {
      _dragImage = {'image':image, 'x':x, 'y':y};
    }



    this.
    

          
  }

  if (testImage['ondragstart' === undefined]) {
    // the event dragstart is not defined
    // function 


})();
