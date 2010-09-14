#!/usr/bin/python
# Filename: make-matlab.py
from __future__ import with_statement
import datetime
import os
import re
import sys
import glob
from alphabetspaths import *
import alphabetsutil

os.chdir(RESULTS_PATH)

SAVE_STROKE = True
MAKE_EXPLICIT = True

now = datetime.datetime.now().isoformat()

matlab_header = """%% %s
%%color_order = get(gca,'ColorOrder');
%%fps = 5;
%%t_per_second = 1000;
%%make_3d = false;
%%save_3d = false;
save_stroke = %s;
clear accepted_alphabets;
clear rejected_alphabets;
clear unreviewed_alphabets;

tic;
""" % (now, str(SAVE_STROKE).lower())

matlab_footer = """
if ~save_stroke
  alphabets = rmfield(alphabets, {'character_xss', 'character_yss', 'character_yss'});
  rejected_alphabets = rmfield(rejected_alphabets, {'character_xss', 'character_yss', 'character_tss'});
  unreviewed_alphabets = rmfield(unreviewed_alphabets, {'character_xss', 'character_yss', 'character_tss'});
end
clear character_i person_i line_i point_i last_t fig aviobj new_xs new_ys new_ts im save_stroke toolbox_version;
"""

def make_matlab_segment(alphabet_id, alphabet_num, prefix, get_ids, get_extra_info_file_name,
                        get_image_list, get_stroke_list,
                        extra_info_keys=('feedback', 'actual_input_device', 'actual_seen_before',
                                         'age', 'language-read', 'language-read-write', 'native-language',
                                         'comments'),
                        info_types={'age':int, 'uids':str},
                        prefix_sep='_', verbose=True, save_stroke=SAVE_STROKE, make_explicit=MAKE_EXPLICIT):
    if verbose: print('  Getting alphabet name...')
    alphabet_name = get_alphabet_name(alphabet_id)
    rtn = ['%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ',
           ('%s (%s) - %s' % (alphabet_id, alphabet_name, prefix)),
           ' %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n']
    alphabets_list_name = '%s%salphabets(%d)' % (prefix, prefix_sep, alphabet_num)
    props = {'alphabets_list_name':alphabets_list_name, 'alphabet_name':alphabet_name}
    def cur_props(new_props):
        rtn = props.copy()
        rtn.update(new_props)
        return rtn
    rtn.append("%(alphabets_list_name)s.name = %(alphabet_name_fixed)s;\n" % cur_props({'alphabet_name_fixed':format_for_matlab(props['alphabet_name'])}))
    if verbose: print('  Getting alphabet ids...')
    uids = get_ids(alphabet_id)
    if verbose: print('  Getting info names...')
    extra_info_names = get_extra_info_file_name(alphabet_id=alphabet_id, from_path=os.getcwd())
    if verbose: print('  Getting stroke names...')
    stroke_names = get_stroke_list(alphabet_id=alphabet_id, from_path=os.getcwd())
    if verbose: print('  Getting image names...')
    old_format_image_names = get_image_list(alphabet_id=alphabet_id, from_path=os.getcwd())
    if verbose: print('  Getting original image name...')
    original_images = get_original_image_list(alphabet_id=alphabet_id, from_path=os.getcwd())
    extra_infos = {'uids':{}}
    strokes = []
    image_names = []
    if verbose: print('  Parsing extra information...')
    for key in extra_info_keys:
        extra_infos[key] = {}
    for uid in uids:
        with open(extra_info_names[uid], 'r') as f:
            cur_extra_info = [line.split(': ') for line in f]
        cur_extra_info = [(line[0], ': '.join(line[1:])) for line in cur_extra_info]
        for key, value in cur_extra_info:
            if key not in extra_infos: extra_infos[key] = {}
            extra_infos[key][uid] = value.strip('\n')
        extra_infos['uids'][uid] = uid

        for stroke_num in range(len(stroke_names[uid])):
            while stroke_num >= len(strokes):
                strokes.append({})
            strokes[stroke_num][uid] = alphabetsutil.get_stroke(stroke_names[uid][stroke_num], parsed=True)
##            if "'y':'y':" in strokes[stroke_num][uid]:
##                strokes[stroke_num][uid] = strokes[stroke_num][uid].replace("'y':'y':", "'y':")
##                with open(stroke_names[uid][stroke_num], 'w') as f:
##                    f.write(strokes[stroke_num][uid])

        for image_num in range(len(old_format_image_names[uid])):
            while image_num >= len(image_names):
                image_names.append({})
            image_names[image_num][uid] = old_format_image_names[uid][image_num]

    # fix extra_infos formatting
    if verbose: print('  Fixing extra information formatting...')
    for key in extra_infos:
        if len(extra_infos[key]) != len(uids):
            for uid in uids:
                if uid not in extra_infos[key]:
                    extra_infos[key][uid] = ''
        if key in info_types:
            for uid in uids:
                if extra_infos[key][uid]:
                    extra_infos[key][uid] = info_types[key](extra_infos[key][uid])
                elif info_types[key] is int:
                    extra_infos[key][uid] = None

    for key in sorted(extra_infos.keys()):
        rtn.append("%(alphabets_list_name)s.%(key)s = %(value)s;\n" % \
                   cur_props({'key':key.replace('-', '_'), 'value':format_for_matlab([extra_infos[key][uid] for uid in uids])}))

    # original images
    if verbose: print('  Appending original images...')
    first_part = "%(alphabets_list_name)s.original_images = {\n" % props
    rtn.append(first_part)
    spaces = ''.join(' ' for i in first_part)
    for image_name in original_images:
        rtn.append("%simread('%s'),...\n" % (spaces, image_name))
    rtn.append('%s};\n' % spaces)

    # results images
    if verbose: print('  Appending results images...')
    first_part = "%(alphabets_list_name)s.character_images = {\n" % props
    rtn.append(first_part)
    spaces = ''.join(' ' for i in first_part)
    for image_name_dict in image_names:
        rtn.append(spaces + '{')
        rtn.append(', '.join("imread('%s')" % image_name_dict[uid] for uid in uids))
        rtn.append('},...\n')
    rtn.append('%s};\n' % spaces)

    # make xs, ys, ts
    xss = []
    yss = []
    tss = []
    if verbose: print('  Parsing and fixing strokes...')
    for stroke_dict in strokes:
        xss.append({})
        yss.append({})
        tss.append({})
        for uid in uids:
            cur_stroke = stroke_dict[uid]
            xss[-1][uid] = '{' + ', '.join('[int8(' + '), int8('.join(str(point['x']) for point in stroke) + ')]' for stroke in cur_stroke) + '}'
            yss[-1][uid] = '{' + ', '.join('[int8(-' + '), int8(-'.join(str(point['y']) for point in stroke) + ')]' for stroke in cur_stroke) + '}'
            tss[-1][uid] = '{' + ', '.join('[uint16(' + '), uint16('.join(str(point['t']) for point in stroke) + ')]' for stroke in cur_stroke) + '}'

    stroke_parts = {'xss':xss, 'yss':yss, 'tss':tss}
    # strokes
    if verbose: print('  Appending strokes images...')
    for stroke_name in ('xss', 'yss', 'tss'):
        first_part = "%(alphabets_list_name)s.character_%(stroke_name)s = {\n" % cur_props({'stroke_name':stroke_name})
        rtn.append(first_part)
        spaces = ''.join(' ' for i in first_part)
        for character_strokes in stroke_parts[stroke_name]:
            rtn.append(spaces + '{\n' + spaces + ' ')
            rtn.append((spaces + ' ').join(character_strokes[uid] + ',...\n' for uid in uids))
            rtn.append(spaces + '},...\n')
        rtn.append('%s};\n' % spaces)

    if save_stroke and make_explicit:
        for character_i in range(len(xss)):
            for person_i in range(len(xss[character_i])):
                uid = uids[person_i]
                new_xs = xss[character_i][uid][1:-1].replace('], [', ', NaN, ')
                new_ys = yss[character_i][uid][1:-1].replace('], [', ', NaN, ')
                new_ts = tss[character_i][uid][1:-1].replace('], [', ', NaN, ')
                rtn.append("%(alphabets_list_name)s.character_xss{%(character_i)d}{%(person_i)d} = %(new_stroke)s;\n" % \
                           cur_props({'character_i':character_i+1, 'person_i':person_i+1, 'new_stroke':new_xs}))
                rtn.append("%(alphabets_list_name)s.character_yss{%(character_i)d}{%(person_i)d} = %(new_stroke)s;\n" % \
                           cur_props({'character_i':character_i+1, 'person_i':person_i+1, 'new_stroke':new_ys}))
                rtn.append("%(alphabets_list_name)s.character_tss{%(character_i)d}{%(person_i)d} = %(new_stroke)s;\n" % \
                           cur_props({'character_i':character_i+1, 'person_i':person_i+1, 'new_stroke':new_ts}))
                rtn.append("""%(alphabets_list_name)s.character_time_strokes{%(character_i)d}{%(person_i)d} = strcat('clf; ',...
     'line(min(%(alphabets_list_name)s.character_xss{%(character_i)d}{%(person_i)d}), min(%(alphabets_list_name)s.character_yss{%(character_i)d}{%(person_i)d}));',...
     'line(max(%(alphabets_list_name)s.character_xss{%(character_i)d}{%(person_i)d}), max(%(alphabets_list_name)s.character_yss{%(character_i)d}{%(person_i)d}));',...
     'for point_i = 1:length(%(alphabets_list_name)s.character_xss{%(character_i)d}{%(person_i)d});',...
       'line(%(alphabets_list_name)s.character_xss{%(character_i)d}{%(person_i)d}(1:point_i), %(alphabets_list_name)s.character_yss{%(character_i)d}{%(person_i)d}(1:point_i));',...
       'getframe;',... %% this makes it take time.
     'end;',...
     'clear point_i;');

""" % cur_props({'character_i':character_i+1, 'person_i':person_i+1}))
    elif save_stroke:
        rtn.append("""if save_stroke
  for character_i = 1:length(%(alphabets_list_name)s.character_xss)
    for person_i = 1:length(%(alphabets_list_name)s.character_xss{character_i})
      new_xs = [];
      new_ys = [];
      new_ts = [];
      for line_i = 1:length(%(alphabets_list_name)s.character_xss{character_i}{person_i})
        new_xs = [new_xs, %(alphabets_list_name)s.character_xss{character_i}{person_i}{line_i}, NaN];
        new_ys = [new_ys, %(alphabets_list_name)s.character_yss{character_i}{person_i}{line_i}, NaN];
        new_ts = [new_ts, %(alphabets_list_name)s.character_tss{character_i}{person_i}{line_i}, NaN];
      end
      %(alphabets_list_name)s.character_xss{character_i}{person_i} = new_xs;
      %(alphabets_list_name)s.character_yss{character_i}{person_i} = new_ys;
      %(alphabets_list_name)s.character_tss{character_i}{person_i} = new_ts;
      %(alphabets_list_name)s.character_strokes{character_i}{person_i} = strcat('clf; plot(%(alphabets_list_name)s.character_xss{', num2str(character_i), '}{', num2str(person_i), '}, %(alphabets_list_name)s.character_yss{', num2str(character_i), '}{', num2str(person_i), '});');
      %(alphabets_list_name)s.character_time_strokes{character_i}{person_i} = strcat('clf; ',...
                                                 'line(min(%(alphabets_list_name)s.character_xss{', num2str(character_i), '}{', num2str(person_i), '}), min(%(alphabets_list_name)s.character_yss{', num2str(character_i), '}{', num2str(person_i), '}));',...
                                                 'line(max(%(alphabets_list_name)s.character_xss{', num2str(character_i), '}{', num2str(person_i), '}), max(%(alphabets_list_name)s.character_yss{', num2str(character_i), '}{', num2str(person_i), '}));',...
                                                 'for point_i = 1:length(%(alphabets_list_name)s.character_xss{', num2str(character_i), '}{', num2str(person_i), '});',...
                                                   'line(%(alphabets_list_name)s.character_xss{', num2str(character_i), '}{', num2str(person_i), '}(1:point_i), %(alphabets_list_name)s.character_yss{', num2str(character_i), '}{', num2str(person_i), '}(1:point_i));',...
                                                   'getframe;',... %% this makes it take time.
                                                 'end;',...
                                                 'clear point_i;');
    end
  end
end

""" % props)
    rtn.append("""

disp('%(alphabets_list_name)s');
disp(toc);
""" % props)

    if alphabet_num % 10 == 0:
        rtn.append("""

%%disp('Packing...');
%%pack;
%%disp('Done packing.');

""")

    rtn.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% End ' + \
               ('%s (%s) - %s' % (alphabet_id, alphabet_name, prefix)) + \
               ' %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n\n\n')
    return ''.join(rtn)

def make_display_all_strokes(prefix, prefix_sep='_'):
    alphabets_list_name = '%s%salphabets' % (prefix, prefix_sep)
    return """


show_all_%(prefix)s_strokes = strcat('ratio=5;fps=23/ratio;verbose=false;',...
          'for alphabet_i = 1:length(%(alphabets_list_name)s); ',...
            'for character_i = 1:length(%(alphabets_list_name)s(alphabet_i).character_xss); ',...
              'for person_i = 1:length(%(alphabets_list_name)s(alphabet_i).character_xss{character_i}); ',...
                'tic; clf; ',...
                'line(min(%(alphabets_list_name)s(alphabet_i).character_xss{character_i}{person_i}), ',...
                     'min(%(alphabets_list_name)s(alphabet_i).character_yss{character_i}{person_i})); ',...
                'line(max(%(alphabets_list_name)s(alphabet_i).character_xss{character_i}{person_i}), ',...
                     'max(%(alphabets_list_name)s(alphabet_i).character_yss{character_i}{person_i})); ',...
                'for point_i = 1:length(%(alphabets_list_name)s(alphabet_i).character_xss{character_i}{person_i}); ',...
                  'if (point_i == length(%(alphabets_list_name)s(alphabet_i).character_xss{character_i}{person_i})) || ',...
                      '(round(%(alphabets_list_name)s(alphabet_i).character_tss{character_i}{person_i}(point_i) / (1000 / fps)) ~= ',...
                         'round(%(alphabets_list_name)s(alphabet_i).character_tss{character_i}{person_i}(point_i+1) / (1000 / fps))) ',...
                    'line(%(alphabets_list_name)s(alphabet_i).character_xss{character_i}{person_i}(1:point_i), ',...
                         '%(alphabets_list_name)s(alphabet_i).character_yss{character_i}{person_i}(1:point_i)); ',...
                     'getframe; ',...
                     'while toc < 1/fps/ratio;end;',...
                     'if verbose;disp(toc); end;',...
                   'end; ',...
                 'end; ',...
               'pause; ',...
               'end; ',...
             'end; ',...
           'end;');
""" % {'prefix':prefix, 'alphabets_list_name':alphabets_list_name}
    
def make_matlab_remove_strokes(file_name, alphabet_names):
    if isinstance(alphabet_names, str):
        alphabet_names = [alphabet_names]
    rtn = []
    for alphabet_name in alphabet_names:
        rtn.append(r"""if exist('%(alphabet_name)s')
    """ % locals())
        for var in ('character_xss', 'character_yss', 'character_tss', 'character_time_strokes'):
            rtn.append(r"""    %(alphabet_name)s = rmfield(%(alphabet_name)s, '%(var)s');""" % locals())
        rtn.append(r"""
end
""")
    rtn.append(r'clear alphabet_num show_all_accepted_strokes show_all_rejected_strokes show_all_strokes show_all_unreviewed_strokes show_all_extra_strokes;')
    with open(file_name, 'w') as f:
        f.write(''.join(rtn))

def make_matlab_padd(file_name, alphabet_names):
    if isinstance(alphabet_names, str):
        alphabet_names = [alphabet_names]
    rtn = []
    for alphabet_name in alphabet_names:
        rtn.append(r"""if exist('%(alphabet_name)s')
    for alphabet_num = 1:length(%(alphabet_name)s)
        disp(alphabet_num);
        disp(toc);
        for image_num = 1:length(%(alphabet_name)s(alphabet_num).original_images)
            [h, w] = size(%(alphabet_name)s(alphabet_num).original_images{image_num});
            if h > w
                padd0 = logical(zeros(h, floor((h - w) / 2)));
                padd1 = logical(zeros(h, ceil((h - w) / 2)));
                %(alphabet_name)s(alphabet_num).original_images{image_num} = [padd0, logical(%(alphabet_name)s(alphabet_num).original_images{image_num}), padd1];
            else
                padd0 = logical(zeros(floor((w - h) / 2), w));
                padd1 = logical(zeros(ceil((w - h) / 2), w));
                %(alphabet_name)s(alphabet_num).original_images{image_num} = [padd0; logical(%(alphabet_name)s(alphabet_num).original_images{image_num}); padd1];
            end
        end
        for image_num = 1:max(size(%(alphabet_name)s(alphabet_num).character_images))
            for user_num = 1:max(size(%(alphabet_name)s(alphabet_num).character_images{image_num}))
                [h, w] = size(%(alphabet_name)s(alphabet_num).character_images{image_num}{user_num});
                if h > w
                    padd0 = logical(zeros(h, floor((h - w) / 2)));
                    padd1 = logical(zeros(h, ceil((h - w) / 2)));
                    %(alphabet_name)s(alphabet_num).character_images{image_num}{user_num} = [padd0, logical(%(alphabet_name)s(alphabet_num).character_images{image_num}{user_num}), padd1];
                else
                    padd0 = logical(zeros(floor((w - h) / 2), w));
                    padd1 = logical(zeros(ceil((w - h) / 2), w));
                    %(alphabet_name)s(alphabet_num).character_images{image_num}{user_num} = [padd0; logical(%(alphabet_name)s(alphabet_num).character_images{image_num}{user_num}); padd1];
                end
            end
        end
    end
end
""" % locals())
    rtn.append(r'clear padd0 padd1 h w size0 size1 cur_size alphabet_num image_num user_num;')
    with open(file_name, 'w') as f:
        f.write(''.join(rtn))

def make_matlab_resize(file_name, alphabet_names, width=28, height=28):
    if isinstance(alphabet_names, str):
        alphabet_names = [alphabet_names]
    rtn = []
    for alphabet_name in alphabet_names:
        rtn.append(r"""if exist('%(alphabet_name)s')
    for alphabet_num = 1:length(%(alphabet_name)s)
        disp(alphabet_num);
        disp(toc);
        for image_num = 1:length(%(alphabet_name)s(alphabet_num).original_images)
            %(alphabet_name)s(alphabet_num).original_images{image_num} = imresize(%(alphabet_name)s(alphabet_num).original_images{image_num}, [%(height)s, %(width)s]);
        end
        for image_num = 1:max(size(%(alphabet_name)s(alphabet_num).character_images))
            for user_num = 1:max(size(%(alphabet_name)s(alphabet_num).character_images{image_num}))
                %(alphabet_name)s(alphabet_num).character_images{image_num}{user_num} = imresize(%(alphabet_name)s(alphabet_num).character_images{image_num}{user_num}, [%(height)s, %(width)s]);
            end
        end
    end
end
""" % locals())
    rtn.append(r'clear alphabet_num image_num user_num;')
    with open(file_name, 'w') as f:
        f.write(''.join(rtn))

def format_for_matlab(object_):
    if object_ is None:
        return 'NaN'
    if isinstance(object_, int):
        return 'int32(' + str(object_) + ')'
    if isinstance(object_, str):
        return "'" + object_.replace("'", "''").replace('\n', '\\n') + "'"
    if isinstance(object_, list):
        return '{' + ', '.join(map(format_for_matlab, object_)) + '}'
    return str(object_)
    
##matlab_file = [matlab_header]
##
##matlab_file.append("""
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##%%                                                                           %%
##%%                                                                           %%
##%%                            Accepted Alphabets                             %%
##%%                                                                           %%
##%%                                                                           %%
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##
##""")
##
##print('Getting accepted alphabets...')
##alphabets = sorted(get_accepted_image_list().keys())
##for alphabet_num in range(len(alphabets)):
##    print('Accepted - %03d - %s' % (alphabet_num, alphabets[alphabet_num]))
##    matlab_file.append(make_matlab_segment(alphabets[alphabet_num], alphabet_num+1, 'accepted', get_accepted_ids, get_accepted_extra_info_file_name,
##                                           get_accepted_image_list, get_accepted_stroke_list))
##
##matlab_file.append(make_display_all_strokes('accepted'))
##
##
##matlab_file.append("""
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##%%                                                                           %%
##%%                                                                           %%
##%%                            Rejected Alphabets                             %%
##%%                                                                           %%
##%%                                                                           %%
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##
##""")
##
##print('Getting rejected alphabets...')
##alphabets = sorted(get_rejected_image_list().keys())
##for alphabet_num in range(len(alphabets)):
##    print('Rejected - %03d - %s' % (alphabet_num, alphabets[alphabet_num]))
##    matlab_file.append(make_matlab_segment(alphabets[alphabet_num], alphabet_num+1, 'rejected', get_rejected_ids, get_rejected_extra_info_file_name,
##                                           get_rejected_image_list, get_rejected_stroke_list))
##
##matlab_file.append(make_display_all_strokes('rejected'))
##
##
##matlab_file.append("""
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##%%                                                                           %%
##%%                                                                           %%
##%%                           Unreviewed Alphabets                            %%
##%%                                                                           %%
##%%                                                                           %%
##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##
##""")
##
##print('Getting unreviewed alphabets...')
##alphabets = sorted(get_unreviewed_image_list().keys())
##for alphabet_num in range(len(alphabets)):
##    print('Unreviewed - %03d - %s' % (alphabet_num, alphabets[alphabet_num]))
##    matlab_file.append(make_matlab_segment(alphabets[alphabet_num], alphabet_num+1, 'unreviewed', get_unreviewed_ids, get_unreviewed_extra_info_file_name,
##                                           get_unreviewed_image_list, get_unreviewed_stroke_list))
##
##matlab_file.append(make_display_all_strokes('unreviewed'))
##
##
##
##matlab_file.append(matlab_footer)
##
##with open(MATLAB_M_FILE_NAME, 'w') as f:
##    f.write(''.join(matlab_file))

def make_matlab_file(accepted_alphabets, rejected_alphabets, unreviewed_alphabets,
                     get_accepted_ids, get_rejected_ids, get_unreviewed_ids, file_name='results.mat'):
    counter = 0

    with open('m' + str(counter) + '.m', 'w') as f:
        f.write(matlab_header)
    counter += 1

    print('Getting accepted alphabets...')
##    alphabets = sorted(get_accepted_image_list().keys())
    alphabets = sorted(accepted_alphabets)
    for alphabet_num in range(len(alphabets)):
        print('Accepted - %03d - %s' % (alphabet_num, alphabets[alphabet_num]))
        append = make_matlab_segment(alphabets[alphabet_num], alphabet_num+1, 'accepted', get_accepted_ids, get_accepted_extra_info_file_name,
                                     get_accepted_image_list, get_accepted_stroke_list)
        with open('m' + str(counter) + '.m', 'w') as f:
            f.write(append)
        counter += 1

    if alphabets:
        with open('m' + str(counter) + '.m', 'w') as f:
            f.write(make_display_all_strokes('accepted'))
        counter += 1

    print('Getting rejected alphabets...')
##    alphabets = sorted(get_rejected_image_list().keys())
    alphabets = sorted(rejected_alphabets)
    for alphabet_num in range(len(alphabets)):
        print('Rejected - %03d - %s' % (alphabet_num, alphabets[alphabet_num]))
        append = make_matlab_segment(alphabets[alphabet_num], alphabet_num+1, 'rejected', get_rejected_ids, get_rejected_extra_info_file_name,
                                     get_rejected_image_list, get_rejected_stroke_list)
        with open('m' + str(counter) + '.m', 'w') as f:
            f.write(append)
        counter += 1

    if alphabets:
        with open('m' + str(counter) + '.m', 'w') as f:
            f.write(make_display_all_strokes('rejected'))
        counter += 1


    print('Getting unreviewed alphabets...')
##    alphabets = sorted(get_unreviewed_image_list().keys())
    alphabets = sorted(unreviewed_alphabets)
    for alphabet_num in range(len(alphabets)):
        print('Unreviewed - %03d - %s' % (alphabet_num, alphabets[alphabet_num]))
        append = make_matlab_segment(alphabets[alphabet_num], alphabet_num+1, 'unreviewed', get_unreviewed_ids, get_unreviewed_extra_info_file_name,
                                     get_unreviewed_image_list, get_unreviewed_stroke_list)
        with open('m' + str(counter) + '.m', 'w') as f:
            f.write(append)
        counter += 1

    if alphabets:
        with open('m' + str(counter) + '.m', 'w') as f:
            f.write(make_display_all_strokes('unreviewed'))
        counter += 1


    with open('m' + str(counter) + '.m', 'w') as f:
        f.write(matlab_footer)
    counter += 1

    matlab_type = 'matlab'
    matlab_command = '/mit/matlab/bin/matlab -r'
    use_matlab = True
    use_octave = False
    cmd = ''
    if 'octave' in sys.argv or '--octave' in sys.argv:
        matlab_command = 'octave --eval '
        #cmd = 'add octave; '
        use_octave = True
    ##else:
    ##    raise ValueError('incorrect matlab_command: ' + matlab_command)



    use_octave = not use_matlab

    cmd += 'pushd ~/web_scripts/alphabets/results/; ' + matlab_command + ' "save(\'results-temp.mat\'); '
    for i in range(counter):
        if i > 0 and i % 10 == 0:
            if use_octave:
                #cmd += "save('results-temp.mat', '-append'); exit;\"; " + matlab_command + " \"m0; "
                cmd += "save('results-temp.mat'); exit;\"; " + matlab_command + " \"load('results-temp.mat'); tic; "
            else:
                cmd += "save('results-temp.mat'); exit;\"; " + matlab_command + " \"load('results-temp.mat'); tic; "
        cmd += 'm' + str(i) + '; '
    if use_octave:
        #cmd += "save('results-temp.mat', '-append'); exit\"; rm results.mat; mv results-temp.mat results.mat; rm *.m; popd;" # '-append'
        cmd += "save('" + file_name + "'); exit\"; " # '-append'
    else:
        cmd += "save('" + file_name + "'); exit\"; " # '-append'
    if '--no-remove' in sys.argv or '--no-delete' in sys.argv:
        cmd += 'rm results-temp.mat; popd;'
    else:
        cmd += 'rm *.m; rm results-temp.mat; popd;'
    print(cmd)

    os.system(cmd)

def make_all_in_one_matlab(file_name='results.mat'):
    make_matlab_file(get_accepted_image_list().keys(), get_rejected_image_list().keys(), get_unreviewed_image_list().keys(),
                     get_accepted_ids, get_rejected_ids, get_unreviewed_ids, file_name=file_name)
    return [file_name]

def make_split_matlab_files(file_name_pattern='results_%02d.mat', split_by=5):
    accepted_ids = get_accepted_ids()
    accepted_image_list = get_accepted_image_list()
    num_ids = max(map(len, accepted_ids.values()))
    raw_input('There are %d ids.' % num_ids)
    rtn = []
    for mat_number in range(1 + (num_ids - 1) / split_by):
        accepted_alphabets = [alphabet for alphabet in accepted_image_list if len(accepted_image_list[alphabet].keys()) > mat_number * split_by]
        def local_get_accepted_ids(alphabet_id=None, id_=None):
            pre_rtn = get_accepted_ids(alphabet_id, id_)
            if alphabet_id is None:
                rtn = {}
                for alphabet_id in pre_rtn:
                    rtn[alphabet_id] = pre_rtn[alphabet_id][mat_number*split_by : (mat_number+1)*split_by]
                    if not rtn[alphabet_id]:
                        del rtn[alphabet_id]
            else:
                rtn = pre_rtn[mat_number*split_by : (mat_number+1)*split_by]
            return rtn
        def local_get_no_ids(alphabet_id=None, id_=None):
            if alphabet_id is None:
                return {}
            else:
                return []
        make_matlab_file(accepted_alphabets, [], [], local_get_accepted_ids, local_get_no_ids, local_get_no_ids, file_name=(file_name_pattern % mat_number))
        rtn.append(file_name_pattern % mat_number)
    return rtn

def padd_and_resize_images(orginal_file_name, new_file_name, delete_after=False):
    push_dir(os.path.expanduser('~/web_scripts/alphabets/results/'))
    make_matlab_padd('padd.m', ['accepted_alphabets', 'rejected_alphabets', 'unreviewed_alphabets', 'extra_alphabets'])
    make_matlab_resize('resize.m', ['accepted_alphabets', 'rejected_alphabets', 'unreviewed_alphabets', 'extra_alphabets'])

    matlab_type = 'matlab'
    matlab_command = '/mit/matlab/bin/matlab -r'
    use_matlab = True
    use_octave = False
    cmd = ''
    if 'octave' in sys.argv or '--octave' in sys.argv:
        matlab_command = 'octave --eval '
        #cmd = 'add octave; '
        use_octave = True
    ##else:
    ##    raise ValueError('incorrect matlab_command: ' + matlab_command)



    use_octave = not use_matlab

    cmd += matlab_command + " \"tic; load('" + orginal_file_name + "'); toc; padd; toc; resize; toc; save('" + \
           new_file_name + "'); exit\""
    print(cmd)

    os.system(cmd)
    if delete_after:
        os.remove('padd.m')
        os.remove('resize.m')
    pop_dir()

def remove_strokes_from_matlab_file(original_file_name, new_file_name, delete_after=False):
    push_dir(os.path.expanduser('~/web_scripts/alphabets/results/'))
    make_matlab_remove_strokes('remove_strokes.m', ['accepted_alphabets', 'rejected_alphabets', 'unreviewed_alphabets', 'extra_alphabets'])
    matlab_type = 'matlab'
    matlab_command = '/mit/matlab/bin/matlab -r'
    use_matlab = True
    use_octave = False
    cmd = ''
    if 'octave' in sys.argv or '--octave' in sys.argv:
        matlab_command = 'octave --eval '
        #cmd = 'add octave; '
        use_octave = True
    ##else:
    ##    raise ValueError('incorrect matlab_command: ' + matlab_command)



    use_octave = not use_matlab

    cmd += matlab_command + " \"tic; load('" + original_file_name + "'); toc; remove_strokes; toc; save('" + \
           new_file_name + "'); exit\""
    print(cmd)

    os.system(cmd)
    if delete_after:
        os.remove('remove_strokes.m')
    pop_dir()

##def remove_stroke_data(output

#todo: make files without strokes, with imresize to 28x28

if __name__ == '__main__':
    do_all = False
    try:
        do_all = do_all or 'a' == raw_input('Press enter to continue making initial matlab files...').lower()
        file_names = make_split_matlab_files()
    except KeyboardInterrupt:
        print('')
        file_names = sorted([i for i in glob.glob('*.mat') if '_28x28' not in i and '_no-strokes' not in i])
    for file_name in file_names:
        try:
            do_all = do_all or 'a' == raw_input('Press enter to continue for 28x28 for %s...' % file_name).lower()
            padd_and_resize_images(file_name, file_name.replace('.mat', '_28x28.mat'))
        except KeyboardInterrupt:
            print('')
        try:
            do_all = do_all or 'a' == raw_input('Press enter to continue for no-strokes for %s...' % file_name).lower()
            remove_strokes_from_matlab_file(file_name, file_name.replace('.mat', '_no-strokes.mat'))
        except KeyboardInterrupt:
            print('')
        try:
            do_all = do_all or 'a' == raw_input('Press enter to continue for 28x28 no-strokes for %s...' % file_name).lower()
            remove_strokes_from_matlab_file(file_name.replace('.mat', '_28x28.mat'), file_name.replace('.mat', '_28x28.mat').replace('.mat', '_no-strokes.mat'))
        except KeyboardInterrupt:
            print('')
