from networkx import dispersion

import utils.toolChain as tc
import numpy as np
import pandas as pd


def run_plots(dataset, PLOT_WIDTH, PLOT_HEIGHT):

    # Velocity dispersion - Mass. Added colour coding with half light radius.
    tc.plot_scatter(
        dataset=dataset,
        x="Mstar",
        y="sig_v",
        color="r_h",
        colorbar_label="Half light radius (pc)",
        xlabel="log(Mass) (log(M_sun))",
        ylabel="Velocity Dispersion (km/s)",
        title="Velocity Dispersion-Mass Relation with Half Light Radius",
        filename="mstar_v_sigv.png",
        xscale="log",
        PLOT_WIDTH=PLOT_WIDTH,
        PLOT_HEIGHT=PLOT_HEIGHT,
    )

    # FeH - Galactocentric distance, coloured by age.
    tc.plot_scatter(
        dataset=dataset,
        x="R_gc",
        y="FeH_Krause",
        color="Age_Krause",
        colorbar_label="Age (Gyr)",
        xlabel="Galactocentric Distance (kpc)",
        ylabel="Metallicity [Fe/H]",
        title="Metallicity-Galactocentric Distance with Age for Krause Clusters",
        filename="feh_rgc_age.png",
        xscale="linear",
        PLOT_WIDTH=PLOT_WIDTH,
        PLOT_HEIGHT=PLOT_HEIGHT,
    )

    # Plot of Age vs FeH for only Krause to identify two branches. Coloured by Galactocentric distance.
    # Plot with color representing Galactocentric distance as a nice way to visualize the data.
    tc.plot_scatter(
        dataset=dataset,
        x="FeH_Krause",
        y="Age_Krause",
        color="R_gc",
        colorbar_label="Galactocentric Distance $R_{gc}$ (kpc)",
        xlabel="Metallicity [Fe/H]",
        ylabel="Age (Gyr)",
        title="Krause Age-Metallicity Relation with Galactocentric Distance",
        label="Krause Clusters",
        filename="krause_age_feh.png",
        xscale="linear",
        PLOT_WIDTH=PLOT_WIDTH,
        PLOT_HEIGHT=PLOT_HEIGHT,
    )

    # Plot of Age vs FeH for only van den Berg to identify two branches. Coloured by Galactocentric distance.rg Clusters",
    tc.plot_scatter(
        dataset=dataset,
        x="FeH_vandenBerg",
        y="Age_vandenBerg",
        color="R_gc",
        colorbar_label="Galactocentric Distance $R_{gc}$ (kpc)",
        xlabel="Metallicity [Fe/H]",
        ylabel="Age (Gyr)",
        title="van den Berg Age-Metallicity Relation with Galactocentric Distance",
        filename="vandenberg_age_feh.png",
        xscale="linear",
        PLOT_WIDTH=PLOT_WIDTH,
        PLOT_HEIGHT=PLOT_HEIGHT,
    )

    # Radial velocity LSR vs Galactocentric distance coloured by Krause metallicities.
    tc.plot_scatter(
        dataset=dataset,
        x="R_gc",
        y="v_LSR",
        color="FeH_Krause",
        colorbar_label="Metallicity [Fe/H]",
        xlabel="Galactocentric Distance $R_{gc}$ (kpc)",
        ylabel="Radial Velocity $v_{LSR}$ (km/s)",
        title="Radial Velocity vs Galactocentric Distance with Krause Metallicity",
        filename="rv_vs_rgc.png",
        xscale="linear",
        PLOT_WIDTH=PLOT_WIDTH,
        PLOT_HEIGHT=PLOT_HEIGHT,
    )

    # Half light radius vs galactocentric distance coloured by krause metallicities.
    tc.plot_scatter(
        dataset=dataset,
        x="R_gc",
        y="r_h",
        color="FeH_Krause",
        colorbar_label="Metallicity [Fe/H]",
        xlabel="Galactocentric Distance $R_{gc}$ (kpc)",
        ylabel="Half Light Radius $r_h$ (pc)",
        title="Half Light Radius vs Galactocentric Distance with Krause Metallicity",
        filename="rh_vs_rgc.png",
        xscale="linear",
        PLOT_WIDTH=PLOT_WIDTH,
        PLOT_HEIGHT=PLOT_HEIGHT,
    )

    # Core relaxation time vs galactocentric distance coloured by krause age.
    tc.plot_scatter(
        dataset=dataset,
        x="R_gc",
        y="lg_tc",
        color="Age_Krause",
        colorbar_label="Age (Gyr)",
        xlabel="Galactocentric Distance $R_{gc}$ (kpc)",
        ylabel="Core Relaxation Time $lg_{tc}$",
        title="Core Relaxation Time vs Galactocentric Distance with Krause Age",
        filename="trc_vs_rgc.png",
        xscale="linear",
        PLOT_WIDTH=PLOT_WIDTH,
        PLOT_HEIGHT=PLOT_HEIGHT,
    )

    # Concentration vs velocity dispersion coloured by krause metallicities
    tc.plot_scatter(
        dataset=dataset,
        x="c",
        y="sig_v",
        color="FeH_Krause",
        colorbar_label="Metallicity [Fe/H]",
        xlabel="Concentration $c$",
        ylabel="Velocity Dispersion $\sigma_v$ (km/s)",
        title="Concentration vs Velocity Dispersion with Krause Metallicity",
        filename="c_vs_sigv.png",
        xscale="linear",
        PLOT_WIDTH=PLOT_WIDTH,
        PLOT_HEIGHT=PLOT_HEIGHT,
    )

    # Harris S0.5
    radial_velocity = "v_r"
    dispersion = "sig_v"
    for i in dataset["sig_v"]:
        if pd.isna(i):
            dataset["sig_v"].fillna(0, inplace=True)
    tc.compute_s0_5(dataset, radial_velocity, dispersion)
    print(dataset["S_0.5"])
