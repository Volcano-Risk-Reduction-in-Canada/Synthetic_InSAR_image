function generate_csv_result(results, output_folder)
    T = struct2table(results);
    writetable(T, fullfile(output_folder, 'metadata.csv'));
end