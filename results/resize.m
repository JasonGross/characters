if exist('accepted_alphabets')
    for alphabet_num = 1:length(accepted_alphabets)
        disp(alphabet_num);
        disp(toc);
        for image_num = 1:length(accepted_alphabets(alphabet_num).original_images)
            accepted_alphabets(alphabet_num).original_images{image_num} = imresize(accepted_alphabets(alphabet_num).original_images{image_num}, [28, 28]);
        end
        for image_num = 1:max(size(accepted_alphabets(alphabet_num).character_images))
            for user_num = 1:max(size(accepted_alphabets(alphabet_num).character_images{image_num}))
                accepted_alphabets(alphabet_num).character_images{image_num}{user_num} = imresize(accepted_alphabets(alphabet_num).character_images{image_num}{user_num}, [28, 28]);
            end
        end
    end
end
if exist('rejected_alphabets')
    for alphabet_num = 1:length(rejected_alphabets)
        disp(alphabet_num);
        disp(toc);
        for image_num = 1:length(rejected_alphabets(alphabet_num).original_images)
            rejected_alphabets(alphabet_num).original_images{image_num} = imresize(rejected_alphabets(alphabet_num).original_images{image_num}, [28, 28]);
        end
        for image_num = 1:max(size(rejected_alphabets(alphabet_num).character_images))
            for user_num = 1:max(size(rejected_alphabets(alphabet_num).character_images{image_num}))
                rejected_alphabets(alphabet_num).character_images{image_num}{user_num} = imresize(rejected_alphabets(alphabet_num).character_images{image_num}{user_num}, [28, 28]);
            end
        end
    end
end
if exist('unreviewed_alphabets')
    for alphabet_num = 1:length(unreviewed_alphabets)
        disp(alphabet_num);
        disp(toc);
        for image_num = 1:length(unreviewed_alphabets(alphabet_num).original_images)
            unreviewed_alphabets(alphabet_num).original_images{image_num} = imresize(unreviewed_alphabets(alphabet_num).original_images{image_num}, [28, 28]);
        end
        for image_num = 1:max(size(unreviewed_alphabets(alphabet_num).character_images))
            for user_num = 1:max(size(unreviewed_alphabets(alphabet_num).character_images{image_num}))
                unreviewed_alphabets(alphabet_num).character_images{image_num}{user_num} = imresize(unreviewed_alphabets(alphabet_num).character_images{image_num}{user_num}, [28, 28]);
            end
        end
    end
end
if exist('extra_alphabets')
    for alphabet_num = 1:length(extra_alphabets)
        disp(alphabet_num);
        disp(toc);
        for image_num = 1:length(extra_alphabets(alphabet_num).original_images)
            extra_alphabets(alphabet_num).original_images{image_num} = imresize(extra_alphabets(alphabet_num).original_images{image_num}, [28, 28]);
        end
        for image_num = 1:max(size(extra_alphabets(alphabet_num).character_images))
            for user_num = 1:max(size(extra_alphabets(alphabet_num).character_images{image_num}))
                extra_alphabets(alphabet_num).character_images{image_num}{user_num} = imresize(extra_alphabets(alphabet_num).character_images{image_num}{user_num}, [28, 28]);
            end
        end
    end
end
clear alphabet_num image_num user_num;