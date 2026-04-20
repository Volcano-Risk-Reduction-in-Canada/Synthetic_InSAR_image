function [filename_png, filename_tif, filename_mat] = save_interferogram( ...
    x, y, wrapped_radians, output_folder, ...
    source_name, Heading, Incidence, param1, param2, sample_id)

    if ~exist(output_folder, 'dir')
        mkdir(output_folder);
    end

    % Clean base filename (no weird decimals)


    base_name = sprintf('%s_%03d_heading_%d_inc_%d_p1_%.3g_p2_%.3g', ...
        lower(source_name), sample_id, Heading, Incidence, param1, param2);

    filename_png = fullfile(output_folder, [base_name '.png']);
    filename_tif = fullfile(output_folder, [base_name '.tif']);
    filename_mat = fullfile(output_folder, [base_name '.mat']);

    %% ---------------- PNG (nice visualization) ----------------
    fig = figure('Visible', 'off');

    imagesc(x/1000, y/1000, wrapped_radians);
    axis xy;
    axis image;
    colormap jet;
    caxis([-pi pi]);

    h = colorbar;
    ylabel(h, 'Radians');

    title(sprintf('%s | Heading %d | Inc %d | p1 %.3g | p2 %.3g', ...
        source_name, Heading, Incidence, param1, param2));

    xlabel('Easting (km)');
    ylabel('Northing (km)');

    exportgraphics(fig, filename_png, 'Resolution', 300);
    close(fig);

    %% ---------------- TIFF (image version) ----------------
    % Normalize for image storage
    tif_image = mat2gray(wrapped_radians);
    imwrite(tif_image, filename_tif);

    %% ---------------- MAT (true values) ----------------
    save(filename_mat, 'wrapped_radians', 'x', 'y');

end