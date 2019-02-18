import os, sys
import json
import requests

import threading
import queue
import time

count = 0
goodURL = json.load(open("urlsClean.json"))
exitFlag = 0


if len(sys.argv) < 2:
    print("Invalid arguments. Usage: momentosGet.py {memgator_url}")
    sys.exit(1)
else:
    try:
        print('carbondate url: %s' % sys.argv[1])
        res = requests.head("%s" % sys.argv[1])
    except Exception as e:
        print("carbon url is not valid: ", str(e))
        sys.exit(1)

carbondate_url = sys.argv[1]

# create backup of URL database file
backup = json.load(open("urlsClean.json"))
with open('urlsClean.bak', 'w') as json_file:
    json.dump(backup, json_file)
    json_file.close()


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        processURL(self.name)


def processURL(thread_name):
    while not exitFlag:
        global count
        global workQueue
        global goodURL
        count += 1
        queueLock.acquire()

        if not workQueue.empty():
            url = workQueue.get()
            queueLock.release()
            try:
                res = requests.get("%s/cd/%s" % (carbondate_url, url))
                responseJSON = json.loads(res.text)
                creationDate = responseJSON["estimated-creation-date"]
                goodURL[url]["carbonDate"] = creationDate
            except Exception as e:
                print("Error: ", str(e))

            if count % 25 == 0:
                print("%d links passed to carbondate. Executed by thread: %s" % (count, thread_name))


threadList = []
for i in range(0, 6):
    threadList.append("Thread-%d" % i)


queueLock = threading.Lock()
workQueue = queue.Queue(maxsize=0)
threads = []
threadID = 1

#create new threads
for threadName in threadList:
    thread = myThread(threadID, threadName)
    thread.start()
    threads.append(thread)
    threadID += 1

# fill queue
queueLock.release()
queueLock.acquire()
q_urls = goodURL.keys()
for link in q_urls:
    workQueue.put(link)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = -1

# wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")

with open('urlsClean.json', 'w')as outFile:
    pretty_data = json.dumps(goodURL, indent=4)
    outFile.write(pretty_data)
