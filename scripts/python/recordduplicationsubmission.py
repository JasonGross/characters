#!/usr/bin/python
# recordduplicationsubmission.py -- Stores the data from the duplication submission
import os, tempfile
import re
import cairo
from alphabetspaths import *
import htmlcanvas
import turkutil
from alphabetsutil import compress_images, png_to_uri, uri_to_png, compress_stroke

alphabets_strokes_dict = get_accepted_stroke_list()
alphabets_images_dict = get_accepted_image_list(from_path='.')

def record_submission(form_dict, path=CLASSIFICATION_UNREVIEWED_PATH, **kwargs):
    turkutil.record_submission(form_dict, path=path, make_summary=None, preprocess_form=fixup_images,
                               put_extras=put_extras, extra_matlab_code=generate_matlab_image_code, **kwargs)

def fixup_images(form_dict, width=100, height=100, offset=None):
    tasks_data = turkutil.form_dict_to_tasks_dict(form_dict)['task']
    image_dict = {}
    for n, task in tasks_data.iteritems():
        strokes = task['strokes']

        image, ctx = htmlcanvas.paint_image_with_strokes_cairo(strokes, size=(width,height), offset=offset)
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image.write_to_png(f)
            image_dict['task-%s-image' % int(n)] = f.name

    compress_images(image_list=image_dict.values(), do_color_change=False)
    for key, path in image_dict.iteritems():
        form_dict[key] = png_to_uri(path)
        os.remove(path)

    return form_dict

CLASS_REGEX = re.compile('class-([0-9]+)-example-image-([0-9]+)-anonymous_url')
def put_extras(path, form_dict, uid, quiet=True):
    html_file_name = os.path.join(path, uid.replace('-', 'm') + '_drawings.html')
    image_file_base_name = os.path.join(path, uid.replace('-', 'm') + '_image_')
    stroke_file_base_name = os.path.join(path, uid.replace('-', 'm') + '_stroke_')

    tasks_data = turkutil.form_dict_to_tasks_dict(form_dict)['task']
    html = [r"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <title>Images Drawn By %s</title>
    <style type="text/css">
        div.task {
            display: inline-block;
            border: thin solid black;
        }

        .image-holder {
              padding: 2.5px;
              width: 100px;
              height: 100px;
        }

        .class-holder {
              display: inline-block;
              padding: 0px;
        }

        .class-box {
              display: inline-block;
              padding: 0px;
        }

        .image-box {
              margin: 2.5px;
              border: thin solid #C0C0C0; //lightgray
              text-align: center;
              vertical-align: middle;
              display: block;
        }

        .class-box-untimed {
              border: thin black solid;
        }

    </style>
</head>
<body>""" % uid]

    for n, task in tasks_data.iteritems():
        image_name = image_file_base_name + '%d.png' % (int(n) + 1)
        uri_to_png(task['image'], '%s%d.png' % (image_file_base_name, int(n) + 1))
        drawn_image = r"""<img src="%s_image_%d.png" alt="drawn" title="drawn"/>""" % (uid.replace('-', 'm'), int(n) + 1)
        if 'class-0-example-image-1-anonymous_url' in task or \
           'class-1-example-image-0-anonymous_url' in task: # untimed, multiple images
            task_html = []
            class_urls = {}
            for key, value in task.iteritems():
                if '-anonymous_url' not in key: continue
                match = CLASS_REGEX.match(key)
                if not match: continue
                class_i, example_i = map(int, match.groups())
                if class_i not in class_urls: class_urls[class_i] = {}
                class_urls[class_i][example_i] = value
            for class_i in sorted(class_urls.keys()):
                task_html.append('<div class="class-box class-box-untimed">')
                for example_i in sorted(class_urls[class_i].keys()):
                    task_html.append(r"""<div class="image-box">
<span class="wraptocenter image-holder">
<img src="%s" />
</span>
</div>""" % class_urls[class_i][example_i])
                task_html.append('</div>')
            task_html.append(r'<br />')
            task_html.append(drawn_image)
            task_html = '\n'.join(task_html)
        else: # timed, single image
            task_html = r"""<img src="%s" alt="given" title="given"/>%s</div>""" % (task['class-0-example-image-0-anonymous_url'], drawn_image)
        html.append(r"""<div class="task">%s</div>""" % task_html)
        with open('%s%d.cstroke' % (stroke_file_base_name, int(n) + 1), 'wb') as f:
            f.write(compress_stroke(task['strokes']))

    html.append(r"""</body>
</html>""")
    with open(html_file_name, 'w') as f:
        f.write('\n'.join(html))

def generate_matlab_image_code(folder, properties, file_name, uid, not_use, quiet=True, zero_based_num=0):
    uid = uid.replace('-', 'm')
    tasks_data = turkutil.form_dict_to_tasks_dict(properties)['task']
    rtn = []

    for n, task in tasks_data.iteritems():
        n = int(n)
        rtn.append("results.for_%s(%d).task(%d).image = imread('%s_image_%d.png');" % (uid, zero_based_num + 1, n + 1, os.path.join(folder, uid), n + 1))

    return '\n\n' + '\n'.join(rtn)
