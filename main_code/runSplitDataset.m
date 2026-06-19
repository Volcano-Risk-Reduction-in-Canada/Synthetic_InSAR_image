% Split combined interferogram chips into train/val/test subsets.
% Edit trainFrac and valFrac to change the ratio; testFrac is the remainder.
% Safe to re-run: output dirs are created fresh each time (existing files overwritten).

runConfig;

trainFrac = 0.70;
valFrac   = 0.15;
% testFrac  = 0.15  (implicit: 1 - trainFrac - valFrac)

splits = {'train', 'val', 'test'};
for s = splits
    mkdir([outputRoot, s{1}, '/wrap/combine/']);
    mkdir([outputRoot, s{1}, '/unwrap/combine/']);
end

allFiles = dir([outputRoot, 'all/unwrap/combine/*.mat']);
N = numel(allFiles);
if N == 0, error('No combined samples found in all/unwrap/combine/'); end

idx    = randperm(N);
nTrain = round(N * trainFrac);
nVal   = round(N * valFrac);

splitIdx = {idx(1:nTrain), idx(nTrain+1:nTrain+nVal), idx(nTrain+nVal+1:end)};

for s = 1:3
    for i = splitIdx{s}
        fname = allFiles(i).name;
        copyfile([outputRoot, 'all/unwrap/combine/', fname], ...
                 [outputRoot, splits{s}, '/unwrap/combine/', fname]);
        pngName = strrep(fname, '.mat', '.png');
        src = [outputRoot, 'all/wrap/combine/', pngName];
        if exist(src, 'file')
            copyfile(src, [outputRoot, splits{s}, '/wrap/combine/', pngName]);
        end
    end
    fprintf('  %s: %d samples\n', splits{s}, numel(splitIdx{s}));
end
fprintf('Total: %d samples split into train/val/test\n', N);
