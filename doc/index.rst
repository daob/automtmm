.. automtmm documentation master file, created by sphinx-quickstart on Tue May  5 16:34:54 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to automtmm's documentation!
====================================

Contents:

.. toctree::
   :maxdepth: 2


Goals and background
====================

.. _intro:

This document describes ``automtmm``, a computer program that automatizes parts
of the process of analyzing MTMM experiments.

The program is part of the European Social Survey's Joint Research Activities 3
project (JRA-3), which aims to estimate and improve the quality of the questionnaire. 

JRA-3 has two goals: control and improvement of the translation of the
source questionnaire, and control and improvement of the survey questions
themselves. ``automtmm`` has been developed to assist this second goal. It is
described in the work description of the project as deliverable 9.

The quality of survey questions is defined in terms of their reliability and 
internal validity, and these quantities are estimated. Those estimates themselves
then become the subject of a 'meta-analysis' predicting the quality of a question from
many of its characteristics such as the number of categories, syllables,
language, and so forth [#]_.

.. [#] For a full overview of this approach and the characteristics used, please
       see [saris2007]_.

Obtaining the estimates for all countries, rounds, experiments and
questions is not trivial. In the third round of the ESS alone there 
are 23 countries in which the experiments were performed, four experiments, 
and twelve questions within each experiment. That means 1104
validities and 1104 reliabilities are to be estimated: a total of 2208 parameters
of interest. For the subsequent meta-analysis additional technical data on these 
parameters is needed that was not provided by any existing computer program.

Because of the difficulties associated with preparing the data, estimating 
the parameters, and storing them together with additional information that
is not given directly by existing computer programs, a new program was developed.

Besides assisting with the JRA-3 group's analysis of the currently available 
data, the program also has the following advantages:
    
    * Subsequent rounds can be quickly analyzed as new data become
      available;

    * The quality prediction program SQP, used by the CCT in the evaluation
      process of the ESS rotating modules, will be improved based on the extra
      information obtained by ``automtmm`` that cannot be obtained in other
      ways;

    * Other researchers that may wish to analyze the same experiments with
      different models can quickly obtain the results for all of their analyses.

The document consists of two chapters. The current chapter explains the goals
and the background of the program, as well as its workings in a manner meant for
a broad audience. The second chapter, *Code Documentation*, documents the Python
and R modules, classes, and functions that make up the program. It is intended
as reference material for those wanting to use or change the program.




A short explanation of MTMM
---------------------------

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


.. _response_model:
+-------------------------------+---------------------------------------+
| .. image:: response_model.pdf | .. image:: response_model_example.pdf |
+-------------------------------+---------------------------------------+





The need for a new program
--------------------------

complicated data processing therefore program

meta analysis

need lots of standardized estimates and their vcov, may change, future rounds
new data need to be added therefore program

The delta method [oehlert1992]_.


How ``automtmm`` works
----------------------

Explanation of the program and structure


.. [campbell1959] Campbell, D. T. and Fiske, D. W. (1959). Convergent and 
    discriminant validation by the multitrait-multimethod matrix. 
    *Psychological bulletin*, 56 (2).

.. [maxima2009] The Maxima Group (2009). *Maxima, a Computer Algebra System*. 
    Version 5.18.1 <http://maxima.sourceforge.net/>

.. [oehlert1992] Oehlert, Gary W. (1992). A Note on the Delta Method.
    *The American Statistician*, 46 (1), pp. 27-29.

.. [oliphant2006]  Oliphant, Travis E. (2006). *Guide to NumPy*. 
    <http://numpy.scipy.org/>.

.. [R2005] R Development Core Team (2005). *R: A language and environment for
    statistical computing*. Vienna, Austria: R Foundation for Statistical Computing,
    <http://www.R-project.org>.

.. [rossum2009] Rossum, Guido van, and Fred L. Drake Jr. (ed.) (2009).
    *The Python Language Reference*. Hampton, NH: Python Software Foundation.

.. [saris2004] Saris, Willem E., Satorra, Albert and Germà Coenders (2004). 
    A new approach to evaluating the quality of measurement instruments: 
    the split-ballot MTMM design.
    *Sociological methodology*, 34(1), pp. 311-347.

.. [saris2007] Saris, Willem E. and Irmtraud Gallhofer (2007).
    *Design, Evaluation, and Analysis of Questionnaires for Survey Research*.
    New York: Wiley.


Code documentation
==================
.. _program_doc:

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


Indices and tables
==================
.. _index:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

