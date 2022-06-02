from matplotlib import colors as mcolors


def show_only_this_labels(fig, labels=None, pred=None):
    assert labels is not None or pred is not None
    
    if pred is None:
        pred = lambda name: name in labels
    
    for trace in fig["data"]:
        trace["showlegend"] = pred(trace["name"])
            

def add_label(fig, name, color, linewidth=1.5, dash=None, mode="lines"):
    def add_sc(color):
        fig.add_scatter(
            x=[None],
            y=[None],
            hoverinfo="none",
            name=name,
            line=dict(color=color, width=linewidth),
            mode=mode,
        )
    
    try:
        add_sc(color)
    except ValueError as _:
        color = mcolors.to_hex(color)
        add_sc(color)
   
    fig.update_layout(showlegend=True)
