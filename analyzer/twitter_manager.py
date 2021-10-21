import queue
import threading

from .twitter_sentiment import TweetMiner

should_publish = threading.Event()
update_queue = queue.Queue()


def start_publisher():
    global handle_list

    starttime = TweetMiner.time.time()
    print("Start polling", starttime)
    poll_iteration = 1

    for i in range(10):
        for name in handle_list:
            print(i, poll_iteration, "\rpublishing update ", end="")
            update_queue.put((poll_iteration, name))
            poll_iteration += 1
            time.sleep(900)
            print("\rawaiting for publishing update", end="")
            should_publish.wait()
            update_queue.join()


def start_update_listener():
    while True:
        poll_iteration, name = update_queue.get()

        print(" --- ", name)
        try:

            miner.mine_crypto_currency_tweets(query=name)
            update_queue.task_done()

        except Exception as e:  # work on python 3.x
            print("Failed to upload to ftp: " + str(e))


listener_thread = threading.Thread(target=start_update_listener, daemon=True)
publisher_thread = threading.Thread(target=start_publisher, daemon=True)
