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
USE_RCM = false;

if USE_RCM
    % RCM (RADARSAT Constellation Mission) - C-band, 30 m resolution
    geom_x = -7500:30:(7500-30);
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

% Alias for combine step
rootDir = outputRoot;
