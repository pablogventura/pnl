PLN 2015: Procesamiento de Lenguaje Natural 2015
================================================

Este práctico se focalizó principalmente en el Modelado de Lenguaje.

Ejercicio 1: CORPUS
===================

Este ejercicio consistió simplemente en elegir un corpus (conjunto de sentencias de algún lenguaje natural)
para crear los modelos de lenguaje.

Para los ejercicios se optó por un corpus de las obras del dramaturgo William Shakespeare.

Ejercicio 2: MODELOS DE N-GRAMAS
================================

Como una primera aproximación al modelado de lenguaje, se implementó un modelo básico: el modelo de ngramas.

Es un modelo relativamente simple que se basa en las ocurrencias relativas de ngramas.

Ejercicio 3: GENERACIÓN DE SENTENCIAS
=====================================

Dado un modelo entrenado de ngramas, podemos generar sentencias basándonos en las las probabilidades de que
se genere una palabra, dadas las n-1 palabras anteriores. Los siguientes son ejemplos de sentencias generadas
con modelos de unigramas, bigramas, trigramas y cuatrigramas:

unigrama:
---------

s the For you it .

carried ? me my I sent to , me of an O chain d year with , charge may of ' ' ' shall shall were conduct .

embrace He ? ' How time to But within And .

am you s Would .

' the with madam an , will Lord .

bigrama:
--------
Be packing with the capacity Is it ; There ' s ambition , marry ; as you knew him . 

Nothing in every loyal servant to the promis ' s a tall , kill ' d that I think , sir . 

There ' s de - temper ' t like a beast . 

If they are you ; Give me . 

I ' s ended , At hand , And not the like , and of thy hands : how our mind . 

trigrama:
---------
Fear me not your own desire . 

That ' s death . 

I am undone , captain . 

No ; you have a living prince Does now speak Sir John . 

The good old Abraham , Lords appellants , Your highness ' pleasure . 


cuatrigrama:
------------
Fear not , ' tis his right : bawd is he , Biondello ! 

You have been factious one against the other : what we chang ' d . 

Here ' s my lord your son , As you have ever been my father ' s dead . 

With him , the hour is come To do you justice , make their sire Stoop with oppression of their prodigal weight : Give some supportance to the bending twigs . 

Prepare my horses . 

Podemos apreciar, que a medida que aumenta el valor n, la coherencia de las sentencias, aumenta.

Ejercicio 4: SUAVIZADO ADD-ONE
==============================

Heurística del modelo de ngramas. Se utiliza el algoritmo de Laplace para suavizar datos categóricos.


Ejercicio 5: EVALUACIÓN DE MODELOS DE LENGUAJE
==============================================
