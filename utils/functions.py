from datetime import datetime as dt

# Define Formatters
def formatter_currency(x):
	return "${:,.0f}".format(x) if x >= 0 else "(${:,.0f})".format(abs(x))

def formatter_currency_with_cents(x):
	return "${:,.2f}".format(x) if x >= 0 else "(${:,.2f})".format(abs(x))

def formatter_percent(x):
	return "{:,.1f}%".format(x) if x >= 0 else "({:,.1f}%)".format(abs(x))

def formatter_percent_2_digits(x):
	return "{:,.2f}%".format(x) if x >= 0 else "({:,.2f}%)".format(abs(x))

def formatter_number(x):
	return "{:,.0f}".format(x) if x >= 0 else "({:,.0f})".format(abs(x))

def date_from_milliseconds(x):
	return dt.fromtimestamp(x/1000.0).strftime("%Y-%m-%d")