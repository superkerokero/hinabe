from naruhodo.utils.dicts import ProDict, MeaninglessDict, VerbLikeFuncDict, VerbLikeExclude
from naruhodo.utils.misc import preprocessText
import re

class CaboChunk(object):
    """Class for cabocha chunks"""
    def __init__(self, chunk_id, parent):
        """Initialize a chunk."""
        self.id = chunk_id    
        """
        id of the chunk.
        """

        self.parent = parent  
        """
        parent id of this chunk.
        """

        self.children = None 
        """
        list of children of this chunk.
        """

        self.nouns = list()   
        """
        list of nouns 名詞
        """

        self.verbs = list()   
        """
        list of verbs 動詞
        """

        self.adjs = list()    
        """
        list of adjectives 形容詞
        """

        self.postps = list()  
        """
        list of postpositions 助詞
        """

        self.auxvs = list()   
        """
        list of auxilary verbs 助動詞
        """

        self.conjs = list()   
        """
        list of conjection 接続詞
        """

        self.interjs = list() 
        """
        list of interjections 感動詞
        """

        self.signs = list()   
        """
        list of signs 記号
        """

        self.advs = list()    
        """
        list of adverbs 副詞
        """

        self.connects = list() 
        """
        list of connects 連体詞
        """

        self.headings = list() 
        """
        list of headings 接頭詞
        """

        self.main = "" 
        """
        Main component of the chunk.
        """

        self.main_surface = ""
        """
        Surface of the main component.
        """

        self.func = "" 
        """
        Functional component of the chunk.
        """

        self.surface = "" 
        """
        Original surface of the chunk.
        """

        self.negative = 0 
        """
        If chunk is negative 1, elif chunk double negtive(strongly positive) -1, else 0 
        """

        self.passive = 0 
        """
        If chunk is passive 1, else 0.
        """

        self.compulsory = 0 
        """
        If chunk is compulsory 1, else 0.
        """

        self.question = 0 
        """
        If chunk contains ? 1, else 0.
        """

        self.yomi = ""
        """
        Contains the yomi of this chunk's surface.
        """

        self.tense = 0 
        """
        If chunk has no tense or present 0, elif past -1, elif present continuous 1
        """
        
        self.type = -1
        """
        Type of this chunk.
        -------------------
        -1: unknown type
         0: noun
         1: adjective
         2: verb
         3: conjective
         4: interjection
         5: adverb
         6: connect
        """
        
        self.type2 = -1
        """
        2nd type of this chunk.
        -----------------------
        -1: no 2nd type
         0: noun
         1: adjective
         2: verb
        """
        
        self.NE = 0
        """
        Named entity type of this chunk.
        The name of NE type can be retrieved using 
        'NEList' in naruhodo.utils.dicts like
        NEtype = NEList[NE].
        --------------------------------
        0: no named entity(or unknown)
        1: person
        2: location
        3: organization
        4: number
        5: general
        """
        
        self.pro = -1
        """
        Pronoun type of this chunk. 
        ---------------------------
        -1: no pronoun(or unknown)
         0: demonstrative-loc
         1: demonstrative-obj
         2: personal(1st)
         3: personal(2nd)
         4: personal(3rd)
         5: indefinite
         6: inclusive
         7: omitted *This type is assigned by naruhodo.core.KnowledgeCoreJa.
        """

        self.npro = 0
        """
        Rank of this pronoun in the sentence it appears.
        """

        self.meaning = ""
        """
        If the main of this chunk is in MeaninglessDict, 
        this variable will be set to the main of its child node that contains its meaning. 
        """
    
    def add(self, inp):
        """Add components to chunk lists."""
        # if inp[1] != "記号" or inp[0] == "？":
        #     self.surface += inp[0]
        self.surface += inp[0]
        if len(inp) > 8:
            self.yomi += inp[8]
        else:
            self.yomi += inp[0]
        elem = {
            'surface': inp[0],
            'lemma' : inp[7],
            'labels': inp[2:7],
        }
        if inp[1] == "名詞":
            self.nouns.append(elem)
        elif inp[1] == "動詞":
            self.verbs.append(elem)
        elif inp[1] == "形容詞":
            self.adjs.append(elem)
        elif inp[1] == "助詞":
            self.postps.append(elem)
        elif inp[1] == "助動詞":
            self.auxvs.append(elem)
        elif inp[1] == "接続詞":
            self.conjs.append(elem)
        elif inp[1] == "感動詞":
            self.interjs.append(elem)
        elif inp[1] == "記号":
            self.signs.append(elem)
        elif inp[1] == "副詞":
            self.advs.append(elem)
        elif inp[1] == "連体詞":
            self.connects.append(elem)
        elif inp[1] == "接頭詞":
            self.headings.append(elem)
        else:
            pass
        
    def _cleanUp(self):
        """Clean up all the lists stored in the object that is no longer needed."""
        del self.nouns
        del self.verbs
        del self.adjs
        del self.postps
        del self.auxvs
        del self.conjs
        del self.interjs
        del self.signs
        del self.advs
        del self.connects
        del self.headings
        
    def _getMain(self):
        """Get the main component of the chunk."""
        if len(self.nouns) > 0 and self.nouns[0]['labels'][0] not in ['非自立', '接尾']:
            self.main = "".join([x['lemma'] for x in self.nouns if x['labels'][0] != '非自立'])
            self.main_surface = "".join([x['surface'] for x in self.nouns if x['labels'][0] != '非自立'])
            self.type = 0
            if len(self.adjs) > 0:
                if self.adjs[0]['lemma'] == "ない":
                    self.negative = 1
            # Corrections for special patterns.
            if self.nouns[0]['labels'][0] == 'サ変接続':
                if len(self.nouns) > 1 and len(self.verbs) == 0:
                    self.type = 0
                else: 
                    self.type = 2
                    self.type2 = 0
            elif self.nouns[0]['labels'][0] == '形容動詞語幹':
                if len(self.nouns) > 1:
                    self.type = 0
                else:
                    self.type = 1
                    self.type2 = 2
            # NE recognition.
            elif self.nouns[0]['labels'][0] == '固有名詞':
                if self.nouns[0]['labels'][1] == '人名':
                    self.NE = 1
                elif self.nouns[0]['labels'][1] == '地域':
                    self.NE = 2
                elif self.nouns[0]['labels'][1] == '組織':
                    self.NE = 3
                elif self.nouns[0]['labels'][1] == '一般':
                    self.NE = 5
                else:
                    pass
            # Pronoun identification(for correference analysis.)
            elif self.nouns[0]['labels'][0] == '代名詞':
                if self.nouns[0]['lemma'] in ProDict['demonstrative-loc']:
                    self.pro = 0
                elif self.nouns[0]['lemma'] in ProDict['demonstrative-obj']:
                    self.pro = 1
                elif self.nouns[0]['lemma'] in ProDict['personal1st']:
                    self.pro = 2
                elif self.nouns[0]['lemma'] in ProDict['personal2nd']:
                    self.pro = 3
                elif self.nouns[0]['lemma'] in ProDict['personal3rd']:
                    self.pro = 4
                elif self.nouns[0]['lemma'] in ProDict['indefinite']:
                    self.pro = 5
                elif self.nouns[0]['lemma'] in ProDict['inclusive']:
                    self.pro = 6
                else:
                    pass
            elif self.nouns[0]['labels'][0] == '数':
                self.main = "".join([x['lemma'] for x in self.nouns])
                self.main_surface = "".join([x['surface'] for x in self.nouns])
                self.NE = 4
            else:
                pass
        elif len(self.nouns) > 0 and self.nouns[0]['lemma'] in MeaninglessDict:
            if len(self.verbs) > 0:
                self.main = self.verbs[0]['surface']
                self.main_surface = self.verbs[0]['surface']
            self.main += self.nouns[0]['lemma']
            self.main_surface += self.nouns[0]['surface']
            self.type = 0
        elif len(self.adjs) > 0:
            self.main = self.adjs[0]['lemma']
            self.main_surface = self.adjs[0]['surface']
            self.type = 1
            if self.adjs[0]['lemma'] == "ない":
                self.negative = 1
        elif len(self.verbs) > 0:
            self.main = self.verbs[0]['lemma']
            self.main_surface = self.verbs[0]['surface']
            self.type = 2
        elif len(self.advs) > 0:
            self.main = self.advs[0]['lemma']
            self.main_surface = self.advs[0]['surface']
            self.type = 5
        elif len(self.conjs) > 0:
            self.main = self.conjs[0]['lemma']
            self.main_surface = self.conjs[0]['surface']
            self.type = 3
        elif len(self.interjs) > 0:
            self.main = self.interjs[0]['lemma']
            self.main_surface = self.interjs[0]['surface']
            self.type = 4
        elif len(self.connects) > 0:
            self.main = self.connects[0]['lemma']
            self.main_surface = self.connects[0]['surface']
            self.type = 6
        elif len(self.postps) > 0:
            self.main = self.postps[0]['lemma']
            self.main_surface = self.postps[0]['surface']
        elif len(self.auxvs) > 0:
            self.main = self.auxvs[0]['lemma']
            self.main_surface = self.auxvs[0]['surface']
        elif len(self.signs) > 0:
            if len(self.nouns) > 0:
                self.main = self.nouns[0]['lemma']
                self.main_surface = self.nouns[0]['surface']
            else:
                self.main = self.signs[0]['lemma']
                self.main_surface = self.signs[0]['surface']
        elif len(self.nouns) > 0 and self.nouns[0]['labels'][0] == '非自立':
            self.main = self.nouns[0]['lemma']
            self.main_surface = self.nouns[0]['surface']
            self.type = 0
        else:
            self.main = 'UNKNOWN'
        if len(self.headings) > 0:
            self.main = "\n".join([x['lemma'] for x in self.headings]) + self.main
            self.main_surface = "\n".join([x['surface'] for x in self.headings]) + self.main_surface
        # Convert main with no lemma to surface
        if self.main.find("*") != -1:
                self.main = self.main_surface
        
    def _getFunc(self):
        """Get the func component of the chunk."""
        # Get func by excluding main from surface.
        self.func = self.surface.replace(self.main_surface, "")
        # Process func to get properties
        if len(self.verbs) > 0:
            for item in self.verbs:
                if item['labels'][0] == '接尾':
                    if item['lemma'] == "れる" or item['lemma'] == "られる":
                        self.passive = 1
                    elif item['lemma'] == "させる":
                        self.compulsory = 1
                elif item['labels'][0] == "非自立":
                    if item['lemma'] == "いる":
                        self.tense = 1
        if len(self.postps) > 0:
            if self.parent == -1:
                for item in self.postps:
                    if item['lemma'] in ["の", "なの", "か"]:
                        self.question = 1
        if len(self.auxvs) > 0:
            neg = sum([
                [x['lemma'] for x in self.auxvs].count('ん'), 
                [x['lemma'] for x in self.auxvs].count('ない'),
                [x['lemma'] for x in self.auxvs].count('ぬ'),
                [x['lemma'] for x in self.auxvs].count('まい')
            ])
            if neg == 1:
                if len(self.signs) > 0 and any([self.signs[x]['surface'] == '？' for x in range(len(self.signs))]):
                    pass
                else:
                    self.negative = 1
            elif neg > 1:
                if neg % 2 == 0:
                    self.negative = -1
                else:
                    self.negative = 1
            else:
                pass
            if any([self.auxvs[x]['lemma'] == "た" for x in range(len(self.auxvs))]):
                self.tense = -1

        # Fix for nouns used as verbs.
        for item in VerbLikeFuncDict:
            if self.func.find(item) != -1 and self.func not in VerbLikeExclude:
                self.type = 2

        if len(self.signs) > 0:
            for item in self.signs:
                if item['surface'] ==  '？':
                    self.question = 1

        # Fix for special words.
        if self.main == "できる" and self.func not in ["た", "ます", "いるて"]:
            self.type = 5
        
    def processChunk(self, pos, npro):
        """Process the chunk to get main and func component of it."""
        self._getMain()
        self._getFunc()
        # Modify pronouns
        if self.pro != -1:
            self.main += "[{0}@{1}]".format(pos, npro)
            self.npro = npro
        # Add tense label to main
        if self.tense == -1:
            self.main += "\n(過去)"
        elif self.tense == 1:
            self.main += "\n(現在)"
        # Add compulsory label to main
        if self.compulsory == 1:
            self.main += "\n(強制)"
        if self.passive == 1:
            self.main += "\n(被動)"
        # Add question label to main
        if self.question == 1:
            self.main += "\n(質問)"
        # Add negative label to main
        if self.negative == 1:
            self.main += "\n(否定)"
        elif self.negative == -1:
            self.main += "\n(二重否定)"
        self._cleanUp()

class CabochaClient(object):
    """Class for CaboCha backend."""
    def __init__(self):
        """Initialize a native database."""
        self.rsplit = re.compile(r'[,]+|\t')
        self.chunks = list()
        self.root = None
        self.npro = 0
                
    def add(self, inp, pos=0):
        """Takes in the block output from CaboCha and add it to native database."""
        ck = None
        for elem in inp.splitlines():
            if elem[0] == '*':
                if ck is not None:
                    ck.processChunk(pos, self.npro)
                    if ck.pro != -1:
                        self.npro += 1
                    self.chunks.append(ck)
                ck = CaboChunk(*self._processHead(elem))
            else:
                ck.add(self.rsplit.split(elem))
        ck.processChunk(pos, self.npro)
        if ck.pro != -1:
            self.npro += 1
        self.chunks.append(ck)
        # Get children list and store in self.childrenList
        self._getChildrenList()
        self._processMeaningless()
        self._processNegative()
                
    def _processHead(self, inp):
        """Takes in the head of the chunk and process ids / parents."""
        elem = inp.split()
        return int(elem[1]), int(elem[2][:-1])

    def _getChildrenList(self):
        """Process to get the list of children for each chunk."""
        nck = len(self.chunks)
        self.childrenList = [list() for x in range(nck)]
        for i in range(nck):
            pid = self.chunks[i].parent
            if pid == -1:
                self.root = i
            else:
                self.childrenList[pid].append(i)
        for i in range(nck):
            self.chunks[i].children = self.childrenList[i]

    def _processMeaningless(self):
        """This function makes meaningless words tagged with its meaning."""
        nck = len(self.chunks)
        for i in range(nck):
            if preprocessText(self.chunks[i].main) in MeaninglessDict:
                if len(self.childrenList[i]) > 0:
                    self.chunks[i].meaning = self.chunks[self.childrenList[i][-1]].main
                    self.chunks[i].main = "({0})\n{1}".format(
                        self.chunks[self.childrenList[i][-1]].surface,
                        self.chunks[i].main
                    )

    def _processNegative(self):
        """This function makes the words that has negative child tagged negative."""
        nck = len(self.chunks)
        for i in range(nck):
            if preprocessText(self.chunks[i].main) in ["ない", ]:
                if len(self.childrenList[i]) > 0:
                    self.chunks[self.childrenList[i][-1]].main += "\n(否定)"
                    self.chunks[self.childrenList[i][-1]].negative = 1
                    self.chunks[i].meaning = self.chunks[self.childrenList[i][-1]].main
                self.chunks[i].main = self.chunks[i].main.replace("\n(否定)", "")