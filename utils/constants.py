# Creating an empty dictionary
screener_list = {}

# Adding list as value
screener_list["option_stocks"] = ["LYFT", "TSLA", "CAT", "COST"]
screener_list["finance"] = ["WF", "BAC", "JPM","C","GS","V","AXP","COF"]
screener_list["tech"] = ["ORCL", "IBM", "FB", "AAPL", "NFLX", "MSFT"]


style_cell = {
    "padding": "12px",
    "width": "auto",
    "textAlign": "center",
    "fontFamily": "Lato",
}
style_header = {
    "backgroundColor": "#2C3E50",
    "color": "white",
    "textAlign": "center",
}
style_data_conditional = [
    {
        # stripped rows
        "if": {"row_index": "odd"},
        "backgroundColor": "rgb(248, 248, 248)",
    },
]
