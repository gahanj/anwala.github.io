import urllib.request
from queue import Queue


def scrapePdfContentLength(queue,results):
    url = queue.get()
    try:
        with urllib.request.urlopen(url) as res:
            # check if the url is a pdf
            if (res.info()['Content-Type'] != 'application/pdf'):
                pass
            else:
                if (res.info()['Content-Length'] != 'None'):
                    contentLength = res.info()['Content-Length']
                    results.append("URL: {}  Content-Length: {}".format(res.geturl(), contentLength))
                else:
                    contentLength = 'CL Header Missing'
    except urllib.error.HTTPError as e:
        print('Exception thrown on URL: {}  Error: {}'.format(url,e.reason))
    except urllib.error.URLError as e:
        print('Exception thrown on URL: {}  Error: {}'.format(url,e.reason))
    except:
        print('Something else went wrong')
    queue.task_done()