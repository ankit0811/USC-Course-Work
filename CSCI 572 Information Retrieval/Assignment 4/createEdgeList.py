import networkx as nx;
G = nx.read_edgelist("edgeList.txt", create_using=nx.DiGraph())
pr = nx.pagerank(G, alpha=0.85, personalization=None, max_iter=30, tol=1e-06, nstart=None, weight='weight',dangling=None)

with open('external_pageRankFile','w') as f:
    for key in pr:
        f.write("/home/ankit/solr-6.5.0/NYTimesData/NYTimesDownloadData/"+key+"="+str(pr[key])+"\n");
    f.close()

