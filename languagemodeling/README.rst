================================================
PLN 2015: Procesamiento de Lenguaje Natural 2015
================================================

Práctico 4: Algoritmo de Smoothing Kneser-Ney
=============================================

En el `Práctico 1`_ se trabajó con el Modelado de Lenguaje y varias técnicas de *smoothing* para lidiar con palabras no conocidas.
El objetivo de este práctico es implementar otra técnica de smoothing con la que se esperan obtener mejores resultados que los ya observados.
La implementación del algoritmo de smoothing está inspirado en el *techinical report* de `Chen & Goodman`_ y en la tesis de `Martin Christian Körner`_.

La idea básica detrás del algoritmo de *Kneser Ney* es introducir de alguna manera la idea de contexto. Por ejemplo, como explica Dan Jurafsky en sus videolecturas_, en un corpus podemos observar una gran cantidad de unigramas 'San', pero si nos movemos a bigramas, vemos que en la gran mayoría de los casos el unigrama 'San', solo está acompañado del unigrama 'Francisco'.

Esta técnica en vez de centrarse solo en la cuenta de ngramas, también se focaliza en la cantidad de contextos en los que ése ngrama aparece.

Entrenar y Evaluar Modelos
--------------------------

Para entrenar un modelo::

  python scripts/train.py -n <int> -m kn -c <str> -o <str> [-D <int>]

Donde:

* ``-n`` seleccionar el orden del del ngrama
* ``-m`` seleccionar el algoritmo de smoothing:

  - ``kn`` para usar kneserney
* ``-c`` seleccionar el Corpus para entrenar:

  - ``S`` para usar el corpus Shakespeare (valor por defecto)
  - ``B`` para usar el corpus Brown
  - ``G`` para usar el corpus Gutenberg

* ``-o`` seleccionar el nombre en el cuál se guardará el modelo
* ``-D`` seleccionar si calcular el valor de *discounting* por *barrido* o que sea calculado con las cuentas de ngramas.

  - ``1`` para ser calculado con las cuentas de ngramas (valor por defecto: None)

Algunos ejemplos::

  python scripts/train.py -n 3 -m kn -c S -o trained_models/kn_model_3_s -D 1
  python scripts/train.py -n 1 -m kn -c G -o my_models/kn_model_1
  python scripts/train.py -n 2 -m kn -o kn_model_2

Para evaluar::

  python scripts/eval.py -i <str>

Donde:

* ``-i`` es la ruta hacia algún modelo entrenado

Por ejemplo::

  python scripts/eval.py -i trained_models/kn_model_3_s


También se provee un *script* que entrena todos los algoritmos de smoothing y luego los evalúa, creando reportes de cada técnica para cada corpus. Para ejecutar::

  sh scripts/do_all.sh

**NOTA**: Para los modelos Interpolated y Backoff se buscan sus parámetros por barrido, por lo que el entrenamiento dura alrededor de 2:30 horas; y la evaluación de todos los modelos dura alrededor de 30 minutos. El script demora cerca de 3 horas en ejecutarse.

Se cuenta con tests para el modelo, para ejecutar::

  python nosetests test/test_kenserney_ngram.py

Experimentación y Resultados
----------------------------

Corpora
*******

Todos los modelos fueron entrenados y evualuados usando la siguiente *corpora*:

* Shakespeare Corpus
* Gutenberg Corpus
* Brown Corpus

Resultados
**********

Shakespeare Corpus
__________________

+---------------------------------+-----------+--------+----------+---------+
|                                 |      Perplexity                         |
+---------------------------------+-----------+--------+----------+---------+
| Model / Smoothing || Orden n    | n = 1     | n = 2  | n = 3    | n = 4   |
+=================================+===========+========+==========+=========+
| NGram                           | Infinite  |Infinite|  Infinite|Infinite |
+---------------------------------+-----------+--------+----------+---------+
| AddOneNGram                     |  833.015  | 1975.82| 13570.08 | 24318.21|
+---------------------------------+-----------+--------+----------+---------+
| InterpolatedNGram               | 834.65    | 352.03 |   331.69 |328.33   |
+---------------------------------+-----------+--------+----------+---------+
| BackOffNGram                    | 834.65    | 273.22 |   254.69 | 261.08  |
+---------------------------------+-----------+--------+----------+---------+
| KneserNeyNGram                  |  833.01   | 261.58 |   201.12 |  239.14 |
+---------------------------------+-----------+--------+----------+---------+

Brown Corpus
____________

+---------------------------------+-----------+--------+----------+---------+
|                                 |      Perplexity                         |
+---------------------------------+-----------+--------+----------+---------+
| Model / Smoothing || Orden n    | n = 1     | n = 2  | n = 3    | n = 4   |
+=================================+===========+========+==========+=========+
| NGram                           | Infinite  |Infinite|  Infinite|Infinite |
+---------------------------------+-----------+--------+----------+---------+
| AddOneNGram                     |  1512.77  | 5500.39| 36192    | 59218.4 |
+---------------------------------+-----------+--------+----------+---------+
| InterpolatedNGram               | 1570.48   | 680.69 |   660.24 |660.91   |
+---------------------------------+-----------+--------+----------+---------+
| BackOffNGram                    | 1570.48   | 490.55 |  481.41  | 494.52  |
+---------------------------------+-----------+--------+----------+---------+
| KneserNeyNGram                  |  1512.77  | 453.84 |  414.33  | 507.97  |
+---------------------------------+-----------+--------+----------+---------+

Gutenberg Corpus
________________

+---------------------------------+-----------+--------+----------+---------+
|                                 |      Perplexity                         |
+---------------------------------+-----------+--------+----------+---------+
| Model / Smoothing || Orden n    | n = 1     | n = 2  | n = 3    | n = 4   |
+=================================+===========+========+==========+=========+
| NGram                           | Infinite  |Infinite|  Infinite|Infinite |
+---------------------------------+-----------+--------+----------+---------+
| AddOneNGram                     |  1944.95  |6391.66 | 37478.36 | 55587.10|
+---------------------------------+-----------+--------+----------+---------+
| InterpolatedNGram               | 2155.14   |1821.52 | 1899.86  |1914.00  |
+---------------------------------+-----------+--------+----------+---------+
| BackOffNGram                    | 2155.14   |1541.76 |  1659.18 |1700.70  |
+---------------------------------+-----------+--------+----------+---------+
| KneserNeyNGram                  |  1944.95  | 1170.80| 917.71   | 1034.76 |
+---------------------------------+-----------+--------+----------+---------+



Conclusiones y trabajos futuros
-------------------------------

Como puede apreciarse, los resultados de Modelos con smoothing Kneser-Ney son los mejores, salvo en el caso del Corpus Brown de orden 4. En el trabajo de `Chen & Goodman`_ se explica que el desempeño de un modelo depende del tamaño del Corpus, la longitud promedio de las sentencias y el orden mismo del modelo, entre otras cosas. Por eso podemos concluir sin lugar a duda, que ésta es la mejor técnica de smoothing de las implementadas anteriormente_. Como experimento futuro, se implementará otra versión del algoritmo de Kneser-Ney, en la cual se calculan distintos valores de *discounting* D, dependiendo de las *counts* que se observen en el momento. El algoritmo está explicado también en `Chen & Goodman`_, el cual prueban que tiene aún mejor rendimiento.


.. _videolecturas: https://class.coursera.org/nlp/lecture/20
.. _`Práctico 1`: https://github.com/giovannirescia/PLN-2015/tree/practico1/languagemodeling
.. _anteriormente: https://github.com/giovannirescia/PLN-2015/tree/practico1/languagemodeling
.. _`Chen & Goodman`: http://www.cs.berkeley.edu/~klein/cs294-5/chen_goodman.pdf
.. _`Martin Christian Körner`: https://west.uni-koblenz.de/sites/default/files/BachelorArbeit_MartinKoerner.pdf
