% Ploting 3D data based on the galactic positions provided in harris I, Krause, vdb


% constants

r0_kpc = 8.0; % 8) "Distance from Galactic center (kpc), assuming R_0=8.0 kpc" Harris one

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
dataVDB = fullfile(scriptDir, 'dataset/vandenBerg_table2.csv');
dataKrause = fullfile(scriptDir, 'dataset/Krause21.csv');
% code: Fe/H
clusters = readCsv(dataHi, ["ID", "Name", "RA", "DEC"]);
krause = readCsv(dataKrause, ["Class", "Object", "AltName"]);

% Literally the worst dataset in human existence
vdb = readCsv(dataVDB,  ["#NGC", "Name", "Method", "Figs", "Range"]);
vdb = renamevars(vdb, "#NGC", "NGC");
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

clusters.xGC_kpc = clusters.X - r0_kpc; % X is heliocentric
clusters.yGC_kpc = clusters.Y;
clusters.zGC_kpc = clusters.Z;
% どうして　どうして　どうして　どうして
% plot
outDir = fullfile(scriptDir, "xyz_figures");
for L = limitsKpc
    fig = plotXYZ(clusters, r0_kpc, L, style);
    if saveFigures
        if ~isfolder(outDir)
            mkdir(outDir);
        end
        file = fullfile(outDir, sprintf("xyz_within_%gkpc.png", L));
        exportgraphics(fig, file, 'Resolution', style.dpi);
    end
end

% func

function fig = plotXYZ(clusters, R0, L, style)
    x = clusters.xGC_kpc;
    y = clusters.yGC_kpc;
    z = clusters.zGC_kpc;
    c = clusters.FeH;
    hasColour = ~isnan(c);
    outside   = any(abs([x, y, z]) > L, 2);  
    fig = figure('Color', 'w', 'Units', 'centimeters', ...
    'Position', [2, 2, style.widthCm, style.heightCm], ...
    'Name', sprintf('position (+/- %g kpc)', L));
    colormap(fig, style.colormap);
    layout = tiledlayout(fig, 2, 2, 'TileSpacing', 'compact', 'Padding', 'compact');
    axs = gobjects(4, 1);

    % 2d proj
    twodPlanes = {x, y, "x (kpc)", "y (kpc)", [-R0, 0], "(x-y)"
          x, z,"x (kpc)", "z (kpc)", [-R0, 0], "(x-z)"
          y,z,"y (kpc)", "z (kpc)", [],"(y-z)"};
 
    for k = 1:3
        axs(k) = nexttile(layout);
        h = drawProjection(axs(k), twodPlanes{k, 1}, twodPlanes{k, 2}, c, hasColour, ...
            twodPlanes{k, 5}, L, style);
        xlabel(axs(k), twodPlanes{k, 3});
        ylabel(axs(k), twodPlanes{k, 4});
        title(axs(k), twodPlanes{k, 6}, 'FontWeight', 'normal');
    
        if k == 1 
            circle = plot(axs(k), R0*cosd(0:360), R0*sind(0:360), ':', ...
                'Color', style.guideColour, 'DisplayName', 'Solar Path');
            uistack(circle, 'bottom');
            legendHandles = [h, circle];
        else            % edge-on: mark the Galactic plane
            yline(axs(k), 0, ':', 'Color', style.guideColour, 'HandleVisibility', 'off');
        end
    end
    ax = nexttile(layout);
    axs(4) = ax;
    hold(ax, 'on');
    scatter3(ax, x(~hasColour), y(~hasColour), z(~hasColour), style.markerSize, ...
        style.noDataColour, 'filled');
    scatter3(ax, x(hasColour), y(hasColour), z(hasColour), style.markerSize, ...
        c(hasColour), 'filled', 'MarkerEdgeColor', style.edgeColour, 'LineWidth', 0.3);
    plot3(ax, R0*cosd(0:360), R0*sind(0:360), zeros(1, 361), ':', 'Color', style.guideColour);
    plot3(ax, 0, 0, 0, style.centreStyle{:});
    plot3(ax, -R0, 0, 0, style.sunStyle{:});
    view(ax, -37.5, 20);
    axis(ax, 'equal');
    xlim(ax, [-L, L]);
    ylim(ax, [-L, L]);
    zlim(ax, [-L, L]);
    ticks = linspace(-L, L, 5);                 
    set(ax, 'XTick', ticks, 'YTick', ticks, 'ZTick', ticks);
    grid(ax, 'on');
    box(ax, 'on');
    xlabel(ax, 'x (kpc)');
    ylabel(ax, 'y (kpc)');
    zlabel(ax, 'z (kpc)');
    title(ax, '3-D view (rotatable in MATLAB)', 'FontWeight', 'normal');
    set(ax, 'FontSize', style.fontSize);
    
    if any(hasColour)
        cLim = [min(c(hasColour)), max(c(hasColour))];
        if diff(cLim) == 0
            cLim = cLim + [-0.5, 0.5];
        end
        set(axs, 'CLim', cLim);
        cb = colorbar(axs(4));
        cb.Layout.Tile = 'east';
        cb.Label.String = '[Fe/H]';
    end
    
    lgd = legend(axs(1), legendHandles, 'Orientation', 'horizontal', ...
    'FontSize', style.fontSize);
    lgd.Layout.Tile = 'south';
 
    title(layout, { ...
    sprintf('MGC Plot (Harris X, Y, Z): %d shown, %d beyond \\pm%g kpc', ...
        nnz(~outside), nnz(outside), L), ...
    sprintf('rgc, R_0 = %g kpc; shows [Fe/H] for %d of %d clusters', ...
        R0, nnz(hasColour), height(clusters))}, ...
    'FontSize', style.fontSize + 1);
    
end

function h = drawProjection(ax, a, b, c, hasColour, sunPos, L, style)

    hold(ax, 'on');
    h = gobjects(1, 0);
    if any(~hasColour)
        h(end+1) = scatter(ax, a(~hasColour), b(~hasColour), style.markerSize, ...
            style.noDataColour, 'filled', 'DisplayName', 'No [Fe/H]');
    end
    h(end+1) = scatter(ax, a(hasColour), b(hasColour), style.markerSize, ...
        c(hasColour), 'filled', 'MarkerEdgeColor', style.edgeColour, ...
        'LineWidth', 0.3, 'DisplayName', 'With [Fe/H]');
    h(end+1) = plot(ax, 0, 0, style.centreStyle{:}, 'DisplayName', 'rgc');
    if ~isempty(sunPos)
        h(end+1) = plot(ax, sunPos(1), sunPos(2), style.sunStyle{:}, 'DisplayName', 'Sun');
    end
    axis(ax, 'equal');
    xlim(ax, [-L, L]);
    ylim(ax, [-L, L]);
    grid(ax, 'on');
    box(ax, 'on');
    set(ax, 'FontSize', style.fontSize);
end

function T = readCsv(file, textVars)

    arguments
        file (1,1) string {mustBeFile}
        textVars (1,:) string = strings(1, 0)
    end
    opts = detectImportOptions(file, 'TextType', 'string', ...
        'VariableNamingRule', 'preserve', 'Encoding', 'UTF-8');
    allVars = string(opts.VariableNames);
    unknown = setdiff(textVars, allVars);
    if ~isempty(unknown)
        error('plot_galactic_xyz:unknownColumn', 'Column(s) "%s" not found in %s.', ...
            strjoin(unknown(:)', '", "'), file);
    end
    numVars = setdiff(allVars, textVars, 'stable');
    if ~isempty(textVars)
        opts = setvartype(opts, textVars, 'string');
    end
    opts = setvartype(opts, numVars, 'double');
    opts = setvaropts(opts, numVars, 'TreatAsMissing', {'NA'});
    T = readtable(file, opts);
end

function key = clusterKey(names)
%   Harris: "Palomar12" to "PAL12", "Ruprecht106" -> "RUP106",
    arguments
        names string
    end
    key = upper(regexprep(strtrim(names), '[\s_]', ''));
    key = regexprep(key, '^PALOMAR', 'PAL');
    key = regexprep(key, '^RUPRECHT', 'RUP');
    key = regexprep(key, '^TER(?!ZAN)', 'TERZAN');
end

