import requests
import threading
import queue
import time

count = 0
notTwitter = []
goodURLS = set()
error = open('duplicateCheckErrors.txt','w')
exitFlag = 0


class myThread (threading.Thread):
    def __init__(self, threadID, name, q, count):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        processURL(self.name, self.q, count)


def processURL(thread_name, q, count):
    while not exitFlag:
        count += 1
        queueLock.acquire()

        # follow the url until the location header isn't present, then check if its a twitter domain.
        # push onto threadsafe list, which will be fed into a set down the line to check for duplicates.
        if not workQueue.empty():
            url = q.get()
            queueLock.release()
            push = False
            try:
                res = requests.get(url)
                url = res.url

                while res.status_code == 301:
                    try:
                        url = res.headers['location']
                        res = requests.get(url)
                    except Exception as e:
                        print("Error: ", str(e))

                if url.find('twitter') < 0 and res.status_code == 200:
                    push = True
                else:
                    push = False
            except Exception as e:
                print("some error " + str(e) + ": " + url)

            if push == True:
                notTwitter.append(url)
        else:
            queueLock.release()
            time.sleep(1)

        if len(notTwitter) % 5 == 0 and len(notTwitter) != 0:
            print("%d candidate links" % len(notTwitter))


threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8", "Thread-9", "Thread-10"]
queueLock = threading.Lock()
workQueue = queue.Queue(maxsize=0)
threads = []
threadID = 1

#create new threads
for threadName in threadList:
    thread = myThread(threadID, threadName, workQueue, count)
    thread.start()
    threads.append(thread)
    threadID += 1

# fill queue
queueLock.acquire()
with open('unparsedURLs.txt', 'r') as inFile:
    for line in inFile:
        testURL = line.strip()
        workQueue.put(testURL)
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



for item in notTwitter:
    goodURLS.add(item + '\n')
with open("parsedURLs.txt", 'a') as outFile:
    for entry in goodURLS:
        outFile.write(entry)
