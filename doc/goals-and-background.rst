Goals and background
====================

.. toctree::
   :maxdepth: 2

This chapter describes the need for quality evaluation in the ESS and
cross-national surveys in general, our approach to quality evaluation,
complications arising from this approach, and consequently the motivation 
for the development of a new collection of computer programmes. 

It also explains the functions of the different modules that make up
``automtmm``. The explanation found in this chapter is meant for practitioners
and methodologists who are not developers.

The following section briefly discusses different approaches to quality control of
questionnaires, as well as the set-up of the experiments and 
our approach in analyzing them. The next section motivates the need for the development of
``automtmm``. In the third section of this chapter the general structure and 
methodological background of the programme will be explained.


Evaluation of the quality of survey questions by MTMM experiments
-----------------------------------------------------------------

The quality of survey questions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are different ways to study the quality of survey questions. Most
prominent among them are cognitive interviewing, behaviour coding, and
psychometric assessment. Cognitive interviewing is a collection of
techniques that are meant to reveal how respondents arrive at 
their answers [willis2005]_. 
In behaviour coding, formal codes for the interaction between
interviewer and respondent are developed and the entire interview is coded. This
then reveals 'incorrect' behaviour on the part of interviewer or respondent
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
this document discusses the need for psychometric assessment and how it is done
in more detail. 

Why estimate the quality?
~~~~~~~~~~~~~~~~~~~~~~~~~

The European Social Survey aims to allow governments, policy analysts, 
scholars and members of the public to interpret how people in 
different countries and at different times see themselves and 
the world around them.

The reliability and validity of the survey questions have several influences on
this goal:

    #. The lower the quality of a question, **the larger the amount of variation
       in that variable that has no interpretation**. This means that real
       differences between countries or across time will take larger
       sample sises to detect than would otherwise be the case. Since larger
       sample sises cost money, it follows that measurement error costs money.
    
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
For this purpose the programme SQP was developed, which suggests improvement of
questions based on their characteristics [sqp2007]_. It also provides estimates of
the quality of the question so that survey estimates can be corrected. 

This programme, however, currently has limited use for cross-national 
comparisons in the ESS, because it does not provide estimates for all
participating countries and languages. Moreover, with the great wealth of
information available from the ESS experiments, it could be greatly improved.

Therefore, the multitrait-multimethod experiments conducted in the European
Social Survey:

    * Contribute to the improvement of the ESS questionnaire, yielding higher
      efficiency and a greater power for governments, policy analysts, 
      scholars and members of the public to detect important phenomena;

    * Contribute to the improvement of survey questions in general;

    * Contribute academic knowledge about the way people answer different kinds
      of questions in different cultures and languages;

    * Allow for the correction of the effect measurement errors have on estimates
      and the cross-national comparison of those estimates.

The following section briefly explains the rationale and implementation of these
experiments.

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
*systematic* measurement errors in the form of a method factor on the one hand,
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
    ∀ *i* ≠ *j*;
   
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
standardised coefficients of a structural equation model (SEM) [saris1991]_. We then label
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



Complications and the solution: split ballot MTMM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The model shown above has the advantage of being able to evaluate the
reliability and validity of any survey question, and of being able to identify
which methods of asking it provide the highest quality. 

However, it also entails asking the same question of the same respondent three
or even four times. This increases the burden on the respondent quite a lot, as
well as increasing the likelihood that the respondents remember their previous 
answer (memory effects). Therefore in the ESS a
different design has been implemented: the split ballot MTMM design
[saris2004]_.

In the split ballot MTMM design, each respondent is asked the question once in
the format of the main questionnaire, and again one more time at the end of the
interview in a different format. The table below shows the resulting design
applied to the variety of work example shown earlier.

+----------------+----------+---------+
| Method         |  Group 1 | Group 2 |
+================+==========+=========+
| 4pt horizontal |    ×     |     ×   |
+----------------+----------+---------+
| 4pt vertical   |    ×     |         |
+----------------+----------+---------+
| 11pt horizontal|          |    ×    |
+----------------+----------+---------+

The table shows that the combination of "4pt vertical" and "11pt
horizontal" is never observed for the same person. However, if the groups are
assigned completely at random the MTMM model formulated above is still identified 
even given this planned missing data [#]_.

.. [#] The crucial assumption here is that of no correlation between the method factors for
       these two methods.

The split-ballot MTMM design makes the MTMM setup feasible in practice. However,
it also complicates the analysis. Instead of a single group analysis, a multiple
group analysis has to be run, where care is taken that the correct order of
variables is maintained and the correct across-group constraints that lead to
identification of the model are made.


The need for a new programme
--------------------------

Why develop a new collection of modules if software for structural equation
modelling is already available?

In each round of the ESS, there are approximately 20-26 countries. For each
country, four or five experiments were conducted, each of which contains two or
three split-ballot groups with each nine or twelve variables (depending on the
round). For each of these variables, there are several parameters, from which
two parameters of interest need to be computed. Furthermore, there are several
rounds, with a new round available every two years.

For each of the experiments in each round and country:

    #. The data for each split-ballot group need to be extracted and prepared for
       analysis;

    #. The model needs to be programmed, estimated, and adjusted to fit the data
       (currently LISREL and its syntax is used);

    #. The output (unstandardised parameter estimates and their
       variance-covariance matrix) needs to be written to files that can be read
       by another programme;

    #. The standardised estimates need to be computed from the unstandardised
       ones. For each question a reliability and a validity coefficient is
       computed;

    #. The variance-covariance matrix of these reliability and validity
       coefficients is needed for the further meta-analysis.

Finally, the reliability and validity coefficients, along with their
variance-covariance matrices and information about the round, country,
experiment, and question, need to be collected into a database to be used
for the meta-analysis.

These steps are laborious to do by hand. Although the process of model
formulation and adjustment cannot currently be automated, the other steps can
be, and this is why a new computer programme was needed. The programme saves time,
and also allows one to re-run the entire analysis if a new round of data becomes
available, or if new insights require that the models need to be adjusted.



How ``automtmm`` works
----------------------

``automtmm`` is not a single programme, but a suite of independently operating
modules.


Each of these modules performs or facilitates one of the five steps listed in
the previous section.

.. rubric:: Data preprocessing 

Preprocessing of the ESS data is done by a collection of ``R`` scripts that read in the
official ESS main and supplementary questions datafile, merge the two, recode
missing values, split the sample on country, experiment and split ballot groups, 
and write the result to a directory tree with different directories for
countries, and experiments. The output is different files containing the
covariances and means for each split-ballot group in each such directory.



The delta method [oehlert1992]_.


