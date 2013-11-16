import requests
#import igraph
import time
import StackAppsConstants


def BuildGraph(start_date, end_date,
               site_info = None, tags = [],
               start_page = 1,
               graph = None):
    """ Builds a graph from data from StackExchange with the specified
        site and tags, between the start and end date. The graphs's
        vertices are users and edges are if a user has answered another
        user's question. It is therefore directed.
        Can also add to an existing graph. This and the start_page argument
        are useful if quota limits prevented grabbing all the data """

    if not graph:
        # Create a new graph
        #graph = igraph.Graph(directed = True)
        pass

    if not site_info:
        site_info = {'site': 'stackoverflow',
                     'base_url': 'http://api.stackexchange.com',
                     'sleep_time': 0.035} # s, since limited to 30 requests/s}

    # Keep track of how we've grab from StackExchange
    # and if we've grabbed everything
    quota_remaining = 10000
    has_more = True
    page = start_page

    while quota_remaining > 0 and has_more:
        # Grab a bunch of questions
        url = GetQuestionRequestString(page, start_date, end_date,
                                       tags, site_info)
        print url
        r = requests.get(url)

        data = r.json()

        # handle throttling
        # the API can tell us to back off, otherwise use a default time
        sleep_time = float(data.get('backoff', site_info['sleep_time']))
        time.sleep(site_info['sleep_time']) # for throttling

        print len(data.get('items', [])), "questions retrievd."
        print data.get('backoff', "No backoff")
        print data.get('has_more', "No more.")
        print data.get('quota_remaining', "No quota left.")

        # process the questions and add to graph
        questions = data.get('items', []) # empty list if no questions returned
        for question in questions:
            AddQuestionToGraph(question, graph)

        # update for next iteration
        if quota_remaining > 0:
            page += 1
        has_more = data['has_more']
        quota_remaining = data['quota_remaining']

        dummy = raw_input('next...')

    print "Processed %i pages."%(page)
    print "Graph summary:"
    igraph.summary(graph)

def GetQuestionRequestString(page, fromdate, todate, tags, site_info):
    """ Returns the StackExchange API request URL for questions
        with the specified arguments """

    url = site_info['base_url']
    url += "/2.1/questions?page=%i&fromdate=%i&todate=%i"%(page,
                                                          fromdate,
                                                          todate)
    url += "&order=desc&sort=activity&tagged=%s&site=%s"%(';'.join(tags),
                                                         site_info['site'])
    if 'key' in site_info:
        url += "&key=%s"%(site_info['key'])
    return url

if __name__ == '__main__':

    # Some constants that determine what data to fetch
    start_date = 1383264000 # November 1, 2013
    end_date =   start_date + 24*60*60
    tag_list = ['python']
    site_info = {'site': 'stackoverflow',
                 'base_url': 'http://api.stackexchange.com',
                 'sleep_time': 0.035, # s, since limited to 30 requests/s}
                 'key': StackAppsConstants.key }



    graph = BuildGraph(start_date, end_date, site_info, tag_list)
