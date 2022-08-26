from cgitb import text
import code
from faulthandler import disable
from inspect import Traceback
from re import X
import tkinter
import csv
import os
from tkinter import BOTTOM, HORIZONTAL, LEFT, RIGHT, VERTICAL, Y, Scrollbar, messagebox
from tkinter import ttk
from traceback import TracebackException
from typing import Literal
from xml.dom import NoModificationAllowedErr
from iteration_utilities import duplicates
from setuptools import Command


def principal():
#Configuraciones ventana principal
    ventana = tkinter.Tk()
    ventana.geometry("450x330")
    ventana.title("Practica1")
    ventana.resizable(False,False)

    def seleccionar():
        ventana.destroy()
        seleccionarArchivo()

    def gestionar():
        ventana.destroy()
        gestionarCursos()

    def conte():
        ventana.destroy()
        conteoCredito()

    #Configuraciones texto de pantalla de inicio
    curso = tkinter.Label(ventana, text="Nombre del curso: Lab. Lenguajes Formales y de Programación")
    nombre = tkinter.Label(ventana, text="Nombre del Estudiante: Mario Ernesto Marroquín Pérez")
    carnet=tkinter.Label(ventana, text="Carnet del Estudiante: 202110509")
    cargarArchivo=tkinter.Button(ventana,text="Cargar Archivos", command=seleccionar)
    gestionarCurso=tkinter.Button(ventana,text="Gestionar Cursos", command=gestionar)
    conteoCreditos=tkinter.Button(ventana,text="Conteo de Créditos", command=conte)
    salir =tkinter.Button(ventana,text="Salir",command=ventana.destroy)

    #Agregar para centrar: fill = tkinter.BOTH, expand=True
    #organizar los elementos pantalla principal

    curso.place(x=50, y=30)
    nombre.place(x=50, y=60)
    carnet.place(x=50, y=90)
    cargarArchivo.place(x=170, y=150)
    gestionarCurso.place(x=167, y=190)
    conteoCreditos.place(x=160, y=230)
    salir.place(x=195, y=270)

    #mantener la ventana funcionando
    ventana.mainloop()

#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def seleccionarArchivo():

    ventana = tkinter.Tk()
    ventana.geometry("400x150")
    ventana.title("Seleccionar Archivo")
    ventana.resizable(False,False)

    def volver():
        ventana.destroy()
        principal()
    
    def obtenerRuta():
        rutaArchivo=rutaTexto.get()
        return rutaArchivo
    
    reader = ""

    def imprimir():
        try:
            csv_file = open(f'{obtenerRuta()}','r')
            global reader
            reader = csv.reader(csv_file,delimiter=",")

            if obtencion() !=1:
                messagebox.showinfo(message="Carga completada!", title="Felicidades")
                csv_file.close()
                volver()
                
            if obtencion() ==1:
                messagebox.showwarning(message="EXISTEN CURSOS REPETIDOS DENTRO DEL ARCHIVO o YA SE HA CARGADO UN ARCHIVO", title="ADVERTENCIA")
                limpieza()     
                csv_file.close()     
                volver()

        except FileNotFoundError:
            messagebox.showerror(message="Error, ingrese una direccion adecuada", title="ERROR")
        except OSError:
            messagebox.showerror(message="Error, ingrese una direccion adecuada", title="ERROR")


    regresar = tkinter.Button(ventana,text="Regresar",command=volver)
    seleccionar =tkinter.Button(ventana,text="Seleccionar", command=imprimir)
    rutaTexto=tkinter.Entry(ventana)
    textoRuta=tkinter.Label(ventana, text="Ruta:")

    regresar.place(x=325, y=100)
    seleccionar.place(x=150,y=100)
    rutaTexto.place(x=85, y=50,width=255)
    textoRuta.place(x=50,y=50)

    ventana.mainloop()
#--------------------------------------------------------------------------


cursos=[]
codigosIngre=[]
nombresIngre=[]


def obtencion():
    try:
            global cursos
            global codigosIngre
            global nombresIngre
            for columnas in reader:
                if not columnas:
                    continue
                codigo = columnas [0]
                nombre = columnas [1]  
                preRequisito=columnas [2]
                semestre=int(columnas [3])
                opcionalidad=int(columnas [4])
                creditos=int(columnas[5])
                estados=int(columnas [6])
                # nombresIngre.clear()
                # codigosIngre.clear()
                cursos.append({
                    "co":codigo, 
                    "nom":nombre, 
                    "pre":preRequisito, 
                    "sem":semestre, 
                    "op":opcionalidad,
                    "cred":creditos, 
                    "es":estados,
                })
                nombresIngre.append({
                    "nomb":nombre,
                })
                codigosIngre.append({
                    "codi": codigo,
                })
            for cur in cursos:
                while (cursos.count(cur)>1):
                    cursos.remove(cur)
            duplicados = list(duplicates(nombresIngre))
            duplicados1 = list(duplicates(codigosIngre))
            duplicados.clear()
            duplicados1.clear()
            if len(duplicados)>0 or len(duplicados1)>0:
                cursos.clear()
                return 1
            else:
                return cursos
    except ValueError:
            messagebox.showerror(message="POR FAVOR NO MEZCLAR LOS APARTADOS NUMERICOS CON LETRAS, verifique el archivo, Se HAN CARGADO LOS CURSOS SIN PROBLEMAS", title="ERROR")
            return 1
    # except IndexError:
    #     return cursos        
    
def limpieza():
    nombresIngre.clear()
    codigosIngre.clear()


class Cursos():

    def __init__(self, cod, nom, pre, sem, op, cred, es):
        self.__codigo = cod
        self.__nombre = nom
        self.__preRequi = pre
        self.__semestre = sem
        self.__opcion = op
        self.__creditos = cred
        self.__estado = es

    
    #getters (método get)
    def get_codigo(self):
        return self.__codigo

    def get_nombre(self):
        return self.__nombre

    def get_preRequisito(self):
        return self.__preRequi

    def get_semestre(self):
        return self.__semestre

    def get_opcion(self):
        return self.__opcion

    def get_creditos(self):
        return self.__creditos

    def get_estados(self):
        return self.__estado



#--------------------------------------------------------------------------
def gestionarCursos():

    ventana = tkinter.Tk()
    ventana.geometry("400x260")
    ventana.title("Gestionar Cursos")
    ventana.resizable(False,False)

    def volver():
        ventana.destroy()
        principal()

    def listarC():
        ventana.destroy()
        listar()

    def agregarC():
        ventana.destroy()
        agregar()
    
    def editarC():
        ventana.destroy()
        editar()

    def eliminarC():
        ventana.destroy()
        eliminar()

    def mostrarEspecificoC():
        ventana.destroy()
        mostrarEspecifico()

    regresar =tkinter.Button(ventana,text="Regresar",command=volver)
    listarCurso =tkinter.Button(ventana,text="Listar Cursos", command=listarC)
    mostrarEspe=tkinter.Button(ventana,text="Mostrar Curso Especifico", command=mostrarEspecificoC)
    agregarCurso =tkinter.Button(ventana,text="Agregar Curso", command = agregarC)
    editarCurso =tkinter.Button(ventana,text="Editar Curso", command = editarC)
    eliminarCurso =tkinter.Button(ventana,text="Eliminar Curso",command=eliminarC)


    listarCurso.place(x=157,y=20)
    mostrarEspe.place(x=127,y=60)
    agregarCurso.place(x=153,y=100)
    editarCurso.place(x=161,y=140)
    eliminarCurso.place(x=153,y=180)
    regresar.place(x=170, y=220)

    ventana.mainloop()


#-  -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   

def listar():
    ventana = tkinter.Tk()
    ventana.geometry("800x280")
    ventana.title("Listar Cursos")
    ventana.resizable(False,False)

    def volver():
        ventana.destroy()
        gestionarCursos()


    #aqui va la tabla

    regresar =tkinter.Button(ventana,text="Regresar",command=volver)
    scrollbarx = Scrollbar(ventana, orient=HORIZONTAL)
    scrollbary = Scrollbar(ventana, orient=VERTICAL)
    tabla = ttk.Treeview(ventana, columns=("#1","#2","#3","#4","#5","#6"))
    #, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    #scrollbary.config(command=tabla.yview)
    #scrollbary.pack(side=RIGHT, fill=Y)
    #scrollbarx.config(command=tabla.xview)
    #scrollbarx.pack(side=BOTTOM, fill=X)    
    #grid(row=0,column=15,columnspan=7)


    tabla.column("#0",width=50)
    tabla.column("#1",width=200)
    tabla.column("#2",width=150)
    tabla.column("#3",width=80)
    tabla.column("#4",width=80)
    tabla.column("#5",width=80)
    tabla.column("#6",width=80)


    tabla.heading("#0",text="Código")
    tabla.heading("#1",text="Nombre")
    tabla.heading("#2",text="Pre requisito")
    tabla.heading("#3",text="Opcionalidad")
    tabla.heading("#4",text="Semestre")
    tabla.heading("#5",text="Créditos")
    tabla.heading("#6",text="Estado")

    tabla.pack()
    regresar.pack()
    #place(x=380, y=290)
    #tabla.place(x=0,y=0)

    curso = cursos
    for alumno in curso:
            co = alumno["co"]
            nom = alumno["nom"]
            pre = alumno["pre"]
            sem = alumno["sem"]
            op =alumno["op"]
            cr=alumno["cred"]
            es=alumno["es"]
            tabla.insert("",0,text=(co),values=(nom, pre, sem, op, cr, es))
            #,alumno["nom"], alumno["pre"],alumno["sem"],alumno["op"],alumno["cred"],alumno["es"])



    ventana.mainloop()


#-  -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   

def mostrarEspecifico():
    ventana = tkinter.Tk()
    ventana.geometry("400x150")
    ventana.title("Mostrar Curso")
    ventana.resizable(False,False)

    def volver():
        ventana.destroy()
        gestionarCursos()
        
    #Agregar funcion de validacion que exista el codigo del curso para eliminar

    def obtenerCodigo():
        mostrar = rutaCodigo.get()
        for alumno in cursos:
            if alumno["co"] == mostrar:
                ventana.destroy()
                mostrarEspecifico1(mostrar)
                break
        messagebox.showerror(message="Este curso NO existe", title="ERROR")


    regresar =tkinter.Button(ventana,text="Regresar",command=volver)
    mostrar =tkinter.Button(ventana,text="Mostrar", command=obtenerCodigo)
    rutaCodigo=tkinter.Entry(ventana)
    textoCodigo=tkinter.Label(ventana, text="Código del Curso:")

    regresar.place(x=325, y=100)
    mostrar.place(x=150,y=100)
    rutaCodigo.place(x=160, y=50,width=180)
    textoCodigo.place(x=50,y=50)

    ventana.mainloop()



def mostrarEspecifico1(nombreCurso):
    ventana = tkinter.Tk()
    ventana.geometry("450x330")
    ventana.title("Agregar Curso")
    ventana.resizable(False,False)

    def volver():
        ventana.destroy()
        gestionarCursos()


    #Agregar funcion que muestre que se agregó correctamente el curso

    for alumno in cursos:
        if alumno["co"] == nombreCurso:
            co = alumno["co"]
            nom = alumno["nom"]
            pre = alumno["pre"]
            sem = alumno["op"]
            op =alumno["sem"]
            cr=alumno["cred"]
            es=alumno["es"]
            break

    textoCodigo=tkinter.Label(ventana, text="Código:")
    rutaCodigo=tkinter.Label(ventana,text=co)
    textoNombre=tkinter.Label(ventana, text="Nombre:")
    rutaNombre=tkinter.Label(ventana,text=nom)
    textoPreRequisito=tkinter.Label(ventana, text="Pre Requisito:")
    rutaPreRequisito=tkinter.Label(ventana,text=pre)
    textoSemestre=tkinter.Label(ventana, text="Semestre:")
    rutaSemestre=tkinter.Label(ventana,text=sem)
    textoOpcionalidad=tkinter.Label(ventana, text="Opcionalidad:")
    rutaOpcionalidad=tkinter.Label(ventana,text=op)
    textoCreditos=tkinter.Label(ventana, text="Créditos:")
    rutaCreditos=tkinter.Label(ventana,text=cr)
    textoEstado=tkinter.Label(ventana, text="Estado:")
    rutaEstado=tkinter.Label(ventana, text=es)

    regresar =tkinter.Button(ventana,text="Regresar",command=volver)
  
    textoCodigo.place(x=30, y=10)
    rutaCodigo.place(x=150, y=10,width=255)
    textoNombre.place(x=30, y=50)
    rutaNombre.place(x=150, y=50,width=255)
    textoPreRequisito.place(x=30, y=90)
    rutaPreRequisito.place(x=150, y=90,width=255)
    textoSemestre.place(x=30, y=130)
    rutaSemestre.place(x=150, y=130,width=255)
    textoOpcionalidad.place(x=30, y=170)
    rutaOpcionalidad.place(x=150, y=170,width=255)
    textoCreditos.place(x=30, y=210)
    rutaCreditos.place(x=150, y=210,width=255)
    textoEstado.place(x=30, y=250)
    rutaEstado.place(x=150, y=250,width=255)

    regresar.place(x=185, y=290)

    ventana.mainloop()

#----------------------------------------------------------------------------

def agregar():

    ventana = tkinter.Tk()
    ventana.geometry("450x330")
    ventana.title("Agregar Curso")
    ventana.resizable(False,False)

    def volver():
        ventana.destroy()
        gestionarCursos()


    #Agregar funcion que muestre que se agregó correctamente el curso
    def agregacion():
        try:
            curso = rutaCodigo.get()
            nombre = rutaNombre.get()
            preRequisito = rutaPreRequisito.get()
            semestre = int (rutaSemestre.get())
            opcion = int(rutaOpcionalidad.get())
            creditos = int(rutaCreditos.get())
            estado = int(rutaEstado.get())
            a=0
            if (semestre >= 1 and semestre <=10):
                if (opcion==1 or opcion==0):
                    if(estado == -1 or estado == 0 or estado ==1):
                        # nombresIngre.append({
                        #             "nomb":nombre,
                        #         })
                        # codigosIngre.append({
                        #             "codi": curso,
                        #         })
                        # duplicados = list(duplicates(nombresIngre))
                        # duplicados1 = list(duplicates(codigosIngre))
                        for repetido in cursos:
                            if repetido["co"] == curso or repetido["nom"] == nombre:
                                messagebox.showwarning(message="ESTE CURSO YA EXISTE, vaya al apartado de edición", title="Ya existe!")
                                a=1
                                break

                        # if len(duplicados)>0 or len(duplicados1)>0:
                        #     duplicados.clear()
                        #     duplicados1.clear()
                        #     messagebox.showwarning(message="ESTE CURSO YA EXISTE, vaya al apartado de edición", title="Ya existe!")
                        if a!=1:

                        # else:
                            cursos.append({
                                        "co":curso, 
                                        "nom":nombre, 
                                        "pre":preRequisito, 
                                        "sem":opcion, 
                                        "op":semestre,
                                        "cred":creditos, 
                                        "es":estado,
                                    })
                            messagebox.showinfo(message="Curso Agregado!", title="Felicidades")

                            volver()
                    else: 
                        messagebox.showerror(message="INGRESE LOS DATOS CORRECTOS en el apartado de ESTADO", title="ERROR")
                else:
                    messagebox.showerror(message="INGRESE LOS DATOS CORRECTOS en el apartado de OPCIONALIDAD", title="ERROR")
            else:
                messagebox.showerror(message="INGRESE LOS DATOS CORRECTOS en el apartado de SEMESTRE", title="ERROR")

        except ValueError:
            messagebox.showerror(message="POR FAVOR NO MEZCLAR LOS APARTADOS NUMERICOS CON LETRAS", title="ERROR")


    textoCodigo=tkinter.Label(ventana, text="Código:")
    rutaCodigo=tkinter.Entry(ventana)
    textoNombre=tkinter.Label(ventana, text="Nombre:")
    rutaNombre=tkinter.Entry(ventana)
    textoPreRequisito=tkinter.Label(ventana, text="Pre Requisito:")
    rutaPreRequisito=tkinter.Entry(ventana)
    textoSemestre=tkinter.Label(ventana, text="Semestre:")
    rutaSemestre=tkinter.Entry(ventana)
    textoOpcionalidad=tkinter.Label(ventana, text="Opcionalidad:")
    rutaOpcionalidad=tkinter.Entry(ventana)
    textoCreditos=tkinter.Label(ventana, text="Créditos:")
    rutaCreditos=tkinter.Entry(ventana)
    textoEstado=tkinter.Label(ventana, text="Estado:")
    rutaEstado=tkinter.Entry(ventana)

    regresar =tkinter.Button(ventana,text="Regresar",command=volver)
    aceptar = tkinter.Button(ventana,text="Agregar", command=agregacion)


    textoCodigo.place(x=30, y=10)
    rutaCodigo.place(x=150, y=10,width=255)
    textoNombre.place(x=30, y=50)
    rutaNombre.place(x=150, y=50,width=255)
    textoPreRequisito.place(x=30, y=90)
    rutaPreRequisito.place(x=150, y=90,width=255)
    textoSemestre.place(x=30, y=130)
    rutaSemestre.place(x=150, y=130,width=255)
    textoOpcionalidad.place(x=30, y=170)
    rutaOpcionalidad.place(x=150, y=170,width=255)
    textoCreditos.place(x=30, y=210)
    rutaCreditos.place(x=150, y=210,width=255)
    textoEstado.place(x=30, y=250)
    rutaEstado.place(x=150, y=250,width=255)

    aceptar.place(x=190,y=290)
    regresar.place(x=350, y=290)

    ventana.mainloop()


#-  -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   

def editar():

    ventana = tkinter.Tk()
    ventana.geometry("450x330")
    ventana.title("Editar Curso")
    ventana.resizable(False,False)

    def volver():
        ventana.destroy()
        gestionarCursos()

    def editar():
        try:
            curso = rutaCodigo.get()
            nombre = rutaNombre.get()
            preRequisito = rutaPreRequisito.get()
            semestre = int (rutaSemestre.get())
            opcion = int(rutaOpcionalidad.get())
            creditos = int(rutaCreditos.get())
            estado = int(rutaEstado.get())

            if (semestre >= 1 and semestre <=10):
                if (opcion==1 or opcion==0):
                    if(estado == -1 or estado == 0 or estado ==1):
                        for nom in cursos:
                            if nom["co"] == curso:
                                nom["nom"]=nombre
                                nom["pre"]=preRequisito
                                nom["sem"]=opcion
                                nom["op"]=semestre
                                nom["cred"]=creditos
                                nom["es"]=estado
                                messagebox.showinfo(message="Se ha actualizado el curso", title="Felicidades!")
                                volver()
                                break
                        messagebox.showerror(message="Este curso NO existe", title="ERROR")
                    else: 
                        messagebox.showerror(message="INGRESE LOS DATOS CORRECTOS en el apartado de ESTADO", title="ERROR")
                else:
                    messagebox.showerror(message="INGRESE LOS DATOS CORRECTOS en el apartado de OPCIONALIDAD", title="ERROR")
            else:
                messagebox.showerror(message="INGRESE LOS DATOS CORRECTOS en el apartado de SEMESTRE", title="ERROR")

        except ValueError:
            messagebox.showerror(message="POR FAVOR NO MEZCLAR LOS APARTADOS NUMERICOS CON LETRAS", title="ERROR")
    
    #Agregar funcion que muestre que se editó correctamente el curso
    #Agregar funcion de validacion que exista el codigo del curso para editar

    textoCodigo=tkinter.Label(ventana, text="Código:")
    rutaCodigo=tkinter.Entry(ventana)
    textoNombre=tkinter.Label(ventana, text="Nombre:")
    rutaNombre=tkinter.Entry(ventana)
    textoPreRequisito=tkinter.Label(ventana, text="Pre Requisito:")
    rutaPreRequisito=tkinter.Entry(ventana)
    textoSemestre=tkinter.Label(ventana, text="Semestre:")
    rutaSemestre=tkinter.Entry(ventana)
    textoOpcionalidad=tkinter.Label(ventana, text="Opcionalidad:")
    rutaOpcionalidad=tkinter.Entry(ventana)
    textoCreditos=tkinter.Label(ventana, text="Créditos:")
    rutaCreditos=tkinter.Entry(ventana)
    textoEstado=tkinter.Label(ventana, text="Estado:")
    rutaEstado=tkinter.Entry(ventana)

    regresar =tkinter.Button(ventana,text="Regresar",command=volver)
    aceptar = tkinter.Button(ventana,text="Editar", command=editar)

    textoCodigo.place(x=30, y=10)
    rutaCodigo.place(x=150, y=10,width=255)
    textoNombre.place(x=30, y=50)
    rutaNombre.place(x=150, y=50,width=255)
    textoPreRequisito.place(x=30, y=90)
    rutaPreRequisito.place(x=150, y=90,width=255)
    textoSemestre.place(x=30, y=130)
    rutaSemestre.place(x=150, y=130,width=255)
    textoOpcionalidad.place(x=30, y=170)
    rutaOpcionalidad.place(x=150, y=170,width=255)
    textoCreditos.place(x=30, y=210)
    rutaCreditos.place(x=150, y=210,width=255)
    textoEstado.place(x=30, y=250)
    rutaEstado.place(x=150, y=250,width=255)

    aceptar.place(x=190,y=290)
    regresar.place(x=350, y=290)


    ventana.mainloop()

#-  -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   

def eliminar():

    ventana = tkinter.Tk()
    ventana.geometry("400x150")
    ventana.title("Eliminar Curso")
    ventana.resizable(False,False)

    def volver():
        ventana.destroy()
        gestionarCursos()
        
    def elimir():
        elim = rutaCodigo.get()
        i=0
        for nom in cursos:
            i=i+1
            if nom["co"] == elim:
                cursos.pop(i-1)
                messagebox.showinfo(message="Se ha eliminado el curso", title="Felicidades!")
                volver()
                break
        messagebox.showerror(message="Este curso NO existe", title="ERROR")


    #Agregar funcion de validacion que exista el codigo del curso para eliminar

    regresar =tkinter.Button(ventana,text="Regresar",command=volver)
    eliminar =tkinter.Button(ventana,text="Eliminar",command = elimir)
    rutaCodigo=tkinter.Entry(ventana)
    textoCodigo=tkinter.Label(ventana, text="Código del Curso:")

    regresar.place(x=325, y=100)
    eliminar.place(x=150,y=100)
    rutaCodigo.place(x=160, y=50,width=180)
    textoCodigo.place(x=50,y=50)

    ventana.mainloop()

#--------------------------------------------------------------------------



#-------------------------------------------------------------------------

def conteoCredito():

    ventana = tkinter.Tk()
    ventana.geometry("450x330")
    ventana.title("Conteo de Créditos")
    ventana.resizable(False,False)

    def volver():
        ventana.destroy()
        principal()

    def sumarAprobados():
        sumatoria = 0
        for suma in cursos:
            if suma["es"] == 0:
                sumatoria += suma["cred"]
        return sumatoria
    
    def sumarCursando():
        sumatoria = 0
        for suma in cursos:
            if suma["es"] == 1:
                sumatoria += suma["cred"]
        return sumatoria

    def sumarPendientes():
        sumatoria = 0
        for suma in cursos:
            if suma["es"] == -1:
                if suma["sem"] == 1:
                    sumatoria += suma["cred"]
                    #print(suma["co"])
        return sumatoria
    
    def creditosHasta():
        sumatoria =0
        semestre1 = int(combo.get())
        for suma in cursos:
                    semestres = int(suma["op"])
                    if semestres <= semestre1:
                        if suma["sem"] == 1:
                            sumatoria += suma["cred"]
                            #print(suma["co"])
                      #print(sumatoria)
        numeroTotalCreditos.config(text=sumatoria)
        return sumatoria
    
    def mostrarCreditosHasta():
        aprovados=0
        cursando =0
        pendientes=0
        semestre1 = int(combo1.get())
        for suma in cursos:
            semestres = int (suma["op"])
            if semestres <= semestre1:
                if suma["es"] == 0:
                    aprovados += suma["cred"]
                if suma["es"]== 1:
                    cursando += suma["cred"]
                if suma ["es"]==-1:
                    pendientes += suma["cred"]
        numeroTotalCreditos1.config(text = aprovados)
        numeroTotalCreditos2.config(text=cursando)
        numeroTotalCreditos3.config(text=pendientes)

    cantidadAprobados = tkinter.Label(ventana, text="Cursos Aprobados:")
    numeroAprovados=tkinter.Label(ventana, text=sumarAprobados())
    creditosCursando = tkinter.Label(ventana, text="Créditos Cursando:")
    numeroCursando=tkinter.Label(ventana, text=sumarCursando())
    creditosPendientes = tkinter.Label(ventana, text="Créditos Pendientes:")
    numeroPendientes=tkinter.Label(ventana, text=sumarPendientes())
    creditosObligatorioSemestre= tkinter.Label(ventana, text="Créditos Obligaratorios hasta semestre N:")#agregar
    combo = ttk.Combobox(state="readonly",values=[int(1),int(2),int(3),int(4),int(5),int(6),int(7),int(8),int(9),int(10)],width=3)
    totalCreditos = tkinter.Label(ventana, text="Total Créditos:")
    numeroTotalCreditos=tkinter.Label(ventana, text="")
    semestreNum1 = tkinter.Label(ventana, text="Semestre:")#agregar
    creditoSemestre = tkinter.Label(ventana, text="Créditos del semestre:")#agregar
    #semestreNum2 = tkinter.Label(ventana, text="Semestre:")#agregar 
    totalCreditos1 = tkinter.Label(ventana, text="Aprobados:")
    totalCreditos2 = tkinter.Label(ventana, text="Cursando:")
    totalCreditos3 = tkinter.Label(ventana, text="Pendientes:")
    combo1 = ttk.Combobox(state="readonly",values=[int(1),int(2),int(3),int(4),int(5),int(6),int(7),int(8),int(9),int(10)],width=3)
    numeroTotalCreditos1=tkinter.Label(ventana, text="")
    numeroTotalCreditos2=tkinter.Label(ventana, text="")
    numeroTotalCreditos3=tkinter.Label(ventana, text="")
    regresar =tkinter.Button(ventana,text="Regresar",command=volver)
    contar1=tkinter.Button(ventana,text="Contar", command=creditosHasta)#Agregar funcion
    contar2=tkinter.Button(ventana,text="Contar", command=mostrarCreditosHasta)#Agregar funcion




    cantidadAprobados.place(x=50,y=20)
    numeroAprovados.place(x=165,y=20)
    creditosCursando.place(x=50,y=60)
    numeroCursando.place(x=165,y=60)
    creditosPendientes.place(x=50,y=100)
    numeroPendientes.place(x=165,y=100)
    creditosObligatorioSemestre.place(x=50,y=140)
    semestreNum1.place(x=100,y=170)
    combo.place(x=170,y=170)
    contar1.place(x=220,y=170)
    totalCreditos.place(x=280, y=170)
    numeroTotalCreditos.place(x=360, y=170)
    creditoSemestre.place(x=50,y=220)
    combo1.place(x=170,y=220)
    contar2.place(x=220,y=220)
    totalCreditos1.place(x=70, y=260)
    totalCreditos2.place(x=190, y=260)
    totalCreditos3.place(x=310, y=260)
    numeroTotalCreditos1.place(x=135, y=260)
    numeroTotalCreditos2.place(x=250, y=260)
    numeroTotalCreditos3.place(x=378, y=260)
    regresar.place(x=370,y=290)
    
    
    ventana.mainloop()
#-----------------------------------------------------------------------


if __name__ == '__main__':
    principal()
