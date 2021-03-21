Python Flask Web Framework to integrate with Broker. Currently supports TD Broker.
Run index.py to start Flask server.  The OAuth token is retreived from Redis but can be changed to pick up from any persistent store including File.

Features
1) Search for option income - Covered Calls and Secured Puts
2) Retrieves all your transaction based on Filter criteria - Date, Trade Type, Ticker, etc.
3) Shows the price for a ticker and other charting capabilities

<img width="1419" alt="Screen Shot 2021-03-21 at 11 36 38 AM" src="https://user-images.githubusercontent.com/5234229/111916848-29dcbb00-8a3a-11eb-80b2-281ad1377e29.png">

<img width="1390" alt="Screen Shot 2021-03-21 at 11 36 53 AM" src="https://user-images.githubusercontent.com/5234229/111916974-c30bd180-8a3a-11eb-9c8b-970823811d87.png">

<img width="1405" alt="Screen Shot 2021-03-21 at 11 37 31 AM" src="https://user-images.githubusercontent.com/5234229/111917001-e8004480-8a3a-11eb-806e-a983af1d9cfc.png">

<img width="1378" alt="Screen Shot 2021-03-21 at 11 38 22 AM" src="https://user-images.githubusercontent.com/5234229/111917008-f0f11600-8a3a-11eb-8a6c-7dda447270da.png">



# Run the below code to get token if needed

from broker.base import Base

base = Base()
base.login()



# redis Start
redis-server /usr/local/etc/redis.conf

