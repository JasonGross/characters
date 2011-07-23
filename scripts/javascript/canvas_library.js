var DrawingCanvas;
(function (defaultLineWidth, defaultLineCap, $, jQuery, undefined) {
  DrawingCanvas = function DrawingCanvas(name, width, height, canvasLineWidth, canvasLineCap, canvas, onRedraw, drawAtPoint, interpolate) {
    if (canvasLineWidth === undefined) canvasLineWidth = defaultLineWidth;
    if (canvasLineCap === undefined) canvasLineCap = defaultLineCap;
    var self = this;
    this.name = name;
    width = parseInt(width); height = parseInt(height);
    if (canvas === undefined)
      canvas = "<canvas>Your browser must support the &lt;canvas&gt; element in order to use this site.</canvas>";
    this.canvas = canvas = $(canvas)
      .attr('id', name)
      .attr('unselectable', 'on')
      .attr('width', width)
      .attr('height', height);
    var clearLink = $('<a/>')
      .attr('id', 'clear')
      .attr('href', '#')
      .append('clear')
      .click(function () { self.clear() });
    var undoLink = $('<a/>')
      .attr('id', 'undo')
      .attr('href', '#')
//      .append('undo')
      .click(function () { self.undo() });
    var redoLink = $('<a/>')
      .attr('id', 'redo')
      .attr('href', '#')
//      .append('redo')
      .click(function () { self.redo() });
    this.DOMElement = $('<div/>')
      .append($('<div/>')
                .attr('id', name + '_div')
                .append(this.canvas))
      .append($('<div/>')
                .attr('id', 'canvascontrols')
                .append(clearLink)
                .append(undoLink)
                .append(redoLink));

    (function events() {
      var events = {'dirty':[], 'dirtyImage':[]};
      jQuery.each(events, function (key) {
          self[key] = function (handler) {
            if (handler === undefined) {
              var len = events[key].length;
              for (var i = 0; i < len; i++) {
                events[key][i]();
              }
            } else {
              events[key].push(handler);
            }
          };
          self[key].name = key;
        });
    })();
    self.dirtyImage(self.dirty);

    var ctx = canvas[0].getContext('2d');

    var drawStroke, drawEnd, clearDrawing;
    (function drawing(ctx) {
      var isDrawing = false;
      var lastPt = undefined;

      drawStroke = function drawStroke(x, y, force) {
        if (drawAtPoint === undefined || drawAtPoint(x, y) || force) {
          if (isDrawing) {
            ctx.lineTo(x, y);
            ctx.stroke();
          } else {
            ctx.fillRect(x-ctx.lineWidth/2, y-ctx.lineWidth/2, ctx.lineWidth, ctx.lineWidth);
            ctx.beginPath();
            ctx.moveTo(x, y);
            isDrawing = true;
          }
          lastPt = {'x':x, 'y':y};
        } else if (isDrawing) {
          isDrawing = false;
          if (lastPt !== undefined && interpolate) {
            var pt = interpolate(lastPt.x, lastPt.y, x, y);
            if (pt !== undefined) {
              ctx.lineTo(pt.x, pt.y);
              ctx.stroke();
            }
          }
        }
        lastPt = {'x': x, 'y': y};
        return isDrawing;
      };

      drawEnd = function drawEnd() {
        isDrawing = false;
        lastPt = undefined;
      };

      clearDrawing = function clearDrawing(lineWidth, lineCap) {
        if (lineWidth === undefined) lineWidth = canvasLineWidth;
        if (lineCap === undefined) lineCap = canvasLineCap;
        
        ctx.lineWidth = lineWidth;
        ctx.lineCap = lineCap;

        ctx.strokeStyle = "rgb(0, 0, 0)";
        ctx.clearRect(0, 0, canvas.width(), canvas.height());
        if (onRedraw !== undefined) onRedraw(ctx);
      };

      self.paintWithStroke = function (strokes, lineWidth, lineCap) {
        clearDrawing(lineWidth, lineCap);

        for (var stroke_i = 0; stroke_i < strokes.length; stroke_i++) {
          for (var point_i = 0; point_i < strokes[stroke_i].length; point_i++) {
            var point = strokes[stroke_i][point_i];
            drawStroke(point.x, point.y);
          }
          drawEnd();
        }
      };

      self.dirtyImage(function () { self.paintWithStroke(self.getStrokes()); });
    })(ctx);


    var pushStroke;
    (function makeCanvasMemoryful() {
      var strokes = [];
      var future_strokes = [];

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

      function disableUndo() { styleDisableLink(undoLink, 'undo'); }
      function enableUndo() { styleEnableLink(undoLink, 'undo'); }
      function disableRedo() { styleDisableLink(redoLink, 'redo'); }
      function enableRedo() { styleEnableLink(redoLink, 'redo'); }

      function dirtyDoButtons() {
        if (self.canUndo())
          enableUndo();
        else
          disableUndo();
        if (self.canRedo())
          enableRedo();
        else
          disableRedo();
      }
      self.dirty(dirtyDoButtons);

      self.canUndo = function canUndo() { return strokes.length > 0; };
      self.canRedo = function canRedo() { return future_strokes.length > 0; };      

      self.undo = function undo() {
        if (!self.canUndo()) throw 'Error: Attempt to undo canvas ' + canvas + ' failed; no state to undo.';
        future_strokes.push(strokes.pop());
        self.dirtyImage();
      }

      self.redo = function redo() {
        if (!self.canRedo()) throw 'Error: Attempt to redo canvas ' + canvas + ' failed; no state to redo.';
        strokes.push(future_strokes.pop());
        self.dirtyImage();
      };

      self.clearFuture = function clearFuture() {
        future_strokes = [];
        self.dirty();
      };

      self.clearPast = function clearPast() {
        strokes = [];
        self.dirty();
      };

      self.clearState = function clearState() {
        self.clearFuture();
        self.clearPast();
      };

      self.getStrokes = function getStrokes() {
        return strokes.slice(0);
      };

      pushStroke = function pushStroke(stroke) {
        strokes.push(stroke);
        self.dirty();
      };
    })();



      

    //===================================================================
    //Canvas Drawing - From http://detexify.kirelabs.org/js/canvassify.js
    // make a canvas drawable and give the stroke to some function after each stroke
    // better canvas.drawable({start: startcallback, stop: stopcallback, stroke: strokecallback})
    //function makeDrawable(canvas, lineWidth, undoLink, redoLink) {
    (function (ctx, canvasLineWidth, canvasLineCap) {
      // Initilize canvas context values
      ctx.lineWidth = canvasLineWidth;
      ctx.lineCap = canvasLineCap;
      //end initilization
      var is_stroking = false;
      var has_drawn = false;
      var current_stroke;
      function point(x, y) {
        return {"x":x, "y":y, "t": (new Date()).getTime()};
      }

      var start = function start(evt) {
        is_stroking = true;
        var coords = getMouseCoordsWithinTarget(evt);
        has_drawn = drawStroke(coords.x, coords.y);
        current_stroke = [point(coords.x, coords.y)];
        // initialize new stroke
      };

      var stroke = function stroke(evt) {
        if (is_stroking) {
          var coords = getMouseCoordsWithinTarget(evt);
          has_drawn = drawStroke(coords.x, coords.y) || has_drawn; // drawStroke returns true if we actually draw this stroke.  reverse the order to make it so drawStroke is always called.
          current_stroke.push(point(coords.x, coords.y));
        }
      };

      var stop = function stop(evt) {
        drawEnd();
        if (is_stroking && has_drawn) {
          pushStroke(current_stroke);
          self.clearFuture();
        }
        is_stroking = false;
      };
    
      canvas
        .mousedown(start)
        .mousemove(stroke)
        .mouseup(stop)
        .mouseout(stop);
    })(ctx, canvasLineWidth, canvasLineCap);
    
    self.clear = function clear(doRedraw) {
      self.clearState(doRedraw);
      ctx.strokeStyle = "rgb(0, 0, 0)";
      ctx.clearRect(0, 0, canvas.width(), canvas.height());
      if (doRedraw || doRedraw === undefined)
        onRedraw(ctx);
    }
    self.clear(false);

    //===================================================================


    this.getImage = function getImage() {
      return canvas[0].toDataURL();
    };

    this.strokesToString = function (extraDelimiter) {
      if (extraDelimiter === undefined) extraDelimiter = '';
      var cur_stroke;
      var rtn = '[';
      var strokes = self.getStrokes();
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
    };

    this.height = function height() { return self.canvas.height(); };
    this.width = function width() { return self.canvas.width(); };

    return this;
  };

})(5, 'butt', jQuery, jQuery);


















































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
