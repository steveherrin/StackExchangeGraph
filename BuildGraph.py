import requests
import igraph

if __name__ == '__main__':

    # Some constants that determine what data to fetch
    start_date = 1383264000 # November 1, 2013
    end_date = 1383350400   # November 2, 2013
    site = 'stackoverflow'
    tag_list = ['python']

    graph = BuildGraph(graph, start_date, end_date, site, tags)

def BuildGraph(start_date, end_date,
               site='stackoverflow', tags = [],
               base_url='http://api.stackexhange.com',
               start_page = 1,
               graph = None)
    """ Builds a graph from data from StackExchange with the specified
        site and tags, between the start and end date. The graphs's
        vertices are users and edges are if a user has answered another
        user's question. It is therefore directed.
        Can also add to an existing graph. This and the start_page argument
        are useful if quota limits prevented grabbing all the data """

    if not graph:
        # Create a new graph
        graph = igraph.Graph(directed = True)

    # Keep track of how we've grab from StackExchange
    # and if we've grabbed everything
    quota_remaining = 10000
    has_more = True
    page = start_page

    while quota_remaining > 0 and has_more:
        # Just keep grabbing questions and looking at their answers
        req = GetQuestionRequestString(page, start_date, end_date
                                       tags, site)
        url = base_url + req
        r = requests.get(url)
        data = r.json()
        questions = data.get('items', []) # empty list if no questions returned
        for question in questions:
            AddQuestionToGraph(question, graph)

        # update for next iteration
        if quota_remaining > 0:
            page += 1
        has_more = data['has_more']
        quota_remaining = data['quota_remaining']

    print "Processed %i pages."%(page)
    print "Graph summary:"
    igraph.summary(graph)

def GetQuestionRequestString(page, fromdate, todate, tags, site):
    """ Returns the StackExchange API request string for questions
        with the specified arguments """
    req = "/2.1/questions?page=%i&fromdate=%i&todate=%i"%(page,
                                                          fromdate,
                                                          todate)
    req += "order=desc&sort=activity&tagged=%s&site=%s"%(';'.join(tags),
                                                         site)
    return req
