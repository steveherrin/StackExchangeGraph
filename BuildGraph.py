import requests
#import igraph
import time
import StackAppsConstants
import cPickle as pickle

def BuildGraph(start_date, end_date,
               site_info = None, tags = [],
               start_page = 1,
               graph = None):
    """ Builds a graph from data from StackExchange with the specified
        site and tags, between the start and end date. The graphs's
        vertices are tags and edges are placed when two tags appear on
        the same question.
        Can also add to an existing graph. This and the start_page argument
        are useful if quota limits prevented grabbing all the data """

    if not graph:
        # Create a new graph
        #graph = igraph.Graph(directed = False)
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
        r = requests.get(url)
        data = r.json()

        # handle throttling
        # the API can tell us to back off, otherwise use a default time
        sleep_time = float(data.get('backoff', site_info['sleep_time']))
        time.sleep(site_info['sleep_time']) # for throttling

        # process the questions and add to graph
        questions = data.get('items', []) # empty list if no questions returned
        for question in questions:
            AddQuestionToGraph(question, graph)

        # update for next iteration
        if quota_remaining > 0:
            page += 1
        has_more = data['has_more']
        quota_remaining = data['quota_remaining']

    print "Processed %i pages."%(page)
    if quota_remaining == 0:
        print "   ... but ran out of quota."
    print "Graph summary:"
    igraph.summary(graph)


def GetQuestionRequestString(page, fromdate, todate, tags, site_info):
    """ Returns the StackExchange API request URL for questions
        with the specified arguments """

    url = site_info['base_url']
    url += "/2.1/questions?page=%i&fromdate=%i&todate=%i"%(page,
                                                          fromdate,
                                                          todate)
    url += "&order=desc&sort=activity&site=%s"%(site_info['site'])
    if tags:
        url += "&tagged=%s"%(';'.join(tags))
    if 'key' in site_info:
        url += "&key=%s"%(site_info['key'])
    return url


def GetVertexList(tags, graph):
    """ Returns a list of vertices in graph that correspond to a tag.
        If a vertex for a tag doesn't exist, one will be created """
    vertices = []

    # first lookup all the vertices in the graph
    # or create them if they don't exist yet
    for tag in tag:
        tag = tag.lower()
        try:
            vertex = graph.find(name=tag)
        except ValueError:
            graph.add_vertex(name=tag, count=0)
            vertex = graph.find(name=tag)
        # Keep track of how many times we see a tag
        # so we can later filter out rare tags if needed
        vertex['count'] += 1
        vertices.append(vertex)

    return vertices


def AddEdgesBetweenVertices(vertices, graph):
    """ Adds edges between all vertex pairs that can be made from vertices.
        If an edge already exists, its weight is increased by 1 """

    for i in xrange(len(vertices)):
        for j in xrange(i+1, len(vertices)):
            v1 = vertices[i].index
            v2 = vertices[j].index
            try:
                e = graph.get_eid(v1, v2)
            except ValueError:
                graph.add_edge(v1, v2, weight=0)
                e = graph.get_eid(v1, v2)
            e['weight'] += 1


def AddQuestionToGraph(question, graph):
    """ For the question, extract the tags. Treat each tag as a vertex
        and create edges (or increase their weight) between the tags in
        this particular question. """
    tags = question['tags']
    vertices = GetVertexList(tags, graph)
    AddEdgesBetweenVertices(vertices, graph)


if __name__ == '__main__':
    # Some constants that determine what data to fetch
    start_date = 1383264000 # November 1, 2013
    end_date =   start_date + 1*60
    tag_list = []
    site_info = {'site': 'stackoverflow',
                 'base_url': 'http://api.stackexchange.com',
                 'sleep_time': 0.035, # s, since limited to 30 requests/s}
                 'key': StackAppsConstants.key }

    graph = BuildGraph(start_date, end_date, site_info, tag_list)

    with out_file as open('graph.pkl'):
        pickle.dump(graph, out_file)
