from threading import Thread, Event
import time

stop_event = Event()


def timer():
    i = 0
    while True:
        i += 1
        print(f"-- Retrying again... In: {i}")
        time.sleep(1)
        if stop_event.is_set():
            break


def TimerThread(threadName, targetFunction, time):
    threadName = Thread(target=targetFunction)
    threadName.start()
    threadName.join(timeout=time)
    stop_event.set()
    print("-- Restarted --")
