from clases import *
from tkinter import *
from PIL import Image, ImageTk
from time import sleep
import re
from tkinter import messagebox as mb
import pyttsx3


#import speech_recognition as sr
class Window():
    def __init__(self):
        self.__root = Tk()
        self.__word = StringVar()
        self.config()
        self.initwidgets()
        self.__root.mainloop()

    def config(self):
        self.__root.title('ADPND')
        self.__root.resizable(0, 0)
        self.__root.geometry('660x400')
        self.__root.config(bg='#1ed455')
        self.__root.iconbitmap('img\line-chart.ico')

        # Expresion regular
        self.__patron = re.compile('[a-b]*c[a-b]*$')
    #    self.__patron = re.compile('(([a]{3})*([a]{2}[b])*([b])*)*$')

        # Voz
        self.__engine = pyttsx3.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__engine.setProperty('voice', self.__voices[0].id)

        # Escuchar
        self.__isListening = False
        #self.__r = sr.Recognizer()

    def initwidgets(self):
        # Entry donde va la palabra
        self.entry = Entry(self.__root, width=25, textvariable=self.__word)
        self.entry.place(x=120, y=280)

        # Imagen del autómata
        image = Image.open("img\einitial.PNG")
        photo = ImageTk.PhotoImage(image)
        self.label = Label(self.__root, image=photo)
        self.label.image = photo
        self.label.place(x=120, y=10)

        # Botón lento
        self.slow = Button(self.__root, bg='#7cbbc4', text='Lento', command=lambda: self.start(3))
        self.slow.place(x=300, y=280)

        # Botón rápido
        self.fast = Button(self.__root, bg='#7cbbc4', text='Rápido', command=lambda: self.start(0.5))
        self.fast.place(x=350, y=280)

        # Imagen de la pila
        image = Image.open("img\pile#.png")
        photo = ImageTk.PhotoImage(image)
        self.labelpile = Label(self.__root, image=photo)
        self.labelpile.image = photo
        self.labelpile.place(x=20, y=330)

        # Botón reiniciar
        self.reiniciar = Button(self.__root, bg='#7cbbc4', text='Reiniciar', command=self.clearall)
        self.reiniciar.place(x=420, y=280)

        # Botón escuchar

        self.listen = Button(self.__root, text='Escuchar',command=self.listening)
        self.listen.place(x=226, y=500)

    # Botón de ayuda
        self.help = Button(self.__root, text='Ayuda', command=self.showhelp)
        self.help.place(x=10,y=10)

    # Comienza el programa
    def start(self, deelay, mensaje2=None, mensaje3=None, mensaje1=None):
        if (re.findall(self.__patron, self.__word.get())):
            self.automaton = Automaton(str(self.__word.get()))
            self.configautomaton()
            self.automaton.start()
            self.__word.set('')

            # Inicializa la lista de imagenes de la pila
            self.piley = 330
            self.pileelements = []
            self.pilex = 20
            # Inicializa la lista de transiciones usadas, para posteriormente darles formato de nombre de imagen
            self.graphicstransitions = self.automaton.getusedtransitions()
            self.formatgraphicstransitions()
            ctransition = self.getctransition()

            for t in self.graphicstransitions:
                self.setactualchar(t[0])
                image = Image.open("img\{}".format(t))
                photo = ImageTk.PhotoImage(image)
                self.label.config(image=photo)
                self.label.image = photo
                if (self.graphicstransitions.index(t) < self.graphicstransitions.index(ctransition)):
                    self.insertpile(t[0])
                    self.label.update()
                elif (self.graphicstransitions.index(t) > self.graphicstransitions.index(
                        ctransition) and self.graphicstransitions.index(t) < len(self.graphicstransitions) - 1):
                    self.removepile()
                    self.label.update()
                else:
                    self.label.update()
                sleep(deelay)

            if (self.automaton.getresult()):
                self.__engine.say('¡Correcto, es un palíndromo!')
                self.__engine.runAndWait()
                font = ("arial Bold", 19)
                mensaje1 = Label(self.__root, text="Es un palindromo")
                mensaje1.pack()
                mensaje1.place(x=230, y=320)

                mb.showinfo("¡Correcto!","Es un palíndromo")
            else:
                self.__engine.say('¡Error, No es un palíndromo!')
                self.__engine.runAndWait()

                mensaje2 = Label(self.__root, text="No es palindromo")
                mensaje2.pack()
                mensaje2.place(x=230, y=320)
                mb.showerror("¡Error!","No es un palíndromo")
        else:
            self.__engine.say('¡Error! Expresión inválida')
            self.__engine.runAndWait()
            mensaje3 = Label(self.__root, text="Expresion invalida")
            mensaje3.pack()
            mensaje3.place(x=230, y=320)
            mb.showerror("¡Error!", "Expresión inválida")

    # Configuración del automata
    def configautomaton(self):
        self.automaton.addstate('p', 'initial')

        self.automaton.addstate('q', 'normal')
        self.automaton.addstate('r', 'final')

        self.automaton.getstate('p').addtransition('p', 'a', '#', '#a')
        self.automaton.getstate('p').addtransition('p', 'b', '#', '#b')
        self.automaton.getstate('p').addtransition('p', 'a', 'a', 'aa')
        self.automaton.getstate('p').addtransition('p', 'b', 'a', 'ab')
        self.automaton.getstate('p').addtransition('p', 'a', 'b', 'ba')
        self.automaton.getstate('p').addtransition('p', 'b', 'b', 'bb')
        self.automaton.getstate('p').addtransition('q', 'c', 'a', 'a')
        self.automaton.getstate('p').addtransition('q', 'c', 'b', 'b')
        self.automaton.getstate('p').addtransition('q', 'c', '#', '#')
        self.automaton.getstate('p').showtransitions()

        self.automaton.getstate('q').addtransition('q', 'a', 'a', 'λ')
        self.automaton.getstate('q').addtransition('q', 'b', 'b', 'λ')
        self.automaton.getstate('q').addtransition('r', 'λ', '#', '#')
        self.automaton.getstate('q').showtransitions()

    # Convierte la lista de transiciones en una lista de nombres de las imágenes
    def formatgraphicstransitions(self):
        for i in range(len(self.graphicstransitions)):
            self.graphicstransitions[i] = self.graphicstransitions[i].getchar() + self.graphicstransitions[i].getout() + \
                                          self.graphicstransitions[i].getinto() + '.png'
            if (self.graphicstransitions[0] == 'c' and self.graphicstransitions[1] == '#'):
                self.graphicstransitions[i] = self.graphicstransitions[i].capitalize()

    def setactualchar(self, char):
        if (char != 'λ'):
            self.__word.set(self.__word.get() + char)

    def insertpile(self, char):
        image = Image.open("img\pile{}.png".format(char))
        photo = ImageTk.PhotoImage(image)
        self.pileelements.append(Label(self.__root, image=photo))
        self.pileelements[len(self.pileelements) - 1].image = photo
        self.piley -= 25
        self.pileelements[len(self.pileelements) - 1].place(x=20, y=self.piley)

    def removepile(self):
        self.pileelements.pop().destroy()

    def clearall(self):
        self.__word = StringVar()
        for e in self.pileelements:
            e.destroy()
            self.graphicstransitions = []
        self.initwidgets()

    def getctransition(self):
        for transition in self.graphicstransitions:
            if (transition[0] == 'c' or transition[0] == 'C'):
                return transition

    def listening(self):
        pass
        """   self.switch()
        if (self.__isListening):
            with sr.Microphone() as source:
                mb.showinfo("Escuchando..","Hable cerca al micrófono")
                audio = self.__r.listen(source)
            try:
                if (self.__r.recognize_google(audio) == 'slow' or self.__r.recognize_google(audio) == 'Slow' or self.__r.recognize_google(audio) == 'SLOW'):
                    self.start(3)
                elif (self.__r.recognize_google(audio) == 'fast' or self.__r.recognize_google(audio) == 'Fast' or self.__r.recognize_google(audio) == 'FAST'):
                    self.start(0.5)

                #mb.showinfo("¡Información!", "Usted dijo " +self.__r.recognize_google(audio))
            except sr.UnknownValueError:
                    mb.showerror("¡Error!","No se pudo entender lo que dijo")
            except sr.RequestError as e:
                    mb.showerror("¡Error!", "Could not request results from Google Speech Recognition service; {0}".format(e))

            self.__isListening=False"""

    def switch(self):
        if (self.__isListening):
            self.__isListening = False
        else:
            self.__isListening = True

    def showhelp(self):
        #mb.showinfo("Ayuda","Este programa está diseñado para validad un palíndromo impar con longitud n>1, que esté dentro del lenguaje=[a,b] y que además tenga un caracter 'c' en el centro.\n\nInstrucciones\nDeberá ingresar la expresión y clickear alguno de los botones(Lento, Rápido) a continuación se mostrará una animación con las transiciones, finalmente el programa le dirá si la expresión ingresada es correcta.\n\nEscuchar\nPara hacer uso de esta función deberá clickear el botón 'Escuchar' y seguidamente decir cerca al micrófono la palabra 'Slow' para lento o 'Fast' para rápido.")
        mb.showinfo("Ayuda","Este programa está diseñado para validad un palíndromo impar con longitud n>1, que esté dentro del lenguaje=[a,b] y que además tenga un caracter 'c' en el centro.\n\nInstrucciones\nDeberá ingresar la expresión y clickear alguno de los botones(Lento, Rápido) a continuación se mostrará una animación con las transiciones, finalmente el programa le dirá si la expresión ingresada es correcta.\n")

    def insertarhorizontal(self, char):
        image = Image.open("img\pile{}.png".format(char))
        photo = ImageTk.PhotoImage(image)
        self.pileelements.append(Label(self.__root, image=photo))
        self.pileelements[len(self.pileelements) - 1].image = photo
        self.pilex += 50
        self.pileelements[len(self.pileelements) - 1].place(x=self.pilex, y=330)


programa = Window()