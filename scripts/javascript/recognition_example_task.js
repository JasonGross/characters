var startExampleTask;
(function ($) {
  var cursor;
  var cursorStart;
  $(function () {
    cursor = $('#example-mouse-cursor');
    cursorStart = cursor.offset();
    cursor.css({'left':cursorStart.left, 'top':cursorStart.top});
  });
  startExampleTask = function () {
    var task;
    task = makeTask(-2, {'anonymous url':'http://scripts.mit.edu/~jgross/alphabets/images/example_k1.png'},
                    {'anonymous url':'http://scripts.mit.edu/~jgross/alphabets/images/example_k2.png'},
                    'http://scripts.mit.edu/~jgross/alphabets/images/strokeNoise.png', 
                    true,  {'do-task':function () { window.setTimeout(function () { task['do-task'](); }, 2000); }}, undefined, {'right':0, 'wrong':0}, 'Example Task 1 of 1',
                    function () {}, false, $('#example-task'), null, true,
                    function () {
                      offset = task['questionInputYes'].offset();
                      window.setTimeout(function () {
                        cursor.animate({'left':offset.left + task['questionInputYes'].width() / 2, 'top':offset.top + task['questionInputYes'].height() / 2}, 'slow', 'linear',
                                       function () {
                                        task['questionInputYes'].attr('checked', 'checked');
                                        window.setTimeout(function () { task['questionInputYes'].change(); }, 2000);
                                        window.setTimeout(function () { cursor.animate({'left':cursorStart.left, 'top':cursorStart.top}, 'slow', 'linear'); }, 3000);
                                       });
                      }, 2000);
                    }, false);
    var oldDoTask = task['do-task'];
    task['do-task'] = function () {
      //cursor.animate({'left':cursorStart.left, 'top':cursorStart.top}, 'slow', 'linear');
      oldDoTask();
    }
    task['do-task']();
  };
})(jQuery);
