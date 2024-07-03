import copy

import networkx as nx
from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._movies = DAO.getMovies()
        self._idMap = {}

        for m in self._movies:
            self._idMap[m.id] = m

        self._bestPath = []
        self._bestScore = 0


    def buildGraph(self, rank):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._movies)

        for u in self._grafo.nodes:
            for v in self._grafo.nodes:
                if u != v and u.rank >= rank and v.rank >= rank:
                    peso = DAO.getEdges(u.id, v.id)
                    if peso:
                        self._grafo.add_edge(u, v, weight=peso[0])



    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def filmGradoMax(self):
        gradoMax = 0
        nodoBest = None
        for n in self._grafo.nodes:
            vicini = self._grafo.neighbors(n)

            pesoNodo = 0
            for v in vicini:
                pesoNodo += self._grafo[n][v]["weight"]

            if pesoNodo > gradoMax:
                gradoMax = pesoNodo
                nodoBest = n

        return nodoBest, gradoMax


    def getPercorso(self, nodoInizio):
        self._bestPath = []
        self._bestScore = 0

        parziale = [nodoInizio]

        listaVicini = []

        vicini = list(self._grafo.neighbors(nodoInizio))

        if len(vicini) > 0:
            for v in self._grafo.neighbors(nodoInizio):
                edgeV = self._grafo[parziale[-1]][v]["weight"]
                listaVicini.append((v, edgeV))
            listaVicini.sort(key=lambda x: x[1])

            parziale.append(listaVicini[0][0])
            self._ricorsione(parziale)

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        if len(parziale) > self._bestScore:
            self._bestScore = len(parziale)
            self._bestPath = copy.deepcopy(parziale)

        listaVicini = []
        for v in self._grafo.neighbors(parziale[-1]):
            edgeV = self._grafo[parziale[-1]][v]["weight"]
            listaVicini.append((v, edgeV))
        listaVicini.sort(key=lambda x: x[1])

        for v1 in listaVicini:
            if (self._grafo[parziale[-2]][parziale[-1]]["weight"] < v1[1]):
                parziale.append(v1)
                self._ricorsione(parziale)
                parziale.pop()
                return

        parziale.append(listaVicini[0][0])



    def getPeso(self, v1, v2):
        peso = self._grafo[v1][v2]["weight"]
        return peso

    def getMovie(self, movieID):
        return self._idMap[movieID]