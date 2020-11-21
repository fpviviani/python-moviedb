import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class MainView():

    def __init__(self, mainTk, mainController):
        # Define os atributos da janela
        self.mainTk = mainTk
        self.mainTk.title("Movie Database")
        self.mainTk.geometry('400x370')
        self.mainController = mainController

        # Instancia a barra de opções
        self.menubar = tk.Menu(self.mainTk, bg='#366998')
        self.blankmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="".ljust(83), menu=self.blankmenu, activebackground="#366998")
        self.menubar.add_command(label="Ajuda", foreground="white", activebackground="#366998", command=lambda:self.helpClick())
        self.mainTk.config(menu=self.menubar)

        # Instancia os frames da janela
        self.frameTitle = tk.Frame(self.mainTk)
        self.frameTitle.grid(row=0, column=0)
        self.frameServer = tk.Frame(self.mainTk)
        self.frameServer.grid(row=1, column=0)
        self.frameReturn = tk.Frame(self.mainTk)
        self.frameReturn.grid(row=2, column=0)
        self.frameInputMovie = tk.Frame(self.mainTk, width=40)
        self.frameInputMovie.grid(row=3, column=0)
        self.frameInputPerson = tk.Frame(self.mainTk, width=40)
        self.frameInputPerson.grid(row=4, column=0, pady=(5, 0))
        self.frameButtons = tk.Frame(self.mainTk)
        self.frameButtons.grid(row=5, column=0, pady=(20, 10), padx=3)

        # Instancia os labels da janela
        self.labelGUI = tk.Label(self.frameTitle, text="Movie Database", font=(None, 18))
        self.labelGUI.pack(pady=(10, 0))
        self.labelServer = tk.Label(self.frameServer, text="Output:", bg="#232323", fg="#329C28", width=47)
        self.labelServer.pack(pady=(10, 0))
        self.labelResponseString = tk.StringVar()
        self.labelResponse = tk.Label(self.frameReturn, textvariable=self.labelResponseString, bg="#232323", fg="#329C28", width=47, height=6)
        self.labelResponse.pack(pady=(0, 10))

        # Instancia os inputs e buttons da janela
        self.inputParametersMovie = tk.Entry(self.frameInputMovie, width=33)
        self.inputParametersMovie.insert(0, 'Nome do filme')
        self.inputParametersMovie.pack(side="left", padx=(0, 5))

        self.buttonSubmitMovie = tk.Button(self.frameInputMovie, text="Buscar filme", width=10)
        self.buttonSubmitMovie.pack(side="right")
        self.buttonSubmitMovie.bind("<Button-1>", lambda event, arg=self.inputParametersMovie: self.searchMovieClick(event, self.inputParametersMovie.get()))

        self.inputParametersPerson = tk.Entry(self.frameInputPerson, width=33)
        self.inputParametersPerson.insert(0, 'Nome da pessoa')
        self.inputParametersPerson.pack(side="left", padx=(0, 5))

        self.buttonSubmitPerson = tk.Button(self.frameInputPerson, text="Buscar pessoa", width=10)
        self.buttonSubmitPerson.pack(side="right")
        self.buttonSubmitPerson.bind("<Button-1>", lambda event, arg=self.inputParametersPerson: self.searchPersonClick(event, self.inputParametersPerson.get()))

        self.buttonMovies = tk.Button(self.frameButtons, text="Inserir filmes populares", width=21)
        self.buttonMovies.pack(side="left")
        self.buttonMovies.bind("<Button-1>", self.movieClick)

        self.buttonPersons = tk.Button(self.frameButtons, text="Inserir pessoas populares", width=21)
        self.buttonPersons.pack(side="left")
        self.buttonPersons.bind("<Button-1>", self.personClick)
            
    # Função para exibir um texto de ajuda sobre a aplicação
    def helpClick(self):
        helpTk = tk.Tk()
        helpTk.resizable(width=False, height=False)
        helpTk.title("Ajuda")
        helpTk.geometry('400x300')

        frameHelp = tk.Frame(helpTk)
        frameHelp.pack(pady=(10, 0))

        labelHelp = tk.Label(frameHelp, text="O primeiro input busca e\ninsere no banco um filme específico.\n\nO segundo input busca e\ninsere no banco uma pessoa específica.\n\nOs dois botões inserem os filmes e\npessoas mais populares\ndo momento no banco, respectivamente.", font=(None, 14))
        labelHelp.pack()

        helpTk.mainloop()
        pass

    # Função para buscar pela pessoa digitada no input
    def searchPersonClick(self, event, personName):
        self.mainController.searchPerson(personName)
    
    # Função para buscar pelo filme digitado no input
    def searchMovieClick(self, event, personName):
        self.mainController.searchMovie(personName)

    # Função para buscar os filmes populares
    def movieClick(self, event):
        self.mainController.getTrendingMovie()

    # Função para buscar as pessoas populares
    def personClick(self, event):
        self.mainController.getTrendingPeople()

    # Função para exibir o retorno das buscas
    def serverResponse(self, responseString):
        self.labelResponseString.set(responseString)
        self.labelResponse.configure(fg="#329C28")

