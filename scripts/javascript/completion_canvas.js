var CompletionCanvas;
(function ($, jQuery, undefined) {
  CompletionCanvas = function CompletionCanvas(name, width, height, image, showImageHalf, canvasLinewidth, canvasLineCap, canvas) {
    var self = this;
    
    var halfWidth, halfHeigh;
    var halfImage;
    var drawAtPoint, onRedraw;
    var interpolate;

    function makeInterpolate(interpolateOrdered) {
      var interpolate = function interpolate(x1, y1, x2, y2) {
        if ((drawAtPoint(x1, y1) && drawAtPoint(x2, y2)) ||
            (!drawAtPoint(x1, y1) && !drawAtPoint(x2, y2)))
          return undefined;
        if (!drawAtPoint(x1, y1))
          return interpolate(x2, y2, x1, y1);
        var m = (y2 - y1) / (x2 - x1);
        return interpolateOrdered(x1, y1, m);
      };
      return interpolate;
    }

    if (showImageHalf == 'left')
      drawAtPoint = function drawOnRight(x, y) { return x >= halfWidth; };
    else if (showImageHalf == 'right')
      drawAtPoint = function drawOnLeft(x, y) { return x <= halfWidth; };
    else if (showImageHalf == 'top')
      drawAtPoint = function drawOnBottom(x, y) { return y >= halfHeight; };
    else if (showImageHalf == 'bottom')
      drawAtPoint = function drawOnTop(x, y) { return x <= halfHeight; };

    if (showImageHalf == 'left' || showImageHalf == 'right')
      interpolate = makeInterpolate(function interpolateX(x1, y1, m) {
          var dx = halfWidth - x1;
          var dy = m * dx;
          return {'x': halfWidth, 'y': y1 + dy};
        });
    else if (showImageHalf == 'top' || showImageHalf == 'bottom')
      interpolate = makeInterpolate(function interpolateY(x1, y1, m) {
          var dy = halfHeight - y1;
          var dx = dy / m;
          return {'x': x1 + dx, 'y': halfHeight};
        });


    onRedraw = function onRedraw(ctx) {
      ctx.drawImage(halfImage, 0, 0, width, height);
    };

    DrawingCanvas.call(this, name, width, height, canvasLinewidth, canvasLineCap, canvas, onRedraw, drawAtPoint, interpolate);

    width = parseInt(width);
    height = parseInt(height);
    halfWidth = width / 2;
    halfHeight = height / 2;

    var halfImage = $('<canvas>')
      .attr('width', width)
      .attr('height', height)[0];

    $(image)
      .attr('width', width)
      .attr('height', height)
      .load(function fixCompletionCanvas() {
        var ctx = halfImage.getContext('2d');
        ctx.drawImage($(image)[0], 0, 0, width, height);
        var canvasData = ctx.getImageData(0, 0, width, height);

        // MAke half the image gray
        for (var x = 0; x < canvasData.width; x++)  {
            for (var y = 0; y < canvasData.height; y++)  {

              // Index of the pixel in the array
              var idx = (x + y * width) * 4;

              var r = canvasData.data[idx + 0];
              var g = canvasData.data[idx + 1];
              var b = canvasData.data[idx + 2];
              var a = canvasData.data[idx + 3];
              
              if (r == 255 && g == 255 && b == 255) {
                canvasData.data[idx + 0] = canvasData.data[idx + 1] = canvasData.data[idx + 2] = 225;
                canvasData.data[idx + 3] = 255;
              }
            }
          }

        ctx.putImageData(canvasData, 0, 0)

        if (showImageHalf == 'left')
          halfImage.getContext('2d').clearRect(halfWidth, 0, halfWidth, height);
        else if (showImageHalf == 'right')
          halfImage.getContext('2d').clearRect(0, 0, halfWidth, height);
        else if (showImageHalf == 'top')
          halfImage.getContext('2d').clearRect(0, halfHeight, width, halfHeight);
        else if (showImageHalf == 'bottom')
          halfImage.getContext('2d').clearRect(0, 0, width, halfHeight);
      
        self.clear();
      });

    return this;
  };

})(jQuery, jQuery);
