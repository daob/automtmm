.. automtmm documentation master file, created by sphinx-quickstart on Tue May  5 16:34:54 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Automtmm Documentation
======================

.. toctree::
   :maxdepth: 2


Goals and background
====================

.. _intro:

This document describes ``automtmm``, a suite of computer programs that 
automatizes parts of the process of analyzing MTMM experiments.

The program is developed in the context of the European Social Survey's Joint 
Research Activities 3 project (JRA-3), which aims to estimate and improve the 
quality of the questionnaire. 

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
are 23 countries in which experiments were performed, four experiments, 
and twelve questions within each experiment.  There are therefore 1104
validities and 1104 reliabilities to be estimated: a total of 2208 parameters
of interest. For the subsequent meta-analysis additional technical data on these 
parameters is needed that, until the development of ``automtmm``,
was not provided by any existing computer program.

Because of the difficulties associated with preparing the data, estimating 
the parameters, and storing them together with additional information that
is not given directly by existing computer programs, a new program was developed.
Besides assisting with the JRA-3 group's analysis of the currently available 
data, this program also has the following advantages:
    
    * Subsequent rounds can be quickly analyzed as new data become
      available;

    * The quality prediction program SQP, used by the CCT in the evaluation
      process of the ESS rotating modules, will be improved based on the extra
      information obtained by ``automtmm`` that cannot be obtained in other
      ways;

    * Other researchers that may wish to analyze the same experiments with
      different models can quickly obtain the results for all of their analyses.

Overall, therefore, this collection of programs greatly improves the 
computational efficiency of the process of quality control and improvement 
by MTMM experiments.

The document consists of two chapters. The current chapter explains the goals
and the background of the program, as well as its workings in a manner meant for
a broad audience. The second chapter, *Documentation*, documents the Python
and R modules, classes, and functions that make up the program. It is intended
as reference material for those who want to use or change the program.

The next section briefly discusses different approaches to quality control of
questionnaires, as well as the set-up of the experiments and 
our approach in analyzing them. The following section motivates the need for the development of
``automtmm``. In the third section of this chapter the general structure and 
methodological background of the program will be explained.


Evaluation of the quality of survey questions by MTMM experiments
-----------------------------------------------------------------


The quality of survey questions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are different ways to study the quality of survey questions. Most
prominent among them are cognitive interviewing, behavior coding, and
psychometric assessment. Cognitive interviewing is a collection of
techniques that are meant to reveal how respondents arrive at 
their answers [willis2005]_. 
In behavior coding, formal codes for the interaction between
interviewer and respondent are developed and the entire interview is coded. This
then reveals 'incorrect' behavior on the part of interviewer or respondent
[zouwen1998]_. Finally, psychometric assessment is a statistical analysis 
of the answers to different questions that should be related according 
to a measurement model [lord1968]_. 

The three approaches are complementary to each other; psychometric models alone
can estimate the extent of random and systematic errors in the questions and are
therefore indispensable. But they cannot reveal anything about the interpretation 
that is given to the questions by different respondents. 
Cognitive interviewing gives insight into these interpretations, and can provide
suggestions for improvement in the concepts behind the questions. Behavior coding 
can identify more precisely what is going wrong in the survey interview that may 
be causing errors.

The ESS has recently performed a cross-national cognitive interviewing project 
[fitzgerald2009]_, which was successful in showing 
"...how respondents understood some of the questions and how they went about answering
[them, and in] identifying and classifying the nature of any problems found..."
(p. 12). In the ESS Dutch pilot study some interviews were recorded on audio 
and coded, revealing parts of the questionnaire that yield
problematic interactions between interviewer and respondent [ongena2003]_. 

The ESS has also performed many experiments that allow for the psychometric
assessment of the reliability and internal validity of questions, and
``automtmm`` has been developed to aid in this procedure. Therefore the rest of
this document discusses psychometric assessment in more detail. The following
section explains briefly how this assessment is done.


.. _mtmm-example:
.. figure:: trait-1.pdf

    A trait measured by three different methods from round two of the ESS.

A short explanation of MTMM
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In every round of the European Social Survey experiments are built in to evaluate 
the quality of the questions by statistical estimation. Each of these experiments 
consist of repeating at least three different questions in at least three 
different ways (see figure :ref:`mtmm-example`). 
This way one can separate how much of the variance of each
ESS question in the experiment is due to the 'trait' to which the question is
supposed to refer, and how much is due to the 'method' of asking it. Therefore
the type of experiment is also called 'multitrait-multimethod'
[campbell1959]_.

Our basic response model is shown on the left-hand side of the figure below. 
It can be seen that the observed variable is a combination of random measurement 
error and a so-called 'true score'. 
This score represents the opinion of the respondent expressed
in the particular method of asking the question, free of random errors. But the
true score is not completely free of error: it is itself a combination of
systematic measurement errors in the form of a method factor on the one hand,
and the true opinion or 'trait' on the other. The method factor represents
the fact that different respondents arrive at an answer to 
questions asked by this specific method in their own way that is stable across questions.

The right-hand side of the figure shows this basic response model applied to the
variety of work example. In this picture, one would have liked to have measured
'work variety', but obtained only the observed scores. Although true 'work
variety' can never be observed, it can be estimated how strong the
relationship between this variable and the observed answers is.

+-------------------------------+---------------------------------------+
| .. image:: response_model.pdf | .. image:: response_model_example.pdf |
+-------------------------------+---------------------------------------+

The path diagrams in the figure can also be expressed in equations as

    *y = τ + ε*

    *τ = m.M + v.T*

where *y* is the observed variable, *τ* the true score, *ε* the random error
component, *M* the method factor, and *T* the trait, and *m* and *v* are scaling coefficients.
This model implies that the deviation scores of the observed variable are unbiased for the 
true score, and that there are no unique components in the true score besides
method and trait variance.

It can then be shown that the proportion of random error in the observed variable
equals *var(e)/var(y)*, which we call the 'reliability' of the question.
The proportion of variance in the true score due to the trait we want to measure
is called the internal 'validity' and equals *v.[var(T)/var(τ)]*.

The model shown is clearly not identified as there is only one observed
variable and four unobserved variables. 
However, in the ESS experiments there are three traits and three or
four methods, yielding nine or twelve observed variables. Then the model is
identified under the following assumption:

    Cov(T\ :sub:`i`\, M\ :sub:`j`\) = Cov(T\ :sub:`i`\, ε\ :sub:`j`\) = 
    Cov(M\ :sub:`j`\, ε\ :sub:`i`\) = Cov(ε\ :sub:`i`\, ε\ :sub:`j`\) = 0,
    for all *i* not equal to *j*;
   
that is, there are no correlations between the traits and methods, 
among the methods, among the random errors, or between either traits
or methods and random errors.

Furthermore in the first instance the following assumptions are also made but
relaxed when necessary:

    #. Cov(ε\ :sub:`i`\, ε\ :sub:`j`\) = 0 (uncorrelated error terms);
    #. *m*\ :sub:`ij`\ *= 1* for all *i* and *j*. (equal scaling coefficients for the
       method factors)

The goal of the MTMM experiments is to estimate how much random and systematic
error each question contains. That is, it is to estimate the validity and
reliability of the questions. These two quantities can be expressed as the
standardized coefficients of a structural equation model (SEM) [saris1991]_. We then label
these coefficients the *validity coefficient* and the *reliability coefficient*.
Their product, the *quality coefficient*, is the square root of the proportion
of variation in the observed variable that is explained by the trait we want
to measure. 

For instance, in the work variety example above, if the quality coefficient 
for an 11 point scale in Norway were to equal *0.8*, then 
*0.8*\ :sup:`2`\ *(100) = 64%* of the variation in the observed answers to the question 
"Please indicate, on a scale of 0 to 10, how varied your work is..." is due to
the respondents' perception of variety in their work, while 36% is random and
systematic measurement error. In round 3 of the ESS, the median quality
coefficient found was *0.7*.


Why estimate the quality?
-------------------------

The European Social Survey aims to allow governments, policy analysts, 
scholars and members of the public to interpret how people in 
different countries and at different times see themselves and 
the world around them.

The reliability and validity of the survey questions have several influences on
this goal:

    #. The lower the quality of a question, **the larger the amount of variation
       in that variable that has no interpretation**. This means that real
       differences between countries or across time will take larger
       sample sizes to detect than would otherwise be the case. Since larger
       sample sizes cost money, it follows that measurement error costs money.
    
    #. Besides increasing the variance of variables users analyse, low quality
       questions will also have lower correlations with other variables. The
       consequence is that regression coefficients, cross-tables, and other
       measures of relationship will be biased. This bias can be
       upwards as well as downwards [fuller1986]_. 

    #. If the reliability and validity are different in different countries or
       times, measures of relationship will be biased differently. Thus, for
       measures of relationship
       **differences between countries and times arise that have no
       interpretation, or true differences are suppressed**. Previous studies
       have shown that there is considerable variation in quality across
       countries [oberski2004]_.

These arguments clarify both the need to create questions that are as good as
possible and the need to estimate the extent of the errors so that corrections
can be made afterwards.

After the estimation, the second need is immediately satisfied, because the
estimates of the quality can be used directly to correct estimates of regression
coefficients.

The improvement of questions is more complicated, because it involves
identifying precisely which methods of asking a question are better or worse.
For this purpose the program SQP was developed, which suggests improvement of
questions based on their characteristics [sqp2007]_. It also provides estimates of
the quality of the question so that survey estimates can be corrected. 

This programme, however, currently has limited use for cross-national 
comparisons in the ESS, because it does not provide estimates for all
participating countries and languages. Moreover, with the great wealth of
information available from the ESS experiments, it could be greatly improved.

Therefore, the multitrait-multimethod experiments conducted in the European
Social Survey:

    * Contribute to the improvement of the ESS questionnare, yielding higher
      efficiency and a greater power for governments, policy analysts, 
      scholars and members of the public to detect important phenomena;

    * Contribute to the improvement of survey questions in general;

    * Contribute academic knowledge about the way people answer different kinds
      of questions in different cultures and languages;

    * Allow for the correction of the effect measurement errors have on estimates
      and the cross-national comparison of those estimates.


Complications and the solution: split ballot MTMM
-------------------------------------------------

The model shown above has the advantage of being able to evaluate the
reliability and validity of any survey question, and of being able to identify
which methods of asking it provide the highest quality. 

Moreover, in cross-national comparisons, for which the ESS has been designed, 
differences between the countries in reliability and validity may cause differences in
regression coefficients and other measures of relationship.

split ballot [saris2004]_



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

.. [fitzgerald2009]  Fitzgerald R., S. Widdop, M. Gray, and D. Collins (2009).
    "Testing for equivalence using cross-national cognitive interviewing".
    *Centre for Comparative Social Surveys Working Paper Series*, paper no. 01.

.. [fuller1986] Fuller, W. A. (1986). *Measurement error models*. New York: Wiley.

.. [lord1968] Lord, F. M. and Novick, M. R. (1968). 
    *Statistical theories of mental test scores*.  Reading MA: Addison-Welsley Publishing Company.

.. [maxima2009] The Maxima Group (2009). *Maxima, a Computer Algebra System*. 
    Version 5.18.1 <http://maxima.sourceforge.net/>

.. [oehlert1992] Oehlert, G. W. (1992). A Note on the Delta Method.
    *The American Statistician*, 46 (1), pp. 27-29.

.. [oliphant2006]  Oliphant, T. E. (2006). *Guide to NumPy*. 
    <http://numpy.scipy.org/>.

.. [oberski2004] Oberski, D. L., W. E. Saris, and J. A. P. Hagenaars (2004). 
    "Why are there Differences in Measurement Quality across Countries?"
    in: *Measuring meaningful data in social research*, G. Loosveldt, M.
    Swyngedouw, and B. Cambré (eds.). Leuven: Acco.

.. [ongena2003]  Ongena, Y. (2003).
    *Pre-testing the ESS-questionnaire using interaction analysis*.
    <http://europeansocialsurvey.org/?option=com_docman&task=doc_download&gid=181&itemid=80>

.. [R2005] R Development Core Team (2005). *R: A language and environment for
    statistical computing*. Vienna, Austria: R Foundation for Statistical Computing,
    <http://www.R-project.org>.

.. [rossum2009] Rossum, G. van, and F. L. Drake Jr. (ed.) (2009).
    *The Python Language Reference*. Hampton, NH: Python Software Foundation.

.. [saris1991] Saris, W. E. and F. Andrews (1991). 
    "Evaluation of measurement instruments using a structural modeling
    approach".
    In: *Measurement errors in surveys*, Biemer, P. P. et al. (eds.).
    New York: Wiley.

.. [saris2004] Saris, W. E., Satorra, A. and G. Coenders (2004). 
    A new approach to evaluating the quality of measurement instruments: 
    the split-ballot MTMM design.
    *Sociological methodology*, 34(1), pp. 311-347.

.. [saris2007] Saris, W. E. and I. Gallhofer (2007).
    *Design, Evaluation, and Analysis of Questionnaires for Survey Research*.
    New York: Wiley.

.. [sqp] Saris, W. E., D. Oberski, and S. Kuipers. *SQP: Survey Quality
    Predictor* (computer programme). <http://www.sqp.nl/>

.. [willis2005] Willis, B. G. (2004).
    *Cognitive interviewing: a tool for improving questionnaire design*. 
    London: Sage.

.. [zouwen1998]  Van der Zouwen, J. en W. Dijkstra (1998).
    Het vraaggesprek onderzocht. Wat zegt het verloop van de interactie in 
    survey-interviews over de kwaliteit van de vraagformulering?
    [The survey interview dissected. What does the course of the interaction
    in survey-interviews tell us about the quality of the question formulation?]
    *Sociologische Gids*, 45(6), 387-403.


Documentation
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

