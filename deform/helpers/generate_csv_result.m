function generate_csv_result(results, output_folder)
    if ~exist(output_folder, 'dir')
        mkdir(output_folder)
    end
    
    T = struct2table(results);
    writetable(T, fullfile(output_folder, 'metadata.csv'));
end