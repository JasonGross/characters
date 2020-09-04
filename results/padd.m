if exist('accepted_alphabets')
    for alphabet_num = 1:length(accepted_alphabets)
        disp(alphabet_num);
        disp(toc);
        for image_num = 1:length(accepted_alphabets(alphabet_num).original_images)
            [h, w] = size(accepted_alphabets(alphabet_num).original_images{image_num});
            if h > w
                padd0 = logical(zeros(h, floor((h - w) / 2)));
                padd1 = logical(zeros(h, ceil((h - w) / 2)));
                accepted_alphabets(alphabet_num).original_images{image_num} = [padd0, logical(accepted_alphabets(alphabet_num).original_images{image_num}), padd1];
            else
                padd0 = logical(zeros(floor((w - h) / 2), w));
                padd1 = logical(zeros(ceil((w - h) / 2), w));
                accepted_alphabets(alphabet_num).original_images{image_num} = [padd0; logical(accepted_alphabets(alphabet_num).original_images{image_num}); padd1];
            end
        end
        for image_num = 1:max(size(accepted_alphabets(alphabet_num).character_images))
            for user_num = 1:max(size(accepted_alphabets(alphabet_num).character_images{image_num}))
                [h, w] = size(accepted_alphabets(alphabet_num).character_images{image_num}{user_num});
                if h > w
                    padd0 = logical(zeros(h, floor((h - w) / 2)));
                    padd1 = logical(zeros(h, ceil((h - w) / 2)));
                    accepted_alphabets(alphabet_num).character_images{image_num}{user_num} = [padd0, logical(accepted_alphabets(alphabet_num).character_images{image_num}{user_num}), padd1];
                else
                    padd0 = logical(zeros(floor((w - h) / 2), w));
                    padd1 = logical(zeros(ceil((w - h) / 2), w));
                    accepted_alphabets(alphabet_num).character_images{image_num}{user_num} = [padd0; logical(accepted_alphabets(alphabet_num).character_images{image_num}{user_num}); padd1];
                end
            end
        end
    end
end
if exist('rejected_alphabets')
    for alphabet_num = 1:length(rejected_alphabets)
        disp(alphabet_num);
        disp(toc);
        for image_num = 1:length(rejected_alphabets(alphabet_num).original_images)
            [h, w] = size(rejected_alphabets(alphabet_num).original_images{image_num});
            if h > w
                padd0 = logical(zeros(h, floor((h - w) / 2)));
                padd1 = logical(zeros(h, ceil((h - w) / 2)));
                rejected_alphabets(alphabet_num).original_images{image_num} = [padd0, logical(rejected_alphabets(alphabet_num).original_images{image_num}), padd1];
            else
                padd0 = logical(zeros(floor((w - h) / 2), w));
                padd1 = logical(zeros(ceil((w - h) / 2), w));
                rejected_alphabets(alphabet_num).original_images{image_num} = [padd0; logical(rejected_alphabets(alphabet_num).original_images{image_num}); padd1];
            end
        end
        for image_num = 1:max(size(rejected_alphabets(alphabet_num).character_images))
            for user_num = 1:max(size(rejected_alphabets(alphabet_num).character_images{image_num}))
                [h, w] = size(rejected_alphabets(alphabet_num).character_images{image_num}{user_num});
                if h > w
                    padd0 = logical(zeros(h, floor((h - w) / 2)));
                    padd1 = logical(zeros(h, ceil((h - w) / 2)));
                    rejected_alphabets(alphabet_num).character_images{image_num}{user_num} = [padd0, logical(rejected_alphabets(alphabet_num).character_images{image_num}{user_num}), padd1];
                else
                    padd0 = logical(zeros(floor((w - h) / 2), w));
                    padd1 = logical(zeros(ceil((w - h) / 2), w));
                    rejected_alphabets(alphabet_num).character_images{image_num}{user_num} = [padd0; logical(rejected_alphabets(alphabet_num).character_images{image_num}{user_num}); padd1];
                end
            end
        end
    end
end
if exist('unreviewed_alphabets')
    for alphabet_num = 1:length(unreviewed_alphabets)
        disp(alphabet_num);
        disp(toc);
        for image_num = 1:length(unreviewed_alphabets(alphabet_num).original_images)
            [h, w] = size(unreviewed_alphabets(alphabet_num).original_images{image_num});
            if h > w
                padd0 = logical(zeros(h, floor((h - w) / 2)));
                padd1 = logical(zeros(h, ceil((h - w) / 2)));
                unreviewed_alphabets(alphabet_num).original_images{image_num} = [padd0, logical(unreviewed_alphabets(alphabet_num).original_images{image_num}), padd1];
            else
                padd0 = logical(zeros(floor((w - h) / 2), w));
                padd1 = logical(zeros(ceil((w - h) / 2), w));
                unreviewed_alphabets(alphabet_num).original_images{image_num} = [padd0; logical(unreviewed_alphabets(alphabet_num).original_images{image_num}); padd1];
            end
        end
        for image_num = 1:max(size(unreviewed_alphabets(alphabet_num).character_images))
            for user_num = 1:max(size(unreviewed_alphabets(alphabet_num).character_images{image_num}))
                [h, w] = size(unreviewed_alphabets(alphabet_num).character_images{image_num}{user_num});
                if h > w
                    padd0 = logical(zeros(h, floor((h - w) / 2)));
                    padd1 = logical(zeros(h, ceil((h - w) / 2)));
                    unreviewed_alphabets(alphabet_num).character_images{image_num}{user_num} = [padd0, logical(unreviewed_alphabets(alphabet_num).character_images{image_num}{user_num}), padd1];
                else
                    padd0 = logical(zeros(floor((w - h) / 2), w));
                    padd1 = logical(zeros(ceil((w - h) / 2), w));
                    unreviewed_alphabets(alphabet_num).character_images{image_num}{user_num} = [padd0; logical(unreviewed_alphabets(alphabet_num).character_images{image_num}{user_num}); padd1];
                end
            end
        end
    end
end
if exist('extra_alphabets')
    for alphabet_num = 1:length(extra_alphabets)
        disp(alphabet_num);
        disp(toc);
        for image_num = 1:length(extra_alphabets(alphabet_num).original_images)
            [h, w] = size(extra_alphabets(alphabet_num).original_images{image_num});
            if h > w
                padd0 = logical(zeros(h, floor((h - w) / 2)));
                padd1 = logical(zeros(h, ceil((h - w) / 2)));
                extra_alphabets(alphabet_num).original_images{image_num} = [padd0, logical(extra_alphabets(alphabet_num).original_images{image_num}), padd1];
            else
                padd0 = logical(zeros(floor((w - h) / 2), w));
                padd1 = logical(zeros(ceil((w - h) / 2), w));
                extra_alphabets(alphabet_num).original_images{image_num} = [padd0; logical(extra_alphabets(alphabet_num).original_images{image_num}); padd1];
            end
        end
        for image_num = 1:max(size(extra_alphabets(alphabet_num).character_images))
            for user_num = 1:max(size(extra_alphabets(alphabet_num).character_images{image_num}))
                [h, w] = size(extra_alphabets(alphabet_num).character_images{image_num}{user_num});
                if h > w
                    padd0 = logical(zeros(h, floor((h - w) / 2)));
                    padd1 = logical(zeros(h, ceil((h - w) / 2)));
                    extra_alphabets(alphabet_num).character_images{image_num}{user_num} = [padd0, logical(extra_alphabets(alphabet_num).character_images{image_num}{user_num}), padd1];
                else
                    padd0 = logical(zeros(floor((w - h) / 2), w));
                    padd1 = logical(zeros(ceil((w - h) / 2), w));
                    extra_alphabets(alphabet_num).character_images{image_num}{user_num} = [padd0; logical(extra_alphabets(alphabet_num).character_images{image_num}{user_num}); padd1];
                end
            end
        end
    end
end
clear padd0 padd1 h w size0 size1 cur_size alphabet_num image_num user_num;