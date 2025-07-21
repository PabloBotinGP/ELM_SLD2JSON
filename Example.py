import logging
import networkx as nx
from rex import init_logger
from elm.base import ApiBase
from elm.tree import DecisionTree

init_logger('elm.tree')

G = nx.DiGraph(text='hello', name='Grant',
                   api=ApiBase(model='gpt-35-turbo'))

G.add_node('init', prompt='Say {text} to {name}')
G.add_edge('init', 'next', condition=lambda x: 'Grant' in x)
G.add_node('next', prompt='How are you?')

tree = DecisionTree(G)
out = tree.run()

print(tree.all_messages_txt)