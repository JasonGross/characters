function getCharacterTags()
{
  rtn = [];
  if (getURLParameter('image') != '') rtn.push('');
  if (getURLParameter('image0') != '') rtn.push('0');
  for (var i = 1; getURLParameter('image'+i) != ''; i++)
    rtn.push(i);
  if (getRandomizeOrder()) rtn = sample(rtn, rtn.length);
  return rtn;
}

/*function characterTagsToTable(tags)
{
  if (tags.length == 0) return tags;
  var rtn = [];
  var cur = [];
  var num_per_row;
  if (getNumCols() == null || (getNumRows() != null && getCharacterOrder() == COLS_FIRST))
    num_per_row = Math.ceil(tags.length / getNumRows());
  else if (getNumCols() != null)
    num_per_row = getNumCols();
  else //This should not happen.  We'll default to all in the same row.
    num_per_row = tags.length;
  for (var i = 0; i < tags.length; i++) {
    if (i % num_per_row == 0 && i != 0) {
      rtn.push(cur);
      cur = [];
    }
    cur.push(tags[i]);
  }
  rtn.push(cur);
  if (getCharacterOrder() == COLS_FIRST) rtn = transpose(rtn);
  return rtn;
}*/

function getImgId(tag) { return 'img_' + getCharacterId(tag); }

function makeImg(tag)
{
  var rtn = '';
  if (getURLParameter('image'+tag) != '') {
    rtn = rtn + '<img src="results/originals/'+getURLParameter('image'+tag)+'"';
    if (!hasURLParameter('noscaling')) {
      if (getURLParameter('image'+tag+'Width') != '')
        rtn = rtn + ' width="'+getURLParameter('image'+tag+'Width')+'"';
      else if (getURLParameter('image'+tag+'Height') != '')
        rtn = rtn + ' height="'+getURLParameter('image'+tag+'Height')+'"';
      else
        rtn = rtn + getImageSize();
    }
    rtn = rtn + ' unselectable="on" id="'+ getImgId(tag) +'" name="'+ getCharacterId(tag)+'_0_image_display"/>';
  }
  return rtn;
}

function makeCanvasWidth(param, tag, canvasId)
{
  var rtn;
  var img = document.getElementById(getImgId(tag));
  if (getURLParameter(param).toLowerCase() == 'fit' ||
      (getURLParameter(param) == '' && getCanvasWidth().toLowerCase() == 'fit')) {
    if (img.width != 0) rtn = img.width;
    else {
      rtn = backupCanvasWidth;
      var fixW = function() { document.getElementById(canvasId).width = img.width; };
      if (img.attachEvent) {
        window.attachEvent('onload', function(){fixW();});
        img.attachEvent('onload', function(){fixW();});
      } else if (img.addEventListener) {
        window.addEventListener('load', function(){fixW();}, false);
        img.addEventListener('load', function(){fixW();}, false);
      } else {
        img.addEventListener('load', function(){fixW();}, false);
      }
    }
  } else if (getURLParameter(param) != '')
    rtn = getURLParameter(param);
  else
    rtn = getCanvasWidth();
  return ' width="' + rtn + '"';
}

function makeCanvasHeight(param, tag, canvasId)
{
  var rtn;
  var img = document.getElementById(getImgId(tag));
  if (getURLParameter(param).toLowerCase() == 'fit' ||
      (getURLParameter(param) == '' && getCanvasHeight().toLowerCase() == 'fit')) {
    if (img.height != 0 && img.width != 0) rtn = img.height; // because in Firefox, unloaded images apparantly have height 19 and width 0!?
    else {
      rtn = backupCanvasHeight;
      var fixH = function() { document.getElementById(canvasId).height = img.height; };
      if (img.attachEvent) {
        window.attachEvent('onload', function(){fixH();});
        img.attachEvent('onload', function(){fixH();});
      } else if (img.addEventListener) {
        window.addEventListener('load', function(){fixH();}, false);
        img.addEventListener('load', function(){fixH();}, false);
      } else {
        img.addEventListener('load', function(){fixH();}, false);
      }
    }
  } else if (getURLParameter(param) != '')
    rtn = getURLParameter(param);
  else
    rtn = getCanvasHeight();
  return ' height="' + rtn + '"';
}


function makeCharacterInput(name, tag)
{
  var rtn = '';
  rtn += '<input type="hidden" name="'+name+'_image" id="'+name+'_image">';
  rtn += '<input type="hidden" name="'+name+'_stroke" id="'+name+'_stroke">';
  rtn += '<div id="'+name+'_div">';
    
  rtn += '<canvas id="'+name+'" unselectable="on"';
  if (getURLParameter('canvas'+tag+'Size') != '')
    rtn += makeCanvasWidth('canvas'+tag+'Size', tag) + makeCanvasHeight('canvas'+tag+'Size', tag, name);
  else {
    if (getURLParameter('canvas'+tag+'Height') != '')
      rtn += makeCanvasHeight('canvas'+tag+'Height', tag, name);
    else
      rtn += makeCanvasHeight('image'+tag+'Height', tag, name);
    if (getURLParameter('canvas'+tag+'Width') != '')
      rtn += makeCanvasWidth('canvas'+tag+'Width', tag, name);
    else
      rtn += makeCanvasWidth('image'+tag+'Width', tag, name);
  }
  rtn += '>';
  rtn += 'Your browser must support the &lt;canvas&gt; element in order to use this site.';
  if (document.all) { //This is a test for Internet Explorer
    rtn += ' Please use another browser, such as Google Chrome or Mozilla Firefox.';
  }
  rtn += '</canvas></div>';
  rtn += '<div id="canvascontrols"> <a id="clear" href="javascript:document.getElementById(\''+name+'\').clear()" unselectable="on">clear</a>';
  rtn += '<a id="undo" name="'+name+'_undo" href="javascript:document.getElementById(\''+name+'\').undo()" unselectable="on"></a>';
  rtn += '<a id="redo" name="'+name+'_redo" href="javascript:document.getElementById(\''+name+'\').redo()" unselectable="on"></a>';
  rtn += '</div>';

  var addC = function() { addCanvas(document.getElementById(name)); };
  var makeD;
  if (getURLParameter('lineWidth'+tag) != '') 
    makeD = function() { makeDrawable(document.getElementById(name), parseFloat(getURLParameter('lineWidth'+tag)), document.getElementsByName(name + '_undo')[0], document.getElementsByName(name + '_redo')[0]); };
  else
    makeD = function() { makeDrawable(document.getElementById(name), undefined, document.getElementsByName(name + '_undo')[0], document.getElementsByName(name + '_redo')[0]); };  
  if (window.attachEvent) {window.attachEvent('onload', function(){addC(); makeD();});}
  else if (window.addEventListener) {window.addEventListener('load', function(){addC(); makeD();}, false);}
  else {document.addEventListener('load', function(){addC(); makeD();}, false);}
  
  return rtn;
}


function makeCharacterInputs(tag, count)
{
  if (count === undefined) count = getSampleCount();
  var rtn = '';
  if (getURLParameter('image'+tag) != '') {
    rtn += '<input type="hidden" name="image'+tag+'" id="image'+tag+'" value="'+getURLParameter('image'+tag)+'">';
    if (getURLParameter('character'+tag+'ID') != '')
      rtn += '<input type="hidden" name="character'+tag+'Id" id="character'+tag+'Id" value="'+getURLParameter('character'+tag+'ID')+'">';
    else if (getURLParameter('image'+tag+'ID') != '')
      rtn += '<input type="hidden" name="character'+tag+'Id" id="character'+tag+'Id" value="'+getURLParameter('image'+tag+'ID')+'">';
    
    rtn += '<table><tr>';
    for (var i = 0; i < count; i++) {
      rtn += '<td align="center">';
      rtn += makeCharacterInput(getCharacterId(tag)+'_'+i, tag);
      rtn += '</td>';
    }
    rtn += '</tr></table>';
  }
  return rtn;
}

function makeImageCharacterPair(tag)
{
  document.write('<table>');
  document.write('  <tbody>');
  document.write('    <tr>');
  document.write('      <td align="center" valign="middle">');
  document.write('        ' + makeImg(tag));
  document.write('      </td>');
  if (isVertical()) {
    document.write('    </tr>');
    document.write('    <tr>');
  }
  document.write('      <td valign="middle">');
  document.write('        ' + makeCharacterInputs(tag));
  document.write('      </td>');
  document.write('    </tr>');
  document.write('  </tbody>');
  document.write('</table>');
  return rtn;
}
