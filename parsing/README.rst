================================================
PLN 2015: Procesamiento de Lenguaje Natural 2015
================================================

En este laboratorio se trabajó con el parseado de sentencias del leguanje natural.
Se implementó un modelo para parsear el árbol sintáctico de una sentencia y se
realizaron experimientos de precisión con el mismo.


EJERCICIO 1: Evaluación de Parsers
==================================

Se completó la implementación de un evaluador de parsers:

·Se agregaron las opciones de, a la hora de evaluar, elegir la cantidad de sentencias a evaluar y también elegir evaluar solo oraciones
de algún largo específico. Esto se logra con las opciones -n y -m respectivamente. Ejemplo: ::

  $ python scripts/eval.py -i generic_model -n 500 -m 20


EJERCICIO 2: Algoritmo CKY
==========================

Se implementó el algoritmo CKY para generar un árbol sintáctico de una sentencia. Dicho árbol es construido basándonos en una gramática
libre de contexto probabilística (que debe estar en forma normal de Chomsky), obtenida de las sentencias de entramiento del corpus usado.

También se creó un test para ver que frente a una sentencia amigua, se seleccionará el árbol de parseo más probable.
La sentencia por la que se optó para el test es "I rode an elephant in my pajamas", y sus posibles árboles de parseo son:

.. image:: https://github.com/giovannirescia/PLN-2015/blob/practico3/parsing/parse1.png?raw=true
   :height: 571 px
   :width: 918 px
   :scale: 45


.. image:: https://github.com/giovannirescia/PLN-2015/blob/practico3/parsing/parse2.png?raw=true
   :height: 582 px
   :width: 808 px
   :scale: 50


Como es esperado, con el algoritmo se conseguirá el primer árbol, ya que es el más probable.


EJERCICIO 3: UPCFG
==================

Basándonos en el corpus de entramiento, creamos una gramática libre de contexto con probabilidades asociadas a cada regla o producción.
Se usó la librería provista por la cátedra para deslexicalizar las producciones (se desxicaliza el árbol y se obtienen las producciones a partir del árbol deslexicalizado), y para volver a lexicalizar las producciones (el árbol final).

Una vez creada la UPCFG, se hizo uso del algoritmo CKY para parsear las sentencias y crear su estructura sintáctica.


EJERCICIO 4: Markovización Horizontal
=====================================

Se hicieron pequeños cambios en la UPCFG para poder usar Markovización horizontal (a la hora de poner en forma normal de Chomsky un conjunto de producciones).

También se modificó el script train.py para poder usar la nueva funcionalidad implementada.


RESULTADOS
==========

A continuación, los resultados de evaluar los modelos provistos por la cátedra (RBranch y Flat) y los implementados (UPCFG y LBranch):

(Nota: para evaluar se usaron 1444 sentencias, que son las sentencias del corpus de largo a lo sumo 20)


Flat model
----------


* Labeled

  * Precision: 99.93% 
  * Recall: 14.57% 
  * F1: 25.43% 

* Unlabeled

  * Precision: 100.00% 
  * Recall: 14.58% 
  * F1: 25.45% 

* time:

  - 6.61 user
  - 0.06 system
  - 0:06.69 elapsed


RBranch model
-------------

* Labeled

  * Precision: 8.81% 
  * Recall: 14.57% 
  * F1: 10.98% 

* Unlabeled

  * Precision: 8.87% 
  * Recall: 14.68% 
  * F1: 11.06% 

* time

  - 7.22 user
  - 0.07 system
  - 0:07.30 elapsed


LBranch model
-------------

* Labeled

  * Precision: 8.81% 
  * Recall: 14.57% 
  * F1: 10.98% 


* Unlabeled

  * Precision: 14.71% 
  * Recall: 24.33% 
  * F1: 18.33% 

* time

  - 7.19 user
  - 0.09 system
  - 0:07.30 elapsed


UPCFG models
------------

Without Horizontal Markovization
""""""""""""""""""""""""""""""""

* Labeled
  
  * Precision: 73.28% 
  * Recall: 72.98% 
  * F1: 73.13% 


* Unlabeled
  
  * Precision: 75.39% 
  * Recall: 75.08% 
  * F1: 75.24% 

* time

  - real 2m13.158s
  - user 2m12.865s
  - sys	0m0.216s

With Horizontal Markovization
"""""""""""""""""""""""""""""

n = 0
'''''

* Labeled 

  * Precision: 70.25%
  * Recall: 70.02%
  * F1: 70.14%

* Unlabeled

  * Precision: 72.11% 
  * Recall: 71.88% 
  * F1: 72.00% 

* time

  - 62.68 user
  - 0.15 system
  - 1:02.88 elapsed


n = 1
'''''

* Labeled

  * Precision: 74.62% 
  * Recall: 74.53% 
  * F1: 74.57% 

* Unlabeled

  * Precision: 76.48% 
  * Recall: 76.38% 
  * F1: 76.43% 

* time

  * 73.05 user
  * 0.09 system
  * 1:13.19 elapsed


n = 2
'''''

* Labeled

  * Precision: 74.87% 
  * Recall: 74.35% 
  * F1: 74.61% 

* Unlabeled
  
  * Precision: 76.79% 
  * Recall: 76.26% 
  * F1: 76.52% 

* time

  - 105.86 user
  - 0.09 system
  - 1:46.01 elapsed


n = 3
'''''

* Labeled

  * Precision: 74.10% 
  * Recall: 73.47% 
  * F1: 73.78% 

* Unlabeled

  * Precision: 76.26% 
  * Recall: 75.61% 
  * F1: 75.93% 

* time

  - 118.66 user
  - 0.25 system
  - 1:58.98 elapsed


n = 4
'''''

* Labeled

  * Precision: 73.51% 
  * Recall: 73.09% 
  * F1: 73.30% 

* Unlabeled

  * Precision: 75.66% 
  * Recall: 75.22% 
  * F1: 75.44% 

* time

  - 126.33 user
  - 0.16 system
  - 2:06.57 elapsed




CONCLUSIÓN
==========

Tal como lo indica James Martin en las videolecturas, los mejores resultados se observan usando Markovización Horizontal de orden 2.
Si bien, con las heurísiticas implementadas, no se observaron mejoras considerables, quizá usando un corpus más grande las diferencias
en la performance pueden mejorar considerablemente.



Nota
----

Se proveen dos scripts (train_models.sh y eval_models.sh) para entrenar los modelos y evaluarlos a todos directamente. (En el directorio 
donde se ejecuten, es necesario que haya una carpeta "models", ya que ahí se guardarán todos los modelos mientras se van entrando y se los tomará para evaluarlos luego).
