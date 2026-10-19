import time as t
import datetime as dt

seconds = t.time()
print("Seconds since January 1, 1970: ", f"{seconds:,.4f}", " or ", f"{seconds:.2e}"," in scientific notation")
now = dt.datetime.now()
formatted_now = now.strftime("%b %d %Y")
print(formatted_now)