% Ploting 3D data based on the galactic positions provided in harris I, Krause, vdb


% constants

const r0_kpc = 8.0; % 8) "Distance from Galactic center (kpc), assuming R_0=8.0 kpc" Harris one





% Settings, Should be obvious w/ the names 
limitsKpc = [20, 100];
saveFigures = true;
style.widthCm = 24;
style.heightCm = 21;
style.fontSize = 10;
style.markerSize = 30;                  
style.colormap = parula(256);
style.noDataColour = [0.78 0.78 0.78]; % edge case, dataNA, grey
style.edgeColour = [0.20 0.20 0.20]; % outline of points
style.guideColour = [0.45 0.45 0.45]; % sun's orbit around smbh, mid grey
style.centreStyle = {'k+', 'MarkerSize', 10, 'LineWidth', 1.5}; % SMBH
style.sunStyle = {'o', 'MarkerSize', 7, 'MarkerFaceColor', [1 0.85 0], 'MarkerEdgeColor', 'k'}; % sun yellow
style.dpi = 300; % resolution 
scriptDir = fileparts(mfilename('fullpath'));
dataHi = fullfile(scriptDir, 'dataset/HarrisPartI.csv');
dataHiii = fullfile(scriptDir, 'dataset/HarrisPartIII.csv');
dataVDB = fullfile(scriptDir, 'dataset/vanDenBergh_table2.csv');
dataKrause = fullfile(scriptDir, 'dataset/Krause21.csv');
% code: Fe/H
clusters = readCsvTyped(dataHi, ["ID", "Name", "RA", "DEC"]);
krause = readCsvTyped(dataKrause, ["Class", "Object", "AltName"]);

% Literally the worst dataset in human existence
vdb = readCsvTyped(dataVDB,  ["#NGC", "Name", "Method", "Figs", "Range"]);
vdb = renamevars(vdb, ["#NGC", "NGC"]);
vdbName = vdb.Name;
isNGC = vdb.NGC ~= "XXXX"; % why? just dont include them.
vdbName(isNGC) = "NGC" + vdb.NGC(isNGC);


clusters.key = clusterKey(clusters.ID);
krause.key   = clusterKey(krause.Object);
vdb.key = clusterKey(vdbName);

% edge case
unmatched = [setdiff(krause.key, clusters.key); setdiff(vdb.key, clusters.key)]; % check fault


[inVdb, iVdb]       = ismember(clusters.key, vdb.key);
[inKrause, iKrause] = ismember(clusters.key, krause.key);
clusters.FeH(inVdb)    = vdb.FeH(iVdb(inVdb));
clusters.FeH(inKrause) = krause.FeH(iKrause(inKrause));

% coord from rgc