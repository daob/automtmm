.. automtmm documentation master file, created by sphinx-quickstart on Tue May  5 16:34:54 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to automtmm's documentation!
====================================

Contents:

.. toctree::
   :maxdepth: 2




Introduction
============
.. _intro:

[what is said in which section]

In every round of the European Social Survey experiments are built in to evaluate 
the quality of the questions by statistical estimation. Each of these experiments 
consist of repeating at least three different questions in at least three 
different ways (see figure :ref:`mtmm-example`). 
This way one can separate how much of the variance of each
ESS question in the experiment is due to the 'trait' to which the question is
supposed to refer, and how much is due to the 'method' of asking it. Therefore
the type of experiment is also called 'multitrait-multimethod'
[campbell1959]_.

The goal of these experiments is to estimate how much random and systematic
error each question contains. These two quantities can be expressed as the
standardized coefficients of a structural equation model (SEM). We then label
these coefficients the *validity coefficient* and the *reliability coefficient*.
The squares of these coefficients equal the proportion of variance in the
observed variable due to the trait and the true score, respectively.

.. _mtmm-example:
.. figure:: trait-1.pdf

    A trait measured by three different methods.

split ballot [saris2004]_

complicated data processing therefore program

meta analysis

need lots of standardized estimates and their vcov, may change, future rounds
new data need to be added therefore program

The delta method [oehlert1992]_.

Explanation of the program and structure


.. [campbell1959] Campbell, D. T. and Fiske, D. W. (1959). Convergent and 
    discriminant validation by the multitrait-multimethod matrix. 
    *Psychological bulletin*, 56 (2).

.. [oehlert1992] Oehlert, Gary W. (1992). A Note on the Delta Method.
    *The American Statistician*, 46 (1), pp. 27-29.

.. [saris2004] Saris, Willem E., Satorra, Albert and Germà Coenders (2004). 
    A new approach to evaluating the quality of measurement instruments: 
    the split-ballot MTMM design.
    *Sociological methodology*, 34(1), pp. 311-347.


Program code documentation
=========================
.. _program_doc:

Module that reads and interprets LISREL input and output files
--------------------------------------------------------------

.. automodule:: parse_lisrel
    :members:

.. autoclass:: LisrelInput
    :members:


Module that calculates analytical derivatives of the standardized coefficients with respect to the free parameters of the model
--------------------------------------------------------------

.. automodule:: read_maxima
    :members:

Module that runs the LISREL input files and gathers the results
---------------------------------------------------------------

.. automodule:: walk_and_run
    :members:

Module that preprocesses the ESS data files for MTMM analysis
------------------------------------------------------------

This module consists of various ``R`` scripts that perform the following tasks:

    * Read in the ESS SPSS data sets for the main and supplementary questionnaires,
      select variables, change some labels, and merge the files
    * Given the merged dataset, write covariance matrices and means of the 
      experimental variables to files for each country, experiment, and split-ballot group.
      This results is <number of countries> directories, each containing 
      <number of experiments> subdirectories, each containing <number of split-ballot groups>
      files with the covariances and the same number of files for the means.


Indices and tables
==================
.. _index:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

