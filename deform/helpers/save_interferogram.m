function filename = save_interferogram(x, y, wrapped_radians, source_name, ...
    Heading, Incidence, param1, param2, output_folder)

    if ~exist(output_folder, 'dir')
        mkdir(output_folder);
    end

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

    filename = fullfile(output_folder, sprintf( ...
        '%s_heading_%d_inc_%d_p1_%.3g_p2_%.3g.png', ...
        lower(source_name), Heading, Incidence, param1, param2));

    exportgraphics(fig, filename, 'Resolution', 300);

    close(fig);
end


