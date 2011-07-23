#!/usr/bin/python
# recordcompletionsubmission.py -- Stores the data from the completion submission
import os, tempfile
import cairo
from alphabetspaths import *
import htmlcanvas
import turkutil
from alphabetsutil import compress_images, png_to_uri, uri_to_png, compress_stroke

alphabets_strokes_dict = get_accepted_stroke_list()
alphabets_images_dict = get_accepted_image_list(from_path='.')

def record_submission(form_dict, path=CLASSIFICATION_UNREVIEWED_PATH, **kwargs):
    desc =  'GIVEN %%(task-%(task)d-image-alphabet)s, %%(task-%(task)d-image-character-number)s, %%(task-%(task)d-image-id)s'
    make_summary = turkutil.make_default_make_summary(desc, count_correct=False)
    turkutil.record_submission(form_dict, path=path, make_summary=make_summary, preprocess_form=fixup_images,
                               put_extras=put_extras, extra_matlab_code=generate_matlab_image_code, **kwargs)

def fixup_images(form_dict, width=105, height=105):
    tasks_data = turkutil.form_dict_to_tasks_dict(form_dict)['task']
    image_dict = {}
    for n, task in tasks_data.iteritems():
        original_strokes_path = alphabets_strokes_dict[task['image-alphabet']][task['image-id']][int(task['image-character-number']) - 1]
        image_half = task['image-show_half']
        strokes = task['strokes']

        image = cairo.ImageSurface.create_from_png(alphabets_images_dict[task['image-alphabet']][task['image-id']][int(task['image-character-number']) - 1])
        ctx = cairo.Context(image)

        # unpaint the half-image

        # paint white
        ctx.set_source_rgb(1.0, 1.0, 1.0)
        if image_half == 'top':
            ctx.rectangle(0, height / 2, width, height)
        elif image_half == 'bottom':
            ctx.rectangle(0, 0, width, height / 2)
        elif image_half == 'left':
            ctx.rectangle(width / 2, 0, width, height)
        elif image_half == 'right':
            ctx.rectangle(0, 0, width / 2, height)
        ctx.fill()

        # and clip
        if image_half == 'top':
            ctx.rectangle(0, height / 2 - 2.5, width, height)
        elif image_half == 'bottom':
            ctx.rectangle(0, 0, width, height / 2 + 2.5)
        elif image_half == 'left':
            ctx.rectangle(width / 2 - 2.5, 0, width, height)
        elif image_half == 'right':
            ctx.rectangle(0, 0, width / 2 + 2.5, height)
        ctx.clip()

        image, ctx = htmlcanvas.paint_image_with_strokes_cairo(strokes, size=(width,height), offset=0, image=image, ctx=ctx, clear=False)
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image.write_to_png(f)
            image_dict['task-%s-image' % int(n)] = f.name

    compress_images(image_list=image_dict.values(), do_color_change=False)
    for key, path in image_dict.iteritems():
        form_dict[key] = png_to_uri(path)
        os.remove(path)

    return form_dict

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
        div {
            display: inline-block;
            border: thin solid black;
        }
    </style>
</head>
<body>""" % uid]

    for n, task in tasks_data.iteritems():
        image_name = image_file_base_name + '%d.png' % (int(n) + 1)
        uri_to_png(task['image'], '%s%d.png' % (image_file_base_name, int(n) + 1))
        html.append(r"""<div><img src="%s" alt="given" /><img src="%s_image_%d.png" alt="drawn" /></div>""" %
                    (task['image-anonymous_url'], uid.replace('-', 'm'), int(n) + 1))
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
