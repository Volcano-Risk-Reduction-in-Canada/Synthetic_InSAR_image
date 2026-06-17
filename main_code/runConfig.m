%% Central configuration for synthetic interferogram pipeline
% Edit these paths for your system. Used by runFullPipeline and individual scripts.

% Output directory for all generated data (deform, turbulent, stratified, combine)
outputRoot = fullfile(fileparts(mfilename('fullpath')), '..', 'output', 'synthesised_patches', filesep);

% Input directory for GACOS stratified data (only needed if SKIP_STRATIFIED = false)
% Expect: inputRoot/volcano_name/*.ztd and *.ztd.rsc
inputRoot = fullfile(fileparts(mfilename('fullpath')), '..', 'gacos_data', 'volcano_2018', filesep);

% Set true to skip stratified generation and use zeros (when GACOS data unavailable)
SKIP_STRATIFIED = true;

% ========== GEOMETRY: Set true for RCM, false for original (Sentinel-1) ==========
USE_RCM = true;

if USE_RCM
    % RCM 5M beam mode — 5m native, downsampled to 15m effective resolution
    % Simulation grid: 1600x1600 pixels (~24km), center-cropped to chipSize
    geom_x = -12000:15:(12000-15);
    geom_y = geom_x;
    geom_wavelength = 0.05405;
    geom_incidence = 35;
    geom_Heading_list = 192;
    geom_Incidence_list = 35;
else
    % Original (Sentinel-1 style) - 100 m resolution
    geom_x = -25000:100:25000-100;
    geom_y = geom_x;
    geom_wavelength = 0.055465;
    geom_incidence = 43.7835;
    geom_Heading_list = 5:40:330;
    geom_Incidence_list = 33;
end

% ========== CHIP SIZE (SwinV2 input; must be divisible by 32) ==========
chipSize = 512;           % 512x512 px @ 15m = 7.68km footprint
halfcrop = chipSize / 2;  % use as (-halfcrop:halfcrop-1) to get exactly chipSize pixels

% Alias for combine step
rootDir = outputRoot;
