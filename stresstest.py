import asyncio
import websockets
import time
from threading import Thread, Event

URL = "wss://kusama-rpc.dwellir.com"
#URL = "wss://kusama.api.onfinality.io/public-ws"

event = Event()

def work(t_id, event):
  async def start_work():
    async with websockets.connect(URL, timeout=30) as websocket:
      await websocket.send("{\"id\":1, \"jsonrpc\":\"2.0\", \"method\": \"chain_subscribeFinalizedHeads\"}")
      while(not event.is_set()):
        start = time.time()
        await websocket.recv()
        stop = time.time()
        print(f"Thread {t_id}: {round(stop - start, 1)}", flush=True)
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(start_work())

def main():
    n_threads = 3
    threads = []
    for i in range(n_threads):
      t = Thread(target=work, args=(i, event))
      threads.append(threads)
      t.start()

    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt as e:
      print("Exitiing...")

    event.set()
    for t in threads:
      try:
        t.join()
      except AttributeError:
        pass

if __name__ == "__main__":
  main()
