import networkx as nx
from naruhodo.utils.communication import Subprocess
from naruhodo.backends.cabocha import CabochaClient
from naruhodo.utils.dicts import UncountedDict
from naruhodo.core.base import AnalyzerBase
from naruhodo.utils.misc import getNodeProperties, getEdgeProperties

class DependencyAnalyzer(AnalyzerBase):
    """Analyze the input text and store the information into a dependency graph(DG)."""
    def __init__(self):
        """Setup a subprocess for backend."""
        super().__init__()
        self.proc = Subprocess('cabocha -f1')
        
    def addToDG(self, inp):
        """Take in a string input and add it to the DG."""
        cabo = CabochaClient()
        cabo.add(self.proc.query(inp))
        for chunk in cabo.chunks:
            # Add nodes.
            # print(chunk.id, chunk.surface, chunk.type, chunk.parent)
            try:
                if chunk.type in [0, 1, 2, 6]:
                    if chunk.main not in UncountedDict: 
                        self.nodes[chunk.main]['count'] += 1
                    else:
                        self.nodes[chunk.main]['count'] == 1
            except KeyError:
                self.nodes[chunk.main] = {
                    'count': 1,
                    'type': chunk.type,
                    'rep': chunk.main,
                    'len': len(chunk.main)
                }
            # Add edges.
            try:
                if chunk.type in [0, 1, 2, 3, 4, 5, 6] and cabo.chunks[chunk.parent].type in [0, 1, 2, 3, 4, 5, 6]:
                    if True:#chunk.main != cabo.chunks[chunk.parent].main:
                        if chunk.main not in UncountedDict and cabo.chunks[chunk.parent].main not in UncountedDict:
                            self.edges[(chunk.main, cabo.chunks[chunk.parent].main)]['weight'] +=1
                        else:
                            self.edges[(chunk.main, cabo.chunks[chunk.parent].main)]['weight'] == 1
            except KeyError:
                self.edges[(chunk.main, cabo.chunks[chunk.parent].main)] = {
                    'weight': 1,
                    'label': chunk.func + ' '
                }
        # Add nodes to DAG.
        for key, val in self.nodes.items():
            self.G.add_node(key, **getNodeProperties(val))
        # Add edges to DAG.
        for key, val in self.edges.items():
            self.G.add_edge(*key, **getEdgeProperties(val))
            
    def addUrlsToDG(self, urls):
        """Add the information from given urls to DG."""
        context = self._grabTextFromUrls(urls)
        for sent in context:
            self.addToDG(sent)