import numpy as np
from skimage import graph
import random


def _max_edge(g, src, dst, neighbor):
    try:
        w1 = g.edge[src][neighbor]['weight']
    except KeyError:
        w1 = None

    try:
        w2 = g.edge[dst][neighbor]['weight']
    except KeyError:
        w2 = None

    if w1 == None:
        return w2
    elif w2 == None:
        return w1
    else:
        return max(w1, w2)


def test_rag_merge():
    g = graph.rag.RAG()
    for i in range(10):
        g.add_edge(i, (i + 1) % 10, {'weight': i * 10})
        g.node[i]['labels'] = [i]

    for i in range(4):
        x = random.choice(g.nodes())
        y = random.choice(g.nodes())
        while x == y:
            y = random.choice(g.nodes())
        g.merge_nodes(x, y)

    for i in range(5):
        x = random.choice(g.nodes())
        y = random.choice(g.nodes())
        while x == y:
            y = random.choice(g.nodes())
        g.merge_nodes(x, y, _max_edge)

    idx = g.nodes()[0]
    assert sorted(g.node[idx]['labels']) == list(range(10))
    assert g.edges() == []


def test_threshold_cut():

    img = np.zeros((100, 100, 3), dtype='uint8')
    img[:50, :50] = 255, 255, 255
    img[:50, 50:] = 254, 254, 254
    img[50:, :50] = 2, 2, 2
    img[50:, 50:] = 1, 1, 1

    labels = np.zeros((100, 100), dtype='uint8')
    labels[:50, :50] = 0
    labels[:50, 50:] = 1
    labels[50:, :50] = 2
    labels[50:, 50:] = 3

    rag = graph.rag_meancolor(img, labels)
    new_labels = graph.threshold_cut(labels, rag, 10)

    # Two labels
    assert new_labels.max() == 1
