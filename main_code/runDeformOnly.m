%% Generate deformation-only synthetic interferograms (no atmosphere)
% Outputs wrapped PNGs to output/synthesised_patches/set{1,2}/wrap/deform/
% and unwrapped .mat files to .../unwrap/deform/
%
% Edit runConfig.m to change geometry, chip size, or source type.
% Run this script instead of runFullPipeline.m when you want clean
% deformation signal without turbulent or stratified atmosphere.

clear; clc;
scriptDir = fileparts(mfilename('fullpath'));
cd(scriptDir);
runConfig;
addpath(fullfile(scriptDir, '..', 'deform'));

fprintf('Output root: %s\n', outputRoot);
fprintf('Geometry: RCM 5M beam (15m effective), chip size: %dx%d\n', chipSize, chipSize);
fprintf('SAVEWRAP: %d\n\n', SAVEWRAP);

fprintf('=== Generating deformation patches ===\n');
run('runGenDeformation.m');
fprintf('Done.\n');
fprintf('Wrapped PNGs: %sset{1,2}/wrap/deform/\n', outputRoot);
fprintf('Unwrapped .mat: %sset{1,2}/unwrap/deform/\n', outputRoot);
