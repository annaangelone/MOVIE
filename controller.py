import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        rank = self._view._txt_rank.value

        try:
            rankFloat = float(rank)

        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Inserire un numero reale tra 0 e 10"))
            self._view.update_page()
            return

        if rankFloat < 0 or rankFloat > 10:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Inserire un numero reale tra 0 e 10"))
            self._view.update_page()
            return

        self._model.buildGraph(rankFloat)

        self._view._txt_result.controls.append(ft.Text(f"GRAFO CORRETTAMENTE CREATO"))

        self._view._txt_result.controls.append(ft.Text(f"#Nodi: {self._model.getNumNodes()}"))
        self._view._txt_result.controls.append(ft.Text(f"#Archi: {self._model.getNumEdges()}"))

        self._view._btnGradoMax.disabled = False

        self._view.update_page()

    def handleGradoMax(self,e):
        filmBest, gradoMax = self._model.filmGradoMax()
        self._view._txt_result.controls.append(ft.Text(f"FILM GRADO MASSIMO:"))

        self._view._txt_result.controls.append(ft.Text(f"{filmBest.id} - {filmBest.name} ({gradoMax})"))

        self._view.update_page()

    def handlePercorso(self, e):
        movie = int(self._view._ddFilm.value)

        if movie is None:
            self._view.create_alert("Selezionare un film")
            return


        movieObj = self._model.getMovie(movie)

        path, score = self._model.getPercorso(movieObj)

        self._view._txt_result.controls.append(ft.Text(f"Nodo di partenza: {movieObj.id} - {movieObj.name}"))
        self._view._txt_result.controls.append(ft.Text(f"Lunghezza del cammino: {score}"))

        for i in range(len(path) - 1):
            peso = self._model.getPeso(path[i], path[i+1])
            self._view._txt_result.controls.append(ft.Text(f"{path[i]} --> {path[i+1]} : {peso}"))

        self._view.update_page()



    def fillDD(self):
        movies = self._model._movies

        for m in movies:
            self._view._ddFilm.options.append(ft.dropdown.Option(key=m.id, text=m.name))

        self._view.update_page()