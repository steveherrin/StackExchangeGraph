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
               site='stackoverflow', tags = [])
    """ Builds a graph from data from StackExchange with the specified
        site and tags, between the start and end date. The graphs's
        vertices are users and edges are if a user has answered another
        user's question. It is therefore directed. """

    # Create a new graph
    graph = igraph.Graph(directed = True)

def GetQuestionRequestString(page, fromdate, todate, tags, site):
    """ Returns the StackExchange API request string for questions
        with the specified arguments """
    req = "/2.1/questions?page=%i&fromdate=%i&todate=%i"%(page,
                                                          fromdate,
                                                          todate)
    req += "order=desc&sort=activity&tagged=%s&site=%s"%(';'.join(tags),
                                                         site)
    return req
