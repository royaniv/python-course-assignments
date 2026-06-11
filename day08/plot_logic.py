from html import escape

PLOT_WIDTH = 720
PLOT_HEIGHT = 430
PLOT_LEFT = 85
PLOT_RIGHT = 30
PLOT_TOP = 40
PLOT_BOTTOM = 75


def make_plot_svg(found_compounds):
    if len(found_compounds) == 0:
        return ""

    tpsas = [compound["tpsa"] for compound in found_compounds]
    xlogps = [compound["xlogp"] for compound in found_compounds]

    min_tpsa = min(tpsas)
    max_tpsa = max(tpsas)
    min_xlogp = min(xlogps)
    max_xlogp = max(xlogps)

    tpsa_range = max(max_tpsa - min_tpsa, 1)
    xlogp_range = max(max_xlogp - min_xlogp, 1)
    min_tpsa -= tpsa_range * 0.1
    max_tpsa += tpsa_range * 0.1
    min_xlogp -= xlogp_range * 0.1
    max_xlogp += xlogp_range * 0.1

    plot_width = PLOT_WIDTH - PLOT_LEFT - PLOT_RIGHT
    plot_height = PLOT_HEIGHT - PLOT_TOP - PLOT_BOTTOM
    x_axis_y = PLOT_HEIGHT - PLOT_BOTTOM
    points = ""

    for compound in found_compounds:
        x = PLOT_LEFT + (compound["tpsa"] - min_tpsa) / (max_tpsa - min_tpsa) * plot_width
        y = PLOT_TOP + (max_xlogp - compound["xlogp"]) / (max_xlogp - min_xlogp) * plot_height
        name = escape(compound["name"])

        points += (
            f'<circle class="plot-point" cx="{x:.1f}" cy="{y:.1f}" r="5">'
            f"<title>{name}</title></circle>\n"
        )

    return f"""
    <div class="plot-box">
        <h3>Plot</h3>
        <svg class="plot-svg" viewBox="0 0 {PLOT_WIDTH} {PLOT_HEIGHT}" role="img" aria-label="Scatter plot of TPSA and XLogP values">
            <line class="plot-axis" x1="{PLOT_LEFT}" y1="{x_axis_y}" x2="{PLOT_WIDTH - PLOT_RIGHT}" y2="{x_axis_y}"></line>
            <line class="plot-axis" x1="{PLOT_LEFT}" y1="{PLOT_TOP}" x2="{PLOT_LEFT}" y2="{x_axis_y}"></line>

            <text class="plot-tick" x="{PLOT_LEFT}" y="{x_axis_y + 22}">{min_tpsa:.1f}</text>
            <text class="plot-tick" x="{PLOT_WIDTH - PLOT_RIGHT}" y="{x_axis_y + 22}" text-anchor="end">{max_tpsa:.1f}</text>
            <text class="plot-tick" x="{PLOT_LEFT - 12}" y="{x_axis_y}" text-anchor="end">{min_xlogp:.1f}</text>
            <text class="plot-tick" x="{PLOT_LEFT - 12}" y="{PLOT_TOP + 4}" text-anchor="end">{max_xlogp:.1f}</text>

            {points}

            <text class="plot-axis-label" x="{PLOT_LEFT + plot_width / 2:.1f}" y="{PLOT_HEIGHT - 22}" text-anchor="middle">TPSA (topological polar surface area)</text>
            <text class="plot-axis-label" transform="translate(24 {PLOT_TOP + plot_height / 2:.1f}) rotate(-90)" text-anchor="middle">XLogP (octanol-water partition coefficient)</text>
        </svg>
    </div>
    """
