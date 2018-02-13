import re
import itertools
import networkx as nx
from nxpd import draw
from naruhodo.utils.scraper import NScraper
from naruhodo.utils.misc import exportToJsonFile

class AnalyzerBase(object):
    """Prototype of the analyzer classes."""
    def __init__(self):
        """Constructor."""
        self.G = nx.DiGraph()
        self.nodes = dict()
        self.edges = dict()
        self.re_sent = re.compile('([^　！？。]*[！？。])')
        self.re_parentheses = re.compile('\（[^)]*\）')

    def _parseToSents(self, context):
        """Parse given context into list of individual sentences."""
        #return [self.re_parentheses.sub("", sent.strip()) for sent in self.re_sent.split(context) if self.re_parentheses.sub("", sent.strip()) != ""]
        return [sent.strip().replace('*', "-") for sent in self.re_sent.split(context) if sent.strip() != ""]

    def _grabTextFromUrls(self, urls):
        """Parse given url(or a list of urls) and return the text content of the it."""
        # Handle the single url case.
        if isinstance(urls, str):
            urls = [urls]
        # Initialize scraper.
        scpr = NScraper()
        ret = list()
        # loop through urls to extract text.
        for url in urls:
            text = scpr.getUrlContent(url)
            for block in text:
                try:
                    from polyglot.detect import Detector
                    lang = Detector(block).language.name
                    if lang != '日本語':
                        print("サポートされてない言語: {0}".format(lang))
                        continue
                except:
                    print("Polyglot unavailable. Language detection disabled.")
                for line in block.splitlines():
                    ret = list(itertools.chain(ret, self._parseToSents(line)))
        return ret

    def reset(self):
        """Reset the content of generated graph to empty."""
        self.G = nx.DiGraph()
        self.nodes = dict()
        self.edges = dict()

    def exportJSON(self, filename):
        """Export current graph to a JSON file on disk."""
        exportToJsonFile(self.G, filename)

    def plotDiGraphNotebook(self):
        '''Plot directional graph in jupyter notebook using nxpd.'''
        # span = list(nx.weakly_connected_component_subgraphs(self.G))
        return draw(self.G, show='ipynb')
    
    def plotDiGraph(self, filename):
        '''Output directional graph to a png file using nxpd.'''
        return draw(self.G, filename=filename)