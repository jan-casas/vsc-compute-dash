# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "0rem",
    "left": 0,
    "bottom": 0,
    "width": "calc(100% - 65rem)",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "background-color": "white",
    "margin-left": "6rem",
    "margin-top": "3.5rem",
}

SIDEBAR_HIDDEN = {
    "position": "fixed",
    "top": "0rem",
    "left": "calc(65rem - 100%)",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "background-color": "white",
    "margin-top": "3.5rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "16rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "white",
    "width": "calc(100% - 16rem)",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "white",  # "#f8f9fa",
    # total width - 16rem
    "width": "98%", }
