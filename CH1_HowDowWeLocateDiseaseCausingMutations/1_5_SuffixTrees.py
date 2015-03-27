__author__ = 'ilap'

from bioLibrary import *

def suffixTrie (text):

    trie = trieConstruction(text)

    idx = 0
    for i in text:
        pattern = text[idx:]
        print pattern,idx
        print
        idx += 1

'''
CS: Constructing a Suffix Tree
'''
def modifiedSuffixTrieConstruction (text):
    # Sort them first

    trie = [{}] # Root, with no edges and nodes
    for i in range (len (text)):
        current_node =  0

        for j,current_symbol in enumerate (text):
            print i,j, current_symbol

            print "TRIE", current_node, trie
            nodes = trie[current_node]
            print "NODES", nodes

            if nodes.has_key(current_symbol):
                #print "ALMA"
                current_node = nodes[current_symbol]
            else:
                new_node = len (trie)
                print "NEW_NODE", new_node
                trie.append({})
                trie[current_node][current_symbol] = (new_node,j)
                print str(current_node) + "->" + str (nodes[current_symbol]) +":" + current_symbol
                current_node = new_node

    return trie

'''
def maximalNonBranchingPath (graph):
    paths = []
    for
'''

#print suffixTrie("panamabananas$")

#print modifiedSuffixTrieConstruction("panamabananas$")