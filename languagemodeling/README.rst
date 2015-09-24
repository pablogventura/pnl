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

En este punto, evaluamos los modelos de lenguaje para ver cuán buenos nuestros modelos son prediciendo muestras.

Más información: https://en.wikipedia.org/wiki/Perplexity

Podemos observar los siguientes resultados:
(cada fila indica un valor de n, empezando por 1, siendo n el orden del modelo de ngrama)


Modelo Addone:
--------------
833.015
1975.822
13570.088 
241318.215
                            

Modelo Intepolated:
-------------------
834.657
352.036
331.694
328.333


Modelo Backoff:
---------------
834.657
273.227
254.692
261.081


Como podemos observar, el modelo con mejor perplexity (mientras menor, mejor),
es el modelo de Backoff.


Ejercicio 6: SUAVIZADO POR INTERPOLACIÓN
========================================

Este modelo de ngramas, se basa en las aproximación de un parámetro q(w_n|w_1,...,w_(n-1))
usando los parámatros de "Maximum Likelihood", o sea, parámetros de NGramas (y, de ser indicado,
modelos de AddOne para los unigramas) de unigramas, bigramas, hasta n-gramas; dándole un peso
a cada uno de estos parámetros con factores lambda_1, ..., lambda_n; tales que lambda_i > 0 y
la suma de estos lambda_i sea igual a 1.

Estos parámetros pueden ser calculados en base a un valor gamma, que es un parámetro del modelo.
Si tal gamma no se provee, el modelo mismo se encarga de estimarlo.
Los valores obtenidos de perplexity referidos en el ejercicio 5, se obtuvieron estimando un gamma
óptimo para cada modelo de orden n.


Ejercicio 7: SUAVIZADO POR BACKOFF CON DISCOUNTING
==================================================

Es un modelo muy usado en práctica. La motivación es no sobrestimar tanto los ngramas que se ven en el
corpus de entrenamiento.
El parámetro de descuento, beta, puede ser previsto, o bien, ajustado por el modelo para elegir el que
muestre mejores resultados de perplexity.
En los valores reflejados en el ejercicio 5, ningún beta fue dado como parámetro, en cada orden n se calculó
el beta que mejor ajuste a los datos.



--------------------------------------------------------------


Notas: se proveen dos scripts adicionales: el script "train_models.sh" entrena modelos de los cuatro modelos
descriptos arriba, de orden 1, 2, 3 y 4 (en los casos de interpolated y backoff, se estiman los parámetros gamma y beta automáticamente dentro de cada modelo, elegiendo el que mejor se ajuste en cada caso). Y el script "eval_models.sh" calcula la perplexity de los modelos
entrenados con "train_models.sh".
