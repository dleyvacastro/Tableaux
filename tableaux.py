# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 19:32:44 2020

@author: dleyv
"""
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea los conectivos
conectivos = ['Y', 'O', '>', '-']
binarios = ['Y', 'O', '>', '<->']
negacion = ['-']
# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
    if (f.right == None):
        return f.label
    elif f.label == '-':
        return f.label + Inorder(f.right)
    else:
        return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def String2Tree(A):
	# Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
	# Input: - A, lista de caracteres con una formula escrita en notacion polaca inversa
	#        - letrasProposicionales, lista de letras proposicionales
	#        - conectivos, lista de conectivos
	# Output: formula como tree
	pila = []
	for c in A:
		# print("Examinando " + str(c))
		if c in letrasProposicionales:
			# print(u"El símbolo es letra proposicional")
			pila.append(Tree(c, None, None))
		elif c == '-':
			# print("Negamos")
			formulaAux = Tree(c, None, pila[-1])
			del pila[-1]
			pila.append(formulaAux)
		elif c in conectivos:
			# print("Unimos mediante conectivo")
			formulaAux = Tree(c, pila[-1], pila[-2])
			del pila[-1]
			del pila[-1]
			pila.append(formulaAux)
		else:
			print(u"Hay un problema: el símbolo " + str(c) + " no se reconoce")
	return pila[-1]

def Inorder2Tree(A):
	if len(A) == 1:
		return Tree(A[0], None, None)
	elif A[0] == '-':
		return Tree(A[0], None, Inorder2Tree(A[1:]))
	elif A[0] == "(":
		counter = 0 #Contador de parentesis
		for i in range(1, len(A)):
			if A[i] == "(":
				counter += 1
			elif A[i] == ")":
				counter -=1
			elif (A[i] in ['Y', 'O', '>', '=']) and (counter == 0):
				return Tree(A[i], Inorder2Tree(A[1:i]), Inorder2Tree(A[i + 1:-1]))
	else:
		return -1

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"

def imprime_listaHojas(L):
	for h in L:
		print(imprime_hoja(h))

def complemento(l):
	# Esta función devuelve el complemento de un literal
	# Input: l, un literal
	# Output: x, un literal
    if (l.label == '-'):
        return l.right
    else:
        return Tree('-',None,l)


def par_complementario(l):
	# Esta función determina si una lista de solo literales
	# contiene un par complementario
	# Input: l, una lista de literales
	# Output: True/False
    for i in l:
        indices = [x for x in l if x != i]
        for j in indices:
            if (Inorder(i) == Inorder(complemento(j))):
                return True
    return False


def es_literal(f):
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
    if f.label in binarios:
        return False
    elif f.label in negacion:
        f = f.right
        if f.label in negacion:
            return False
        return es_literal(f)
    else:
        return True


def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
    for i in l:
       if (es_literal(i) == False):
            return i
        
    return None

def clasificacion(f):
	# clasifica una fórmula como alfa o beta
	# Input: f, una fórmula como árbol
	# Output: string de la clasificación de la formula
    if f.label == '-':
        #alfa
        if f.right.label == '-':
            return '1alfa'
        elif f.right.label == 'O':
            return '3alfa'
        elif f.right.label == '>':
            return '4alfa'
        #beta
        elif f.right.label == 'Y' :
            return '1beta'
        else:
            return "Error en la clasificacion."
    elif f.label == 'Y':
        return '2alfa'
    elif f.label == 'O':
        return '2beta'
    elif f.label == '>':
        return '3beta'
    else:
        return "Error en la clasificacion."
        
def clasifica_y_extiende(f, h):
	# Extiende listaHojas de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# 		 h, una hoja (lista de fórmulas como árboles)
	# Output: no tiene output, pues modifica la variable global listaHojas

    global listaHojas
    
    print("Formula:", Inorder(f))
    print("Hoja:", imprime_hoja(h))

    assert(f in h), "La formula no esta en la lista!"
    
    clase = clasificacion(f)
    print("Clasificada como:", clase)
    assert(clase != None), "Formula incorrecta " + imprime_hoja(h)
    
    if clase == '1alfa':
        aux = [x for x in h if x != f] + [f.right.right]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif clase == '2alfa':
        aux = [x for x in h if x!=f] + [f.left, f.right]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif clase == '3alfa':
        aux = [x for x in h if x!=f] + [Tree('-', None, f.right.right), Tree('-', None, f.right.left)]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif clase == '4alfa':
        aux = [x for x in h if x!=f] + [f.right.left, Tree('-', None, f.right.right)]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif clase == '1beta':
        aux1 = [x for x in h if x!=f] + [Tree('-', None, f.right.right)]
        aux2 = [x for x in h if x!=f] + [Tree('-', None, f.right.left)]
        listaHojas.remove(h)
        listaHojas.append(aux1)
        listaHojas.append(aux2)
    elif clase == '2beta':
        aux1 = [x for x in h if x!=f] + [f.right]
        aux2 = [x for x in h if x!=f] + [f.left]
        listaHojas.remove(h)
        listaHojas.append(aux1)
        listaHojas.append(aux2)
    elif clase == '3beta':
        aux1 = [x for x in h if x!=f] + [f.right]
        aux2 = [x for x in h if x!=f] + [Tree('-', None, f.left)]
	# Aqui el resto de casos


def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f

	global listaHojas
	global listaInterpsVerdaderas

	A = String2Tree(f)
	print(u'La fórmula introducida es:\n', Inorder(A))

	listaHojas = [[A]]

	while (len(listaHojas) > 0):
		h = choice(listaHojas)
		print("Trabajando con hoja:\n", imprime_hoja(h))
		x = no_literales(h)
		if x == None:
			if par_complementario(h):
				listaHojas.remove(h)
			else:
				listaInterpsVerdaderas.append(h)
				listaHojas.remove(h)
		else:
			clasifica_y_extiende(x, h)

	return listaInterpsVerdaderas

sz = [Tree('-',None,Tree('p',None,None)),Tree('p',None,None),Tree('-',None,Tree('q',None,None)),Tree('q',None,None)]
 
print(no_literales(sz))
