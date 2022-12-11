import pandas as pd
url='wss://fstream.binance.com/ws/!forceOrder@arr'
import asyncio
from websockets import connect
import json
import requests

token='5801845290:AAFQKKjdqY5bzbHWcjhOCoRRzqgN9zWucQU'
id='binance_liq_data_sid'
def send_message_on_telegram(message):
    url=f'https://api.telegram.org/bot{token}/sendMessage?chat_id=@{id}&text={message}'
    tel_resp= requests.get(url)
    
    
    if tel_resp.status_code==200:
        print('Notification has been sent')
        
    else:
        print('you made an error')
        
async def bin_liq(url):
    async for websocket in connect(url):
        try:
            while True:
                msg=await websocket.recv()
                print(msg)
                msg=json.loads(msg)['o']
                ap_1=float(msg["ap"])
                ap=round(ap_1,3)
                q_1=float(msg["q"])
                q=round(q_1,3)
                if msg['S'] == 'SELL' :
                    ab = f'🔴{msg["s"]} Long Liquidation : ${ap * q} at ${ap}'
                    send_message_on_telegram(ab)
                if msg['S'] == 'BUY'  :
                    ab = f'🟢{msg["s"]} Short Liquidation : ${ap * q} at ${ap}'
                    
                    send_message_on_telegram(ab)
                
        except Exception as e:
            print(e)
            continue     
        
asyncio.run(bin_liq(url))
