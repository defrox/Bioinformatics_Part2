__author__ = 'ilap'

## Imports
import threading

import sys
sys.setrecursionlimit(1000000000)
import time

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

'''
########################################################################################
####### 1.5 Suffix Trees
########################################################################################
'''

def suffixTreeMatching (suffix_trie, text, node = 0,result ="", pattern_len=0):

    max_len = pattern_len
    nodes = suffix_trie[node].keys ()

    #print "NODES to walk", nodes
    for tmp_node in nodes:
        ((str_pos, str_len), idx) = suffix_trie[node][tmp_node]
        new_result = text[str_pos:str_pos+str_len]
        #print "NODE", tmp_node, node, result

        nr_keys = suffix_trie[tmp_node].keys ()
        key_len = len (nr_keys)
        if  nr_keys != []:
            #print "AAA", node, tmp_node, " AAA", key_len, result, " NEW R:", new_result
            new_result = result + new_result
            if (max_len < len (new_result)):
                max_len = len (new_result)
            suffixTreeMatching(suffix_trie, text, tmp_node, new_result, pattern_len)
        #else:
        #    result = ""

    if result != "":
        print len (result), result
    return result

def sufixTreeConstructionProblem (suffix_tree, text):
    result = []
    for line in suffix_tree:
        if  line != {}:
            #print line
            for key in line.keys ():
                (pos, str_len) = line[key]
                #print STR[pos:pos+len]
                result.append(text[pos:pos+str_len])


    print '\n'.join(result)

'''
CS: Constructing a Suffix Tree
'''

def modifiedSuffixTrieConstruction (text):

    trie = [{}] # Root, with no edges and nodes
    for i in range (len (text)):
        current_node =  0

        #new_text = text[i:]
        #for j,current_symbol in enumerate (new_text):
        for j in range (i, len (text)):
            current_symbol = text[j]

            #print "PRINT", i,j, current_symbol

            nodes = trie[current_node]

            if nodes.has_key(current_symbol):
                (current_node, dummy) = nodes[current_symbol]
                #print "ALMA", current_node, nodes[current_symbol]
            else:
                new_node = len (trie)
                #print "NEW_NODE", new_node
                trie.append({})
                trie[current_node][current_symbol] = (new_node,(j,i))

                #if current_symbol == "$":
                #    print "PRINT NODE", str(current_node) + "->" + str (nodes[current_symbol]) +":" + str (i) + ": SYM:" + current_symbol
                current_node = new_node


    return trie

global GIDX
global TRIE

def recursiveBuild (idx, nbg, old_trie, new_idx = 0, suffix_graph = None):

    global GIDX
    global TRIE
    #print "NBG", idx, len(nbg), nbg
    #print "0000000", idx, new_idx
    for arr in nbg[idx]:
        #print "AAAAAAAAAA", arr[-1], idx, arr
        GIDX += 1
        ##

        key = idx
        f_s = key
        f_e = arr[0]

        if len (arr) == 1:
            l_s = key
            l_e = arr[0]
        else:
            l_s = arr[-2]
            l_e = arr[-1]

        f_p = old_trie[f_s].values(); f_p.sort()
        l_p = old_trie[l_s].values(); l_p.sort ()

        #print "f_p, f_e", f_e, f_p
        #print "l_p, l_e", l_e, f_p

        f_pp = dict (f_p)[f_e]
        l_pp = dict(l_p)[l_e]
        #print "FIRST, LAST", key, f_pp, l_pp, old_trie[l_pp]

        str_len = len (arr)
        tt = old_trie[idx].values ()
        tt.sort ()
        dd = dict (tt)
        aa= dd[f_e]
        (str_position, str_idx) = aa

        TRIE.append({})
        TRIE[new_idx][GIDX] = ((str_position,str_len), (str_idx, 'g'))
        #print "FINAL:", len (TRIE), " NEW IDX", new_idx, idx, "(", GIDX-1, ",", GIDX, ") :", str_position, str_len

        (pidx, dummy) = l_pp
        #print "LPP", pidx, l_pp
        if old_trie[pidx+1] != {} :
            recursiveBuild(arr[-1], nbg, old_trie, GIDX)

    return TRIE


def rebuildSuffixTrie (old_trie):

    suffix_graph = suffixTrie2Graph(old_trie)
    nonb_ranch_graph = maximalNonBranchingPathsInTrie(suffix_graph)

    #TODO: enable if necessary for i in nonb_ranch_graph:
    #    print i, nonb_ranch_graph[i]

    global GIDX
    GIDX = 0
    global TRIE
    TRIE = [{}]

    trie = recursiveBuild(0, nonb_ranch_graph, old_trie, 0, suffix_graph)

    return trie

def maximalNonBranchingPathsInTrie(graph, start_node=-1, end_node=-1):

    paths = []
    dict = {}
    np = []

    in_keys = graph.keys ()
    in_keys.sort ()

    #print "GRAPH", graph
    #print "LEN OF KEEYS", len (graph.keys ())
    for node in graph.keys ():
        if len (graph[node]) > 1:

            nbp = []
            for n in graph[node]:
                nbp = [node]
                nbp.append(n)
                w = n

                while graph.has_key (w) and (len (graph[w]) == 1):
                    u = graph[w][0]
                    nbp.append(u)
                    w = u
                paths.append(nbp)
                np.append(nbp[1:])
            dict[node] = np[:]
            np = []
            continue


    #print "PATSH", paths
    #for i in paths:
    #    print ' -> '.join (str (x) for x in i)
    return  dict

def compressedSuffixTrie2Graph (trie):

    print "TRIE", trie
    graph = {}
    idx = 0
    for node in trie:
        vals = node.keys()
        #print "VALS NOTS", vals
        vals.sort()
        #print "VALS SORT", node, vals
        if vals != []:
            graph[idx] = vals
            ##### print graph[idx]
        idx += 1

    return graph

def suffixTrie2Graph (trie):
    graph = {}
    idx = 0
    for node in trie:
        vals = [int (k) for k,v in node.values()]
        #print "VALS NOTS", vals
        vals.sort()
        #print "VALS SORT", node, vals
        if vals != []:
            graph[idx] = vals
            ##### print graph[idx]
        idx += 1

    return graph

def trie2Graph (trie):
    graph = {}
    idx = 0
    for node in trie:
        vals = node.values()
        vals.sort()
        if vals != []:
            graph[idx] = vals
            ##### print graph[idx]
        idx += 1

    return graph

'''
nonBranching...
'''
def deletePath (graph, from_node, to_node=-1):
    lock = threading.Lock()

    lock.acquire() # will block if lock is already held
    if from_node in graph:
        nodes = graph[from_node]
        if len (nodes) > 1:
            if to_node == -1:
                idx = 0
            else:
                #print "NOEDS", nodes
                idx = nodes.index (to_node)
            del graph[from_node][idx]
        else:
            del graph[from_node]
    lock.release()
    return graph
# @timing
def outPath (graph, node):

    result = -1
    if graph.has_key(node):
        result =  len (graph[node])
    #print "OUTP", result
    return result

#@timing
def inPath (graph, node, arr):

    i = arr.count (node)
    #print "INP", i
    return i

    i = 0
    for graph_keys in graph.keys ():
        values = graph[graph_keys]
        #print values
        i += values.count (node)
        if i > 1:
            break
    print "INP", i
    return i

def oneInOneOut (graph, node, arr):

    o1 = outPath(graph, node)
    if o1 > 1:
        return False
    i1 = inPath(graph, node, arr)
    #print "INOUT-----", node,  i1, o1, (i1 == o1) and (i1 == 1)
    return ( (i1 == o1) and (i1 == 1))

def maximalNonBranchingPaths(graph, start_node=-1, end_node=-1):

    paths = []
    dict = {}
    np = []

    if start_node != -1 and end_node != -1:
        deletePath(graph, start_node, end_node)

    import copy
    new_graph = copy.deepcopy (graph)

    NA = []
    for n in graph.keys ():
        NA.append (n)
    NA.sort ()
    #print NA
    #exit ()

    print "LEN OF KEEYS", len (graph.keys ())
    for node in graph.keys ():
        if not oneInOneOut(graph, node, NA):

            nbp = []

            if outPath(graph, node) > 0:
                for n in graph[node]:
                    nbp = [node]
                    nbp.append(n)
                    #TODO deletePath(new_graph, node, n)
                    w = n
                    #print "ONE IN ONE OUT"
                    while oneInOneOut(graph, w, NA):
                        #print "IN ONE IN ONE OUT"

                        u = graph[w][0]
                        nbp.append(u)
                        #TODO deletePath(new_graph, w, u)
                        w = u
                    #print "NBP2", nbp, len (new_graph.keys ())

                    paths.append(nbp)
                    np.append(nbp[1:])

                dict[node] = np[:]
                np = []
            #print "DICT", len (new_graph.keys ())

    print "PATSH", paths
    for i in paths:
        print ' -> '.join (str (x) for x in i)
    return  dict
    if not len (new_graph):

        return dict
        #TODO return paths


    nodes = new_graph.keys ()

    indegreezero = []
    for node in nodes:
        if inPath(new_graph, node):
            indegreezero.append (node)
        else:
            print "######### WARNINGGGGGG ###########", node

    #print "SSSSSSSSSSSSSSS", indegreezero
    #print "NEWGRAPH", new_graph

    for start_node in indegreezero:
        snode = start_node
        nbp_cycle = []

        while True:
            nbp_cycle.append(snode)
            if not new_graph.has_key(snode):
                break

            onode = snode
            snode = new_graph[snode][0]

            #print "NW", snode, onode, new_cycle
            deletePath(new_graph, onode)
            if start_node == snode:
                nbp_cycle.append(snode)
                #paths.append(nbp_cycle)
                #print "BREAKED", nbp_cycle
                if dict.has_key(start_node):
                    arr = dict[start_node]
                    arr.append (nbp_cycle)
                else:
                    arr = nbp_cycle[:]

                dict[start_node] = arr[:]

                nbp_cycle = []
                break


        if not new_graph:
            break

    return dict

'''
########################################################################################
####### 1.3 Herding Patterns To Tries
########################################################################################
'''
'''
TRIECONSTRUCTION(Patterns)
        Trie <- a graph consisting of a single node root
        for each string Pattern in Patterns
            currentNode <- root
            for i <- 1 to |Pattern|
                if there is an outgoing edge from currentNode with label currentSymbol
                    currentNode <- ending node of this edge
                else
                    add a new node newNode to Trie
                    add a new edge from currentNode to newNode with label currentSymbol
                    currentNode <- newNode
        return Trie
'''
'''
Trie Construction Problem: Construct a trie on a set of patterns.
     Input: A collection of strings Patterns.
     Output: Trie(Patterns).
     Note: Checked/Tested...
'''
def trieConstruction (*patterns):

    # Sort them first
    #TODO sort does not need
    ##  patterns = sorted (patterns)

    trie = [{}] # Root, with no edges and nodes
    for word in patterns:
        current_node =  0

        for idx, current_symbol in enumerate (word):

            nodes = trie[current_node]
            if nodes.has_key(current_symbol):
                current_node = nodes[current_symbol]
            else:
                new_node = len (trie)
                trie.append({})
                trie[current_node][current_symbol] = new_node
                print str(current_node) + "->" + str (nodes[current_symbol]) +":" + current_symbol
                current_node = new_node

    return trie

'''
PREFIXTRIEMATCHING(Text, Trie)
        symbol <- first letter of Text
        v <- root of Trie
        while forever
            if v is a leaf in Trie
                return the pattern spelled by the path from the root to v
            else if there is an edge (v, w) in Trie labeled by symbol
                symbol <- next letter of Text
                v <- w
            else
                output "no matches found"
                return
'''
def prefixMatching (text, trie):

    str_idx = 0
    current_symbol = text[str_idx]
    current_node = 0;
    result = ""

    while True:

        #next_nodes = {v: k for k, v in trie[current_node].items()}

        if trie[current_node] == {}:
            return result
        else:

            if trie[current_node].has_key (current_symbol):

                result += current_symbol

                current_node = trie[current_node][current_symbol]

                str_idx += 1
                try:
                    current_symbol = text[str_idx]
                except:
                    #print "Exception"
                    True
            else:
                #print "No Matches Found!"
                return
'''
TRIEMATCHING(Text, Trie)
        while Text is nonempty
            PREFIXTRIEMATCHING(Text, Trie)
            remove first symbol from Text
'''
def treeMatching (text, *patterns):



    trie = trieConstruction(*patterns)
    result = []
    str_idx = 0
    while str_idx < len (text):

        match = prefixMatching(text[str_idx:], trie)
        if match != None:
            result.append (str_idx)
        str_idx += 1

    return result

