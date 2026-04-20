%% Run full synthetic interferogram generation pipeline
% Generates deformation, turbulent, stratified, and combined interferograms.
% Edit runConfig.m to set output paths and options.

clear; clc;

%% Load config and add paths
scriptDir = fileparts(mfilename('fullpath'));
cd(scriptDir);
runConfig;
addpath(fullfile(fileparts(mfilename('fullpath')), '..', 'deform'));
addpath(fullfile(fileparts(mfilename('fullpath')), '..', 'turbulent'));
addpath(fullfile(fileparts(mfilename('fullpath')), '..', 'stratify'));

fprintf('Output root: %s\n', outputRoot);
if USE_RCM, geomStr = 'RCM (30m)'; else, geomStr = 'Original (Sentinel-1, 100m)'; end
fprintf('Geometry: %s\n', geomStr);
fprintf('Skip stratified: %d\n\n', SKIP_STRATIFIED);

%% Step 1: Deformation
fprintf('=== Step 1/4: Generating deformation patches ===\n');
run('runGenDeformation.m');
fprintf('Done.\n\n');

%% Step 2: Turbulent atmosphere
fprintf('=== Step 2/4: Generating turbulent atmosphere ===\n');
run('runGenTurbulent.m');
fprintf('Done.\n\n');

%% Step 3: Stratified atmosphere
if SKIP_STRATIFIED
    fprintf('=== Step 3/4: Generating placeholder stratified (zeros) ===\n');
    % Create stratified dirs and zero .mat files so combine step has inputs
    halfcrop = floor(227/2);
    for setnum = 1:2
        outDir = [outputRoot, 'set', num2str(setnum), filesep, 'unwrap', filesep, 'stratified', filesep];
        mkdir(outDir);
        deformList = dir([outputRoot, 'set', num2str(setnum), filesep, 'unwrap', filesep, 'deform', filesep, '*.mat']);
        nNeed = min(length(deformList), 10000);
        for k = 1:nNeed
            atmo = ones(227, 227) * 1e-10;  % placeholder (tiny non-zero so mask works)
            save([outDir, 'S', sprintf('%05d', k), '.mat'], 'atmo');
        end
        fprintf('  Set %d: created %d placeholder stratified patches\n', setnum, nNeed);
    end
    fprintf('Done.\n\n');
else
    fprintf('=== Step 3/4: Generating stratified atmosphere (GACOS) ===\n');
    run('runGenStratified.m');
    fprintf('Done.\n\n');
end

%% Step 4: Combine signals
fprintf('=== Step 4/4: Combining D + S + T into interferograms ===\n');
run('runGenCombineSignals.m');
fprintf('Done.\n\n');

fprintf('=== Pipeline complete ===\n');
fprintf('Output in: %s\n', outputRoot);
