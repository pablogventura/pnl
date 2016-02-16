================================================
PLN 2015: Procesamiento de Lenguaje Natural 2015
================================================

Práctico 4: Algoritmo de Smoothing Kneser-Ney
=============================================

En el `Práctico 1`_ se trabajo con el Modelado de Lenguaje y varias técnicas de *smoothing* para lidiar con palabras no conocidas.
El objetivo de este práctico es implementar otra técnica de *smoothing* con la que se esperan obtener mejores resultados que los ya observados.
La implementación del algoritmo de *smoothing* está inspirado en el *techinical report* de `Chen & Goodman`_ y en la tesis de `Martin Christian Körner`_

La idea básica detrás del algoritmo de *Kneser Ney* es introducir de alguna manera la idea de contexto. Por ejemplo, como explica Dan Jurafsky en sus videolecturas_, en un corpus podemos observar una gran cantidad de unigramas 'San', pero si nos movemos a bigramas, vemos que en la gran mayoría de los casos el unigrama 'San', solo está acompañado del unigrama 'Francisco'.

Esta técnica en vez de centrarse solo en la cuenta de ngramas, también se focaliza en la cantidad de contextos en los que ése ngrama aparece.

Experimentos y Resultados
-------------------------

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
| Model / Smoothing               | n = 1     | n = 2  | n = 3    | n = 4   |
+=================================+===========+========+==========+=========+
| NGram                           |               Inf                       |
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
| Model / Smoothing               | n = 1     | n = 2  | n = 3    | n = 4   |
+=================================+===========+========+==========+=========+
| NGram                           |               Inf                       |
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
| Model / Smoothing               | n = 1     | n = 2  | n = 3    | n = 4   |
+=================================+===========+========+==========+=========+
| NGram                           |               Inf                       |
+---------------------------------+-----------+--------+----------+---------+
| AddOneNGram                     |  1944.95  |6391.66 | 37478.36 | 55587.10|
+---------------------------------+-----------+--------+----------+---------+
| InterpolatedNGram               | 2155.14   |1821.52 | 1899.86  |1914.00  |
+---------------------------------+-----------+--------+----------+---------+
| BackOffNGram                    | 2155.14   |1541.76 |  1659.18 |1700.70  |
+---------------------------------+-----------+--------+----------+---------+
| KneserNeyNGram                  |  1944.95  | 1170.80| 917.71   | 1034.76 |
+---------------------------------+-----------+--------+----------+---------+






.. _videolecturas: https://class.coursera.org/nlp/lecture/20
.. _`Práctico 1`: https://github.com/giovannirescia/PLN-2015/tree/practico1/languagemodeling
.. _`Chen & Goodman`: http://www.cs.berkeley.edu/~klein/cs294-5/chen_goodman.pdf
.. _`Martin Christian Körner`: https://west.uni-koblenz.de/sites/default/files/BachelorArbeit_MartinKoerner.pdf
