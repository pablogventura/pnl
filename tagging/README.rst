================================================
PLN 2015: Procesamiento de Lenguaje Natural 2015
================================================

En este práctico se trabajó con el etiquetado de secuencias.
Se implementaron varios modelos de etiquetado y se realizaron algunos experimentos con ellos.


EJERCICIO 1: CORPUS ANCORA: Estadísticas de etiquetas POS (Part of speech)
==========================================================================

El ejercicio se basó en implementar un script (stats.py) que provea cierta
información del corpus ANCORA.
A continuación, las estadísticas obtenidas:

Cantidad de sentencias: 17379
Cantidad de ocurrencias de palabras: 517268
Tamaño del vocabulario: 46482
Tamaño del vocabulario de tags: 48


Los 10 tags más frecuentes, ordenados de más frecuente a menos frecuente, son:
------------------------------------------------------------------------------


El tag `nc`, aparece un total de 92002 veces y con un porcentaje de 17.78.
Sus lemas más frecuentes son:


el lema `años`, con una frecuencia de 849

el lema `presidente`, con una frecuencia de 682

el lema `millones`, con una frecuencia de 616

el lema `equipo`, con una frecuencia de 457

el lema `partido`, con una frecuencia de 438


El tag `sp`, aparece un total de 79904 veces y con un porcentaje total de 15.447.
Sus lemas más frecuentes son:

el lema `de`, con una frecuencia de 28475

el lema `en`, con una frecuencia de 12114

el lema `a`, con una frecuencia de 8192

el lema `del`, con una frecuencia de 6518

el lema `con`, con una frecuencia de 4150

El tag `da` aparece un total de 54552 veces y con un porcentaje total de 10.546.
Sus lemas más frecuentes son:

el lema `la`, con una frecuencia de 17897

el lema `el`, con una frecuencia de 14524

el lema `los`, con una frecuencia de 7758

el lema `las`, con una frecuencia de 4882

el lema `El`, con una frecuencia de 2817

El tag `vm` aparece un total de 50609 veces y con un porcentaje total de 9.784.
Sus lemas más frecuentes son:

el lema `está`, con una frecuencia de 564

el lema `tiene`, con una frecuencia de 511

el lema `dijo`, con una frecuencia de 499

el lema `puede`, con una frecuencia de 381

el lema `hace`, con una frecuencia de 350

El tag `aq` aparece un total de 33904 veces y con un porcentaje total de 6.554.
Sus lemas más frecuentes son:

el lema `pasado`, con una frecuencia de 393

el lema `gran`, con una frecuencia de 275

el lema `mayor`, con una frecuencia de 248

el lema `nuevo`, con una frecuencia de 234

el lema `próximo`, con una frecuencia de 213

El tag `fc` aparece un total de 30148 veces y con un porcentaje total de 5.828.
Su lema es:

el lema `,`, con una frecuencia de 30148

El tag `np` aparece un total de 29113 veces y con un porcentaje total de 5.628.
Sus lemas más frecuentes son:

el lema `Gobierno`, con una frecuencia de 554

el lema `España`, con una frecuencia de 380

el lema `PP`, con una frecuencia de 234

el lema `Barcelona`, con una frecuencia de 232

el lema `Madrid`, con una frecuencia de 196

El tag `fp` aparece un total de 21157 veces y con un porcentaje total de 4.09.
Sus lemas más frecuentes son:

el lema `.`, con una frecuencia de 17513

el lema `(`, con una frecuencia de 1823

el lema `)`, con una frecuencia de 1821

El tag `rg` aparece un total de 15333 veces y con un porcentaje total de 2.964.
Sus lemas más frecuentes son:

el lema `más`, con una frecuencia de 1707

el lema `hoy`, con una frecuencia de 772

el lema `también`, con una frecuencia de 683

el lema `ayer`, con una frecuencia de 593

el lema `ya`, con una frecuencia de 544

El tag `cc` aparece un total de 15023 veces y con un porcentaje total de 2.904.
Sus lemas más frecuentes son:

el lema `y`, con una frecuencia de 11211

el lema `pero`, con una frecuencia de 938

el lema `o`, con una frecuencia de 895

el lema `Pero`, con una frecuencia de 323

el lema `e`, con una frecuencia de 310



Breve descripción de los tags:
------------------------------

nc : nombre común,
dd : determinante demostrativo,
fc : el símbolo coma,
fs : los puntos suspensivos,
sp : preposicón adopción,
da: determinante artículo,
vm: verbo principal,
aq: adjetivo calificativo,
np: nombre propio,
fp: el símbolo punto,
rg: adverbio general,
cc: conjunción coordinada.


Niveles de ambigüedad:
----------------------

con 1 tag(s) hay 44109 lemas; los más frecuentes son:


el lema `,`, con 30148 ocurrencias y un porcentaje de 10.4175

el lema `el`, con 14524 ocurrencias y un porcentaje de 5.0187

el lema `en`, con 12114 ocurrencias y un porcentaje de 4.1859

el lema `con`, con 4150 ocurrencias y un porcentaje de 1.434

el lema `por`, con 4087 ocurrencias y un porcentaje de 1.4122

con 2 tag(s) hay 2194 lemas; los más frecuentes son:

el lema `la`, con 18100 ocurrencias y un porcentaje de 14.7375

el lema `y`, con 11212 ocurrencias y un porcentaje de 9.1291

el lema `"`, con 9296 ocurrencias y un porcentaje de 7.569

el lema `los`, con 7824 ocurrencias y un porcentaje de 6.3705

el lema `del`, con 6519 ocurrencias y un porcentaje de 5.3079

con 3 tag(s) hay 153 lemas; los más frecuentes son:

el lema `.`, con 17520 ocurrencias y un porcentaje de 34.6725

el lema `a`, con 8200 ocurrencias y un porcentaje de 16.228

el lema `un`, con 5198 ocurrencias y un porcentaje de 10.287

el lema `no`, con 3300 ocurrencias y un porcentaje de 6.5308

el lema `es`, con 2315 ocurrencias y un porcentaje de 4.5814

con 4 tag(s) hay 19 lemas; los más frecuentes son:

el lema `de`, con 28478 ocurrencias y un porcentaje de 87.2621

el lema `dos`, con 917 ocurrencias y un porcentaje de 2.8099

el lema `este`, con 830 ocurrencias y un porcentaje de 2.5433

el lema `tres`, con 425 ocurrencias y un porcentaje de 1.3023

el lema `todo`, con 393 ocurrencias y un porcentaje de 1.2042

con 5 tag(s) hay 4 lemas; los más frecuentes son:

el lema `que`, con 15391 ocurrencias y un porcentaje de 96.3926

el lema `mismo`, con 247 ocurrencias y un porcentaje de 1.5469

el lema `cinco`, con 224 ocurrencias y un porcentaje de 1.4029

el lema `medio`, con 105 ocurrencias y un porcentaje de 0.6576

con 6 tag(s) hay 3 lemas; los más frecuentes son:

el lema `una`, con 3852 ocurrencias y un porcentaje de 65.0346

el lema `como`, con 1736 ocurrencias y un porcentaje de 29.3095

el lema `uno`, con 335 ocurrencias y un porcentaje de 5.6559

no hay lemas con 7 o más tags.



Ejercicio 2: Baseline Tagger
============================


Implementamos un etiquetador muy básico, que para cada palabra, elige su etiqueta más probable,
basándonos en su etiqueta más frecuente observada en el entrenamiento. Y para las palabras que son desconocidas,
elegimos el tag más frecuente observado en todo el entrenamiento.


Ejercicio 3: Entrenamiento y Evaluación de Taggers
==================================================


Se implementaron los scripts train.py y eval.py. El primero es para entrenar modelos de tagging, y el segundo para evaluar 
la accuracy de nuestro modelo de tagging; calculamos la accuracy general (global), que son la cantidad de tags correctos
sobre cualquier palabra, la accuracy sobre palabras conocidas, que es la cantidad de palabras conocidas taggeadas correctamente, y 
por último, la accuracy sobre palabras desconocidas, que es la cantidad de palabras desconocidas que se taggearon correctamente.

Algunos resultados del Baseline Tagger:
---------------------------------------

Global accuracy: 89.00%

Accuracy in unknown words: 31.80%

Accuracy in known words: 95.31%



Ejercicio 4: Hidden Markov Models y Algoritmo de Viterbi
========================================================


Sobre Hidden Markov Models:
---------------------------

Se implementó un algoritmo de tagging (tomado de las notas de Michael Collins y de las notas de Martin Jurafsky), 
que se basa fuertemente en los Hidden Markov Models.
Este algoritmo a su vez, usa el algoritmo de Viterbi para crear la secuencia de tags más probable para una sentencia dada.


Sobre Viterbi:
--------------

Como fue mencionado anteriormente, el algoritmo de Viterbi crea la secuencia de tags más probable para una sentencia cualquiera.
Se tomó como referencia a los tests sobre Viterbi, y el pseudo código que aparece en las notas de Michael Collins.


Ejercicio 5: HMM POS Tagger
===========================


Implementamos un Hidden Markov Model, cuyos parámetros se estiman usando Maximum Likelihood sobre un corpus de oraciones etiquetadas, 
algo bastante parecido a lo que se hizo en el primer proyecto sobre modelado de lenguajes con ngramas.


Se entrenaron modelos y evaluaron modelos, obteniendo los siguientes resultados:


n = 1
-----

Accuracy: 89.01%

Accuracy in unknown words: 31.80%

Accuracy in known words: 95.32%


n = 2
-----

Accuracy: 92.72%

Accuracy in unknown words: 48.42%

Accuracy in known words: 97.61%


n = 3
-----

Accuracy: 92.76%

Accuracy in unknown words: 49.63%

Accuracy in known words: 97.52%


n = 4
-----

Accuracy: 92.78%

Accuracy in unknown words: 51.78%

Accuracy in known words: 97.30%


Ejercicio 6: Features para Etiquetado de Secuencias
===================================================


Se implementaron los siguientes features básicos:


word_lower:
-----------
Pone en minúsculas la palabra


word_istitle:
-------------
Indica si la palabra es un título (Primer letra en mayúscula y el resto de las letras en minúscula)


word_isupper:
-------------
Indica si la palabra está toda en mayúsculas


word_isdigit:
-------------
Indica si la palabra es un número


prev_tags:
----------
Devuelve el tag previo


NPrevTags:
----------
Devuelve una tupla de los tags previos

        
PrevWord(Feature):
------------------
Le aplica el Feature a la palabra previa


Ejercicio 7: Maximum Entropy Markov Models
==========================================

Calculamos la secuencia de tags más probable usando los features del ejercicio anterior y los clasificadores Logistic Regression,
Multinomial NB, Linear SVC. A continuación, los resultados de accuracy observados usando cada clasificador con orden 1, 2, 3 y 4.


Logistic Regression:
--------------------


n = 1
.....

Accuracy: 92.73%

Accuracy in unknown words: 68.95%

Accuracy in known words: 95.36%


n = 2
.....

Accuracy: 91.99%

Accuracy in unknown words: 68.76%

Accuracy in known words: 94.55%


n = 3
.....

Accuracy: 92.17%

Accuracy in unknown words: 69.11%

Accuracy in known words: 94.71%


n = 4
.....

Accuracy: 92.24%

Accuracy in unknown words: 69.64%

Accuracy in known words: 94.73%


Multinomial NB
--------------


n = 1
.....

Accuracy: 88.27%

Accuracy in unknown words: 52.85%

Accuracy in known words: 92.18%


n = 2
.....

Accuracy: 70.53%

Accuracy in unknown words: 37.77%

Accuracy in known words: 74.15%


n = 3
.....

Accuracy: 67.98%

Accuracy in unknown words: 38.28%

Accuracy in known words: 71.25%


n = 4
.....

Accuracy: 64.68%

Accuracy in unknown words: 40.41%

Accuracy in known words: 67.36%


Linear SVC
----------


n = 1
.....

Accuracy: 94.39%

Accuracy in unknown words: 70.34%

Accuracy in known words: 97.04%


n = 2
.....

Accuracy: 94.27%

Accuracy in unknown words: 70.47%

Accuracy in known words: 96.90%


n = 3
.....

Accuracy: 94.39%

Accuracy in unknown words: 71.29%

Accuracy in known words: 96.94%


n = 4
.....

Accuracy: 94.45%

Accuracy in unknown words: 71.71%

Accuracy in known words: 96.96%



En base a los resultados, podemos apreciar que el clasificador que con el cual se obtienen mejores resultados, 
es el Linear SVC de orden n = 4.



Nota:
-----



1. Se proveen dos scrips: train_models.sh y eval_models.sh. El primero entrena todos los modelos implementados
con sus variantes (uso de addone y órdenes de n € {1,2,3,4}), y el segundo, evalúa los modelos entrenados.



2. Para obtener la matriz de confusión a la hora de evaluar un modelo, usar '-m 1' al final del comando, por ejemplo,
   $ python scripts/eval.py -i generic_model_path -m 1.


3. Para la matriz de confusión, se optó por imprimir las tuplas (row, column) : value, correspondientes a la matriz,
   por un tema de comodidad a la hora de leerla o buscar algún resultado en particular. También se optó por ignorar
   las entradas de la matriz en cuyo valor (r, c) sea igual a 0.
