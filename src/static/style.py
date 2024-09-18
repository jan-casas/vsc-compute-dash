# the style arguments for the sidebar. We use position:fixed and a fixed width
WIDTH_COLLAPSED = "60rem"
sidebar_style_dict = {
    "position": "fixed",
    "top": "0rem",
    "left": 0,
    "bottom": 0,
    "width": f"calc(100% - {WIDTH_COLLAPSED})",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "background-color": "white",
    "margin-left": "6rem",
    "margin-top": "3.5rem",
}

sidebar_hidden_dict = {
    "position": "fixed",
    "top": "0rem",
    "left": f"calc({WIDTH_COLLAPSED} - 100%)",
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
content_style_dict = {
    "transition": "margin-left .5s",
    "margin-left": "16rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "white",
    "width": "calc(100% - 16rem)",
}

content_style1_dict = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "white",  # "#f8f9fa",
    # total width - 16rem
    "width": "98%", }
