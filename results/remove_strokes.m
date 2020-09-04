if exist('accepted_alphabets')
        accepted_alphabets = rmfield(accepted_alphabets, 'character_xss');    accepted_alphabets = rmfield(accepted_alphabets, 'character_yss');    accepted_alphabets = rmfield(accepted_alphabets, 'character_tss');    accepted_alphabets = rmfield(accepted_alphabets, 'character_time_strokes');
end
if exist('rejected_alphabets')
        rejected_alphabets = rmfield(rejected_alphabets, 'character_xss');    rejected_alphabets = rmfield(rejected_alphabets, 'character_yss');    rejected_alphabets = rmfield(rejected_alphabets, 'character_tss');    rejected_alphabets = rmfield(rejected_alphabets, 'character_time_strokes');
end
if exist('unreviewed_alphabets')
        unreviewed_alphabets = rmfield(unreviewed_alphabets, 'character_xss');    unreviewed_alphabets = rmfield(unreviewed_alphabets, 'character_yss');    unreviewed_alphabets = rmfield(unreviewed_alphabets, 'character_tss');    unreviewed_alphabets = rmfield(unreviewed_alphabets, 'character_time_strokes');
end
if exist('extra_alphabets')
        extra_alphabets = rmfield(extra_alphabets, 'character_xss');    extra_alphabets = rmfield(extra_alphabets, 'character_yss');    extra_alphabets = rmfield(extra_alphabets, 'character_tss');    extra_alphabets = rmfield(extra_alphabets, 'character_time_strokes');
end
clear alphabet_num show_all_accepted_strokes show_all_rejected_strokes show_all_strokes show_all_unreviewed_strokes show_all_extra_strokes;