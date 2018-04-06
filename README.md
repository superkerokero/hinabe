# Naruhodo(なるほど)

[![Build Status](https://travis-ci.org/superkerokero/naruhodo.svg?branch=master)](https://travis-ci.org/superkerokero/naruhodo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/naruhodo.svg)](https://badge.fury.io/py/naruhodo)

[日本語はこちら](README-ja.md)

`naruhodo` is a python library for automatic semantic graph generation from human-readable text. Graphs generated by `naruhodo` are [networkx](https://networkx.github.io/) objects, so you can apply furthur garph analysis/processing conveniently. 

Supported languages:

* Japanese
* English(WIP)
* Chinese(WIP)

Supported semantic graph types:

* knowledge-structure-graph(KSG): A directed graph based on entity-predicate model of knowledge representation.
* dependency-structure-graph(DSG): A directed graph based on dependency structure.

 `naruhodo` provides basic visulization utilities using [nxpd](https://github.com/chebee7i/nxpd). A full-fledged visualization webapp [naruhodo-viewer](https://github.com/superkerokero/naruhodo-viewer) is also available. This webapp provides faster and interactive visualization of large graphs. 
 
### Knowledge structure graph(KSG)

Knowledge structure graph(KSG) tries to capture meaningful relationships between different entities. It is generated based on the dependency structure of the text.

In KSG, there are primarily two kinds of nodes:
* nodes that represent entities (entities)
* nodes that represent properties or actions (predicates)

Entity nodes are primarily connected by predicate nodes. Edges represent the relationship between these nodes. If an entity has a property or performs an action, it has an edge pointing to corresponding predicate nodes. If an entity is part of the property of another entity or the object of an action, it has an edge pointing from the predicate node to it.

This kind of graph structure is inspired by the way human brains store knowledge/information. Accurate and comprehensive KSG parsing is the main focus of `naruhodo`.

Below is an example of KSG generated by `naruhodo` using the following texts.

```
"田中一郎は田中次郎が描いた絵を田中三郎に贈った。"
"三郎はこの絵を持って市場に行った。"
"彼はしばらく休む事にした。"
```

![KSG generated from texts](img/KSG_example.png)


### Dependency structure graph (DSG)

[Dependency parsing](https://web.stanford.edu/~jurafsky/slp3/14.pdf) is the analysis of [dependency grammar](https://en.wikipedia.org/wiki/Dependency_grammar) on a block of text using computer programs. 
The directed linking nature of dependency grammar makes the result of dependency parsing directed graphs.
`naruhodo` generates denpendency structure graphs(DSG) directly from the output of dependency parsing programs. 

Below is an example of DSG generated by naruhodo using the following texts.

```
"田中一郎は田中次郎が描いた絵を田中三郎に贈った。"
"三郎はこの絵を持って市場に行った。"
"彼はしばらく休む事にした。"
```

![DSG generated from texts](img/DSG_example.png)

## Installation

`naruhodo` supports `python` version 3.4 and above.
You can install the library directly using pip:

```bash
pip install naruhodo
```

This will install the latest release version of `naruhodo`. 
The current development version of `naruhodo` can be installed from github repository directly using the following command:

```bash
pip install https://github.com/superkerokero/naruhodo/archive/dev.zip
``` 

`naruhodo` relies on external programs to do Japanese word and dependency parsing, so you need to have corresponding programs installed as well.

`naruhodo` is designed to support multiple backend parsers, but currently only the support for `mecab` + `cabocha` is implemented.

For guide on installing `mecab` and `cabocha`, please refer to this page:

[Amazon Linux に MeCab と CaboCha をインストール](https://qiita.com/january108/items/85c80769ea870c190eaa)

Support for other parsers such as `KNP` is planned in the future.

## Nodes-and-edges-specification

`naruhodo` stores graph information in a [networkx](https://networkx.github.io/) [`DiGraph`](https://networkx.github.io/documentation/latest/reference/classes/digraph.html) object. The properties of nodes and edges provided by naruhodo are listed in the following table.

* **Node properties**

  | Property | Description                                                                                                                     |
  |:--------:|---------------------------------------------------------------------------------------------------------------------------------|
  | name     | A string that stores the name of the node stored in the graph. This is what you use to refer to the node from graph object.     |
  | count    | An integer representing the number of this node being referred to. Can be used as an indicator of node's significance.          |
  | type     | An integer representing the type of the node. For meanings of integers, refer to the table of node types below.                 |
  | label     | A string that stores the normalized representation of the node. This is what you see from the visualizations.                   |
  | pro      | An integer representing the pronoun type of this node. For meanings of integers, refer to the table of pronoun types below.     |
  | NE       | An integer representing the named-entity(NE) type of this node. For meanings of integers, refer to the table of NE types below. |
  | negative | If chunk is negative 1, elif chunk double negtive(strongly positive) -1, else 0  |
  | question | If chunk contains ? 1, else 0. |
  | passive | If chunk is passive 1, else 0. |
  | compulsory  | If chunk is compulsory 1, else 0. |
  | tense | If chunk has no tense or present 0, elif past -1, elif present continuous 1 |
  | pos[0:n-1]      | A list of integers representing the id of sentences where this node appears.                                                    |
  | lpos[0:n-1]      | A list of integers representing the id of chunk in the sentence it appears.                                                    |
  | surface[0:n-1]  | A list of strings that stores the surfaces of this node(original form as it appears in the text).                                         |
  | yomi[0:n-1]  | A list of strings that stores the yomi of the corresponding surface of this node.                    |
  | sub  | A string that stores the subject of this node(if none it will be an empty string).                    |

* **Node types**

  | Type ID | Description   |
  |---------|---------------|
  | -1      | Unknown type  |
  | 0       | Noun          |
  | 1       | Adjective     |
  | 2       | Verb          |
  | 3       | Conjective    |
  | 4       | Interjection  |
  | 5       | Adverb        |
  | 6       | Connect       |

* **Pronoun types**

  | Pronoun ID | Description                       |
  |------------|-----------------------------------|
  | -1         | Not a pronoun(or unknown pronoun) |
  | 0          | Demonstrative-location            |
  | 1          | Demonstrative-object              |
  | 2          | Personal-1st                      |
  | 3          | Personal-2nd                      |
  | 4          | Personal-3rd                      |
  | 5          | Indefinite                        |
  | 6          | Inclusive                         |
  | 7          | Omitted subject                   |


* **Named-entity types**

  | NE ID | Description                  |
  |-------|------------------------------|
  | 0     | Not named-entity(or unknown) |
  | 1     | Person                       |
  | 2     | Location                     |
  | 3     | Organization                 |
  | 4     | Number/Date                  |

* **Edge properties**

  | Property | Description                                                                                                        |
  |----------|--------------------------------------------------------------------------------------------------------------------|
  | weight   | An integer representing the number of appearance of this edge. Can be used as an indicator of edge's significance. |
  | label    | A string that stores the label of this edge.                                                                       |
  | type     | A string that stores the type of this edge. For details, refer to the table of edge types below.                   |

* **Edge types**

  | Type    | Description                                |
  |---------|--------------------------------------------|
  | none    | Unknown type(also used as DSG edges)       |
  | sub     | Edge from a subject to predicate           |
  | autosub | Edge from a potential subject to predicate |
  | obj     | Edge from a predicate to object            |
  | aux     | Edge from auxiliary to predicate           |
  | cause   | Edge from potential cause to result        |
  | coref   | Edge from potential antecedent to pronoun  |
  | synonym | Edge from potential synonym to an entity   |
  | para    | Edge between parallel entities             |
  | attr    | Edge from potential attribute to an entity |
  | stat    | Edge from potential subject to a statement |

## Tutorial

The tutorial of `naruhodo` is provided as `ipynb` files in the tutorial folder. You can view it directly in your browser.

[Tutorial notebook for Japanese text parsing](https://github.com/superkerokero/naruhodo/blob/master/tutorial/Tutorial-Ja.ipynb)

## Python-API

The complete python API document for `naruhodo` can be found here:

[`naruhodo` Python API Reference](https://superkerokero.github.io/naruhodo).

This document is generated automatically from source code using [pdoc](https://github.com/BurntSushi/pdoc), so it is always up-to-date.

## Change-Log

You can find the change log of `naruhodo` [here](https://superkerokero.github.io/naruhodo).

## Development status and some personal comments

`naruhodo` is still in development state(especially KSG related part), so you might find it outputs weird results sometimes. If you like the idea and want to help improve the library, feel free to create a pull request on github.

Here are some of my thoughts on the development of `naruhodo` :

* ### Improvement on the quality of generated graph (0.2 ~ 0.5)
    
    As you can see from the source code, `naruhodo` relies mostly on rule-based system to parse given information.
    And for a subject as large and complex as a language, long-term testing and procedural improvement of the program is neccessary before it can go anywhere.

    Currently the knowledge structure graph(KSG) generated by `naruhodo` is below my expectation for large amount of input texts. Improvement will come from furthur examination on varieties of input text and corresponding refinement of parsing logic.

    As a rule-based system, it certainly has its limitations such as completely resolving coreferences. But I believe in the realm of NLP, especially in rudimentary information parsing tasks, rule-based system can be used to make practical applications. Recent advances in statitics-based techniques such as deep learning seem promising. But almost all of these techniques require large amount of labelled data, which is hard to retrieve. The rule-based approach taken here is more or less an Ab Initio way of looking at some NLP problems(which doesn't take any training data before making useful predictions). My hope is that applications like this may at least alleviate the pain of collecting large amount of labelled data by automating some of the tedious tasks. `naruhodo` is my personal experiment on how far rule-based system can go in the world of NLP. It may fail to be practically useful, but I am sure it is going to be an interesting journey. 

* ### Improving coreference resolution performance (0.2.1 ~)

    [Coreference resolution](https://en.wikipedia.org/wiki/Coreference) is the task of finding all expressions that refer to the same entity in a text. Without proper coreference resolution, generated KSG does not capture all meaningful information, and its usability will be quite limited. Currently `naruhodo` has a primitive coreference resolution added from 0.2.1, but the performance is quite limited. I am experimenting with some published works on this topic. A method based on word embeddings and reinforcement learning might be added to `naruhodo` first starting from version 0.5 ~.

* ### Support for more backends (0.5 ~)
    
    There aren't many Japanese parsing programs available on the internet yet. Aside of `mecab` + `cabocha`, the most usable parsing program seems to be `juman(++)` + `knp`. The output format of `knp` does contain extra useful information and can be more accurate than `cabocha` in some situations. But its output lacks a unified scheme, making it difficult to use. Another important fact is that `juman(++)` + `knp` parsing can be very time consuming compared to `mecab` + `cabocha`, which limits its use cases.

    I am looking into some fast generic libraries like `spaCy` as well. Though Japanese is not the officially supported language for the moment. 

    To summarize, though `naruhodo` is designed to support multiple backends, since its current focus is Japanese only, adding support for other backends is not a priority.

* ### Support for other languages(?~)
    
    Japanese is the only language `naruhodo` supports now. Besides my personal interest, I chosen Japanese because it has some unique characteristics that make it both challenging and rewarding. In my opnion, the difficulty regarding Japanese mostly comes from its ambiguity in the expression(for example, the subject is frequently ommited in Japanese) and large amount of word transformations(the same verb can have as many as 10+ forms).

    From a practical point of view, languages such as English and Chinese are in potentially large demand. So I am thinking about expanding the library to these popular languages in the future, if the rule-based approach taken by `naruhodo` proves to be usable afterall.

* ### Adding statistics-based approaches(?~)
    
    It seems that everybody is excited about machine learning these days. And I do see huge application potential in techniques like reinforcement learning and generative adversarial models. I do have some thoughts about the applications of these techniques to some specific knowledge retrieval problems. For example, the coreference problem is obviously outside the reach of any rule-based systems, and a reinforcement learning based approach seems quite attractive in this case(provided that we have a real-time feedback system from users).
    
    As my understanding of machine learning techniques improves, some statistics-based approaches may be added in the future.

* ### Applications based on DSG and KSG(new projects)
    
    I think information of DSG and KSG is especially useful in the realm of automating information retrieval processes. This includes, but not limited to, 
    * automatic text summarization
    * knowledge base generation for Q&A system and translation system 
    * generic sentiment analysis

    As the quality of KSG generated by `naruhodo` improves, I will try to apply it to some of these areas.

