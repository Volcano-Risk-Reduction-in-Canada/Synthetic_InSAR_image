%%%%% Script to produce simulated interferograms using simple elastic
%%%%% sources for Earthquakes, Dykes, Sills and point pressure changes at Magma
%%%%% Chambers
%
% Tim J Wright, University of Leeds, 12 August 2009
% t.wright@see.leeds.ac.uk
%
% Note, the script produces wrapped and unwrapped simulations on a 50x50 km
% grid, with the fault/volcano located at the grid centre.
%
% Requires the following additional files:
%
% disloc3d4.m
% dc3d4.m
% dc3d5.m
% dc3d6.m
% penny.m
% Q.m
% RtWt.m
% fpkernel.m
% fredholm.m
% intgr.m
% rngchn_mogi.m
%
% This script and the subroutines will also run in GNU Octave, but some
% minor modifications will be required to the lines that plot the data at
% the bottom of the script (e.g. quiver and colorbar are not functions in
% octave).
%
%%%%%%%%%%%%%%
clear; clc; close all;

script_dir = fileparts(mfilename('fullpath'));
addpath(script_dir);
addpath(fullfile(script_dir, 'params'));
addpath(fullfile(script_dir, 'helpers'));

config = main_dataset();

results = struct([]);
counter = 1;

for Source_Type = 1:5

    disp(['Generating Source Type ', num2str(Source_Type)])

    for n = 1:config.num_samples_per_type

        % Empty structs for unused source types
        Quake = struct();
        Dyke = struct();
        Sill = struct();
        Mogi = struct();
        Penny = struct();

        % Get only the active source parameters
        [source_struct, source_name, param1, param2] = generate_source_params(Source_Type);

        % Put source_struct into the correct variable
        switch Source_Type
            case 1
                Quake = source_struct;
            case 2
                Dyke = source_struct;
            case 3
                Sill = source_struct;
            case 4
                Mogi = source_struct;
            case 5
                Penny = source_struct;
        end

        % Get heading and incidence separately
        [Heading, Incidence] = generate_geometry();

        % Run model
        [los_grid_wrap, los_grid] = generateDeformation(Source_Type, ...
            config.x, config.y, Quake, Dyke, Sill, Mogi, Penny, Heading, Incidence);


        wrapped_radians = los_grid_wrap / 0.028333 * 2*pi - pi;

        [num_fringes, detectable, max_disp, min_disp, disp_range] = ...
            compute_fringe_count(los_grid);


        [filename_png, filename_tif, filename_mat] = save_interferogram( ...
            config.x, config.y, wrapped_radians, config.output_folder, ...
            source_name, Heading, Incidence, param1, param2, n);
        
        % Metadata
        results(counter).filename_png = filename_png;
        results(counter).filename_tif = filename_tif;
        results(counter).filename_mat = filename_mat;

        results(counter).source_type = Source_Type;
        results(counter).source_name = source_name;
        results(counter).heading = Heading;
        results(counter).incidence = Incidence;
        results(counter).param1 = param1;
        results(counter).param2 = param2;

        results(counter).max_displacement = max_disp;
        results(counter).min_displacement = min_disp;
        results(counter).displacement_range = disp_range;
        results(counter).num_fringes = num_fringes;
        results(counter).detectable = detectable;

        % Source-specific metadata
        switch Source_Type
            case 1
                if isfield(Quake, 'Depth'), results(counter).depth_km = Quake.Depth; end
                if isfield(Quake, 'Slip'), results(counter).slip_m = Quake.Slip; end
            case 2
                results(counter).strike_deg = Dyke.Strike;
                results(counter).dip_deg = Dyke.Dip;
                results(counter).opening_m = Dyke.Opening;
                results(counter).top_depth_km = Dyke.Top_depth;
                results(counter).bottom_depth_km = Dyke.Bottom_depth;
                results(counter).length_km = Dyke.Length;
            case 3
                if isfield(Sill, 'Depth'), results(counter).depth_km = Sill.Depth; end
                if isfield(Sill, 'Radius'), results(counter).radius_km = Sill.Radius; end
            case 4
                if isfield(Mogi, 'Depth'), results(counter).depth_km = Mogi.Depth; end
                if isfield(Mogi, 'Volume_Change'), results(counter).volume_change = Mogi.Volume_Change; end
            case 5
                if isfield(Penny, 'Depth'), results(counter).depth_km = Penny.Depth; end
                if isfield(Penny, 'Radius'), results(counter).radius_km = Penny.Radius; end
                if isfield(Penny, 'Pressure_Change'), results(counter).pressure_change = Penny.Pressure_Change; end
        end
        counter = counter + 1;
    end
end

% generate_csv_result(results, config.output_folder)

disp('Done.')