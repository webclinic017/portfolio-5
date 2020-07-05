# Creating an empty dictionary
screener_list = {}

# Adding list as value
screener_list["option_stocks"] = ["LYFT", "TSLA", "CAT", "COST"]
screener_list["finance"] = ["WF", "BAC", "JPM","C","GS","V","AXP","COF"]
screener_list["tech"] = ["ORCL", "IBM", "FB", "AAPL", "NFLX", "MSFT","QQQ","TWTR"]
screener_list["ETF"] = ["XLE","VTE","XLB","XLI","XLY","XLP","XLF","XLV","XLU"]
screener_list["JEPI"] = ["AMZN","MSFT","ACN","ABBV","GOOGL","LLY","AAPL","HON","PEP","JKHY","MA","XEL","PG","INTU","MDLZ","NEE","BMY","CMS","CHTR","JNJ","MRK","SLGN","PGR","KMB","COST","NOC","ICE","TGT","ALL","VZ","PFE","BRK.B","EQIX","ETR","CB","CME","AZO","BAX","HD","PCAR","WM","SRE","TMUS","TMO","AON","ODFL","NFLX","ADP","TT","FB","KO","DUK","AEP","LDOS","TXN","CMCSA","PM","DLTR","CRM","V","WMT","TJX","LIN","MO","REGN","ETN","HSY","PYPL","NSC","MCD","CMI","NKE","UNH","GIS","CAG","ALXN","STZ","GD","APD","SUI","RTX","PLD","KR","SPGI","KMI","EVRG","AXP","BLK","MDT","MCK","MMC","CVX","NEM","ELS","DE","ROST"]


style_cell = {
    "padding": "12px",
    "width": "auto",
    "textAlign": "center",
    "fontFamily": "\"Segoe UI\", \"Source Sans Pro\", Calibri, Candara, Arial, sans-serif",
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
