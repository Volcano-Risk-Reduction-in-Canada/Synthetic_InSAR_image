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

        filename = save_interferogram(config.x, config.y, wrapped_radians, source_name, ...
            Heading, Incidence, param1, param2, config.output_folder);

        results(counter).filename = filename;
        results(counter).source_type = Source_Type;
        results(counter).source_name = source_name;
        results(counter).heading = Heading;
        results(counter).incidence = Incidence;
        results(counter).param1 = param1;
        results(counter).param2 = param2;

        counter = counter + 1;
    end
end

% generate_csv_result(results, config.output_folder)

disp('Done.')