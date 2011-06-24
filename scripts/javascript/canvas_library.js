var DrawingCanvas;
(function (defaultLineWidth, defaultLineCap, $, jQuery, undefined) {
  DrawingCanvas = function (name, width, height, canvasLinewidth, canvasLineCap, canvas, onRedraw, drawAtPoint) {
    if (canvasLineWidth === undefined) canvasLineWidth = defaultLineWidth;
    if (canvasLineCap === undefined) canvasLineCap = defaultLineCap;
    var self = this;
    this.name = name;
    this.tag = tag;
    if (canvas === undefined)
      canvas = "<canvas>Your browser must support the &lt;canvas&gt; element in order to use this site.</canvas>";
    this.canvas = $(canvas)
      .attr('id', name)
      .attr('unselectable', 'on')
      .width(width)
      .height(height);
    var clearLink = $('<a/>')
      .attr('id', 'clear')
      .attr('href', '#')
      .append('clear')
      .click(function () { self.clear() });
    var undoLink = $('<a/>')
      .attr('id', 'undo')
      .attr('href', '#')
      .append('undo')
      .click(function () { self.undo() });
    var redoLink = $('<a/>')
      .attr('id', 'redo')
      .attr('href', '#')
      .append('redo')
      .click(function () { self.redo() });
    var _image = $('<input/>')
      .attr('type', 'hidden')
      .attr('name', name + '_image')
      .attr('id', name + '_image');
    var _stroke = $('<input/>')
      .attr('type', 'hidden')
      .attr('name', name + '_stroke')
      .attr('id', name + '_stroke');
    this.DOMElement = $('<div/>')
      .append(_image)
      .append(_stroke)
      .append($('<div/>')
                .attr('id', name + '_div')
                .append(this.canvas))
      .append($('<div/>')
                .attr('id', 'canvascontrols')
                .append(_clear)
                .append(_undo)
                .append(_redo));

    var ctx = canvas.get(0).getContext('2d');

    var drawStart, drawStroke, drawEnd;

    (function (ctx) {
      var isDrawing = false;

      drawStart = function (x, y) {
        ctx.fillRect(x-ctx.lineWidth/2, y-ctx.lineWidth/2, ctx.lineWidth, ctx.lineWidth);
        ctx.beginPath();
        ctx.moveTo(x, y);
        isDrawing = true;
      };

      drawStroke = function (x, y, force) {
        if (isDrawing) {
          ctx.lineTo(x, y);
          ctx.stroke();
        } else if (force) {
          drawStart(x, y);
        }
        return isDrawing;
      };

      drawEnd = function () {
        isDrawing = false;
      };
    })(ctx);


    this.paintWithStroke = function (strokes, lineWidth, lineCap) {
      if (lineWidth === undefined) lineWidth = canvasLineWidth;
      if (lineCap === undefined) lineCap = canvasLineCap;

      ctx.lineWidth = lineWidth;
      ctx.lineCap = lineCap;

      ctx.strokeStyle = "rgb(0, 0, 0)";
      ctx.clearRect(0, 0, canvas.width(), canvas.height());
      if (onRedraw !== undefined) onRedraw(ctx);

      for (var stroke_i = 0; stroke_i < strokes.length; stroke_i++) {
        var x = strokes[stroke_i][0].x; var y = strokes[stroke_i][0].y;

        if (drawAtPoint === undefined || drawAtPoint(x, y))
          drawStart(x, y);

        for (point_i = 0; point_i < strokes[stroke_i].length; point_i++) {
          point = strokes[stroke_i][point_i];
          x = point.x; y = point.y;
          if (drawAtPoint === undefined || drawAtPoint(x, y)) {
            drawStroke(x, y, true);
          } else {
            drawEnd();
          }
        }
      }
    };

    var strokes = {};

    function makeCanvasMemoryful(strokes_name) {
      if (strokes_name === undefined) strokes_name = 'strokes';
      future_strokes_name = 'future_' + strokes_name;
      strokes[future_strokes_name] = [];

      self.canUndo = function () { return strokes[strokes_name].length > 0; };
      self.canRedo = function () { return strokes[future_strokes_name].length > 0; };

      self.undo = function () {
        if (!self.canUndo()) throw 'Error: Attempt to undo canvas ' + canvas + ' failed; no state to undo.';
        strokes[future_strokes_name].push(strokes[strokes_name].pop());
        self.paintWithStroke(strokes[strokes_name]);
        if (strokes[strokes_name].length == 0 && disableUndo !== undefined) disableUndo();
        if (enableRedo !== undefined) enableRedo();
      };

      self.redo = function () {
        if (!self.canRedo()) throw 'Error: Attempt to redo canvas ' + canvas + ' failed; no state to redo.';
        strokes[strokes_name].push(strokes[future_strokes_name].pop());
        self.paintWithStroke(strokes[strokes_name]);
        if (strokes[future_strokes_name].length == 0 && disableRedo !== undefined) disableRedo();
        if (enableUndo !== undefined) enableUndo();
      };

      self.clearFuture = function () {
        strokes[future_strokes_name] = [];
        if (disableRedo !== undefined) disableRedo();
      };

      self.clearPast = function () {
        strokes[strokes_name] = [];
        if (disableUndo !== undefined) disableUndo();
      };

      self.clearState = function () {
        self.clearFuture();
        self.clearPast();
      };
    }



    //===================================================================
    //Canvas Drawing - From http://detexify.kirelabs.org/js/canvassify.js
    // make a canvas drawable and give the stroke to some function after each stroke
    // better canvas.drawable({start: startcallback, stop: stopcallback, stroke: strokecallback})
    //function makeDrawable(canvas, lineWidth, undoLink, redoLink) {
    (function (ctx, canvasLineWidth, canvasLineCap, strokesDict, strokesKey) {
      // Initilize canvas context values
      ctx.lineWidth = canvasLineWidth;
      ctx.lineCap = canvasLineCap;
      //end initilization
      var is_stroking = false;
      var has_drawn = false;
      var current_stroke;
      strokesDict[strokesKey] = [];
      function point(x, y) {
        return {"x":x, "y":y, "t": (new Date()).getTime()};
      }

      function start(evt) {
        is_stroking = true;
        var coords = getMouseCoordsWithinTarget(evt);
        has_drawn = (drawAtPoint === undefined || drawAtPoint(coords.x, coords.y));
        if (has_drawn)
          drawStart(coords.x, coords.y);
        current_stroke = [point(coords.x, coords.y)];
        // initialize new stroke
      }

      function stroke(evt) {
        if (is_stroking) {
          var coords = getMouseCoordsWithinTarget(evt);
          if (drawAtPoint === undefined || drawAtPoint(coords.x, coords.y))
            has_drawn = drawStroke(coords.x, coords.y) || has_drawn; // drawStroke returns true if we actually draw this stroke.  reverse the order to make it so drawStroke is always called.
          current_stroke.push(point(coords.x, coords.y));
        }
      }

      function stop(evt) {
        drawEnd();
        if (is_stroking && has_drawn) {
          strokesDict[strokesKey].push(current_stroke);
          self.clearFuture();
          if (enableUndo !== undefined) enableUndo();
        }
        is_stroking = false;
      }
    })(ctx, canvasLineWidth, canvasLineCap, strokes, 'strokes');
    
    // canvas addons
    makeCanvasMemoryful('strokes');

    self.clear = function() {
      self.clearState();
      ctx.strokeStyle = "rgb(0, 0, 0)";
      ctx.clearRect(0, 0, canvas.width(), canvas.height());
    }
    self.clear();
    canvas
      .mousedown(start)
      .mousemove(stroke)
      .mouseup(stop)
      .mouseout(stop);

    function styleDisableLink(link, name) {
      link
        .css({
             'color':'gray',
             'background':'url(../images/'+name+'-gray.png) no-repeat 2px 1px'
             });
    }
    function styleEnableLink(link, name) {
      link
        .css({
             'color':'blue',
             'background':'url(../images/'+name+'.png) no-repeat 2px 1px'
             });
    }

    var self_undo = self.undo;
    var self_redo = self.redo;
    
    if (undoLink !== undefined) {
      disableUndo = function () {
        styleDisableLink(undoLink, 'undo');
        self.undo = function () { return false; };
      };
      enableUndo = function () {
        styleEnableLink(undoLink, 'undo');
        self.undo = self_undo;
      };
    }

    if (redoLink !== undefined) {
      disableRedo = function () {
        styleDisableLink(redoLink, 'redo');
        self.redo = function () { return false; };
      };
      enableRedo = function () {
        styleEnableLink(redoLink, 'redo');
        self.redo = self_redo;
      };
    }
    //===================================================================


    //===================================================================
    //From http://skuld.bmsc.washington.edu/~merritt/gnuplot/canvas_demos/
    function getMouseCoordsWithinTarget(event) {
      var coords = {x: 0, y: 0};

      if (!event) { // then we're in a non-DOM (probably IE) browser
        event = window.event;
        if (event) {
          coords.x = event.offsetX;
          coords.y = event.offsetY;
        }
      } else {		// we assume DOM modeled javascript
        var Element = event.target;
        var CalculatedTotalOffsetLeft = 0;
        var CalculatedTotalOffsetTop = 0;

        while (Element.offsetParent) {
          CalculatedTotalOffsetLeft += Element.offsetLeft;
          CalculatedTotalOffsetTop += Element.offsetTop;
          Element = Element.offsetParent;
        }

        coords.x = event.pageX - CalculatedTotalOffsetLeft;
        coords.y = event.pageY - CalculatedTotalOffsetTop;
      }

      return coords;
    }
    //===================================================================

    self.strokesToString = function (extraDelimiter) {
      if (extraDelimiter === undefined) extraDelimiter = '';
      var cur_stroke;
      var rtn = '[';
      for (var j = 0; j < strokes.strokes.length; j++) {
        rtn += '[';
        cur_stroke = strokes.strokes[j];
        for (var k = 0; k < cur_stroke.length; k++) {
          rtn += "{'x':" + cur_stroke[k].x + ",'y':" + cur_stroke[k].y + ",'t':" + cur_stroke[k].t + '}'
            rtn += (k + 1 == cur_stroke.length ? '' : ','+extraDelimiter);
        }
        rtn += ']' + (j + 1 == strokes.length ? '' : ','+extraDelimiter);
      }
      return rtn + ']';
    };

    return this;
  };

})(getLineWidth(), getLineCap(), jQuery, jQuery);


















































//===================================================================
//===================== DEPRECATED ==================================

function paintCanvasWithStroke(canvas, strokes, lineWidth, lineCap) {
  var ctx = canvas.getContext('2d');
  
  if (lineWidth !== undefined) ctx.lineWidth = lineWidth;
  if (lineCap === undefined) lineCap = getLineCap();
  ctx.lineCap = lineCap;
  
  ctx.strokeStyle = "rgb(0, 0, 0)";
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (var stroke_i = 0; stroke_i < strokes.length; stroke_i++) {
    var x = strokes[stroke_i][0].x; var y = strokes[stroke_i][0].y;
    
    ctx.fillRect(x-ctx.lineWidth/2, y-ctx.lineWidth/2, ctx.lineWidth, ctx.lineWidth);
    ctx.beginPath();
    ctx.moveTo(x, y);
    
    for (point_i = 0; point_i < strokes[stroke_i].length; point_i++) {
      point = strokes[stroke_i][point_i];
      last_x = x; last_y = y;
      x = point.x; y = point.y;
      ctx.lineTo(x, y);
      ctx.stroke();
    }    
  }
}

function makeCanvasMemoryful(canvas, strokes_name) {
  if (strokes_name === undefined) strokes_name = 'strokes';
  canvas.futureStrokes = [];
  
  canvas.canUndo = function () { return canvas[strokes_name].length > 0; };
  canvas.canRedo = function () { return canvas.futureStrokes.length > 0; };
  
  canvas.undo = function () {
    if (!canvas.canUndo()) throw 'Error: Attempt to undo canvas ' + canvas + ' failed; no state to undo.';
    canvas.futureStrokes.push(canvas[strokes_name].pop());
    paintCanvasWithStroke(canvas, canvas[strokes_name]);
    if (canvas[strokes_name].length == 0 && !(canvas.disableUndo === undefined)) canvas.disableUndo();
    if (!(canvas.enableRedo === undefined)) canvas.enableRedo();
  };
  
  canvas.redo = function () {
    if (!canvas.canRedo()) throw 'Error: Attempt to redo canvas ' + canvas + ' failed; no state to redo.';
    canvas[strokes_name].push(canvas.futureStrokes.pop());
    paintCanvasWithStroke(canvas, canvas[strokes_name]);
    if (canvas.futureStrokes.length == 0 && !(canvas.disableRedo === undefined)) canvas.disableRedo();
    if (!(canvas.enableUndo === undefined)) canvas.enableUndo();
  };
  
  canvas.clearFuture = function () {
    canvas.futureStrokes = [];
    if (!(canvas.disableRedo === undefined)) canvas.disableRedo();
  };
  
  canvas.clearPast = function () {
    canvas[strokes_name] = [];
    if (!(canvas.disableUndo === undefined)) canvas.disableUndo();
  };

  canvas.clearState = function () {
    canvas.clearFuture();
    canvas.clearPast();
  };
}

//===================================================================
//Canvas Drawing - From http://detexify.kirelabs.org/js/canvassify.js
// make a canvas drawable and give the stroke to some function after each stroke
// better canvas.drawable({start: startcallback, stop: stopcallback, stroke: strokecallback})
function makeDrawable(canvas, lineWidth, undoLink, redoLink) {
  var ctx = canvas.getContext('2d');
  // Initilize canvas context values
  if (lineWidth === undefined) lineWidth = getLineWidth();
  ctx.lineWidth = lineWidth;
  ctx.lineCap = getLineCap();
  //end initilization
  var draw = false;
  var current_stroke;
  canvas.strokes = [];
  var point = function(x,y) {
    return {"x":x, "y":y, "t": (new Date()).getTime()};
  }
  var start = function(evt) {
    draw = true;
    var x,y;
    var coords = getMouseCoordsWithinTarget(evt);
    x = coords.x;
    y = coords.y;
    ctx.fillRect(x-ctx.lineWidth/2, y-ctx.lineWidth/2, ctx.lineWidth, ctx.lineWidth);
    ctx.beginPath();
    ctx.moveTo(x, y);
    current_stroke = [point(x,y)];
  // initialize new stroke
  }
  var stroke = function(evt) {
    if (draw) {
      var coords = getMouseCoordsWithinTarget(evt);
      ctx.lineTo(coords.x, coords.y);
      ctx.stroke();
      current_stroke.push(point(coords.x, coords.y));
    }
  }
  var stop = function(evt) {
    if (draw) {
      canvas.strokes.push(current_stroke);
      draw = false;
      canvas.clearFuture();
      if (!(canvas.enableUndo === undefined)) canvas.enableUndo();
    }
  }
  // canvas addons
  makeCanvasMemoryful(canvas, 'strokes');

  canvas.clear = function() {
    canvas.clearState();
    ctx.strokeStyle = "rgb(0, 0, 0)";
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
  canvas.clear();
  // addeventlistener
  canvas.onmousedown = function(evt) {start(evt);};
  canvas.onmousemove = function(evt) {stroke(evt);};
  canvas.onmouseup = function(evt) {stop(evt);};
  canvas.onmouseout = function(evt) {stop(evt);};
  
  if (undoLink !== undefined) {
    canvas.disableUndo = function () { 
      undoLink.style.color = 'gray'; 
      undoLink.style.background = 'url(undo-gray.png) no-repeat 2px 1px'; 
      undoLink.onclick = function () {return false;};
    };
    canvas.enableUndo = function () {
      undoLink.style.color = 'blue'; 
      undoLink.style.background = 'url(undo.png) no-repeat 2px 1px'; 
      undoLink.onclick = function () {return true;};
    };
  }
  
  if (!(redoLink === undefined)) {
    canvas.disableRedo = function () { 
      redoLink.style.color = 'gray';
       redoLink.style.background = 'url(redo-gray.png) no-repeat 2px 1px'; 
       redoLink.onclick = function () {return false;};
     };
    canvas.enableRedo = function () { 
      redoLink.style.color = 'blue'; 
      redoLink.style.background = 'url(redo.png) no-repeat 2px 1px'; 
      redoLink.onclick = function () {return true;};
    };
  }
  
  //canvas.init();
  return canvas;  
}
//===================================================================


//===================================================================
//From http://skuld.bmsc.washington.edu/~merritt/gnuplot/canvas_demos/
function getMouseCoordsWithinTarget(event)
{
	var coords = { x: 0, y: 0};

	if(!event) // then we're in a non-DOM (probably IE) browser
	{
		event = window.event;
		if (event) {
			coords.x = event.offsetX;
			coords.y = event.offsetY;
		}
	}
	else		// we assume DOM modeled javascript
	{
		var Element = event.target ;
		var CalculatedTotalOffsetLeft = 0;
		var CalculatedTotalOffsetTop = 0 ;

		while (Element.offsetParent)
 		{
 			CalculatedTotalOffsetLeft += Element.offsetLeft ;     
			CalculatedTotalOffsetTop += Element.offsetTop ;
 			Element = Element.offsetParent ;
 		}

		coords.x = event.pageX - CalculatedTotalOffsetLeft ;
		coords.y = event.pageY - CalculatedTotalOffsetTop ;
	}

	return coords;
}
//===================================================================



function strokesToString(strokes, extraDelimiter)
{
  if (extraDelimiter === undefined) extraDelimiter = '';
  var cur_stroke;
  var rtn = '[';
  for (var j = 0; j < strokes.length; j++) {
    rtn += '[';
    cur_stroke = strokes[j];
    for (var k = 0; k < cur_stroke.length; k++) {
      rtn += "{'x':" + cur_stroke[k].x + ",'y':" + cur_stroke[k].y + ",'t':" + cur_stroke[k].t + '}'
      rtn += (k + 1 == cur_stroke.length ? '' : ','+extraDelimiter);
    }
    rtn += ']' + (j + 1 == strokes.length ? '' : ','+extraDelimiter);
  }
  return rtn + ']';
}
