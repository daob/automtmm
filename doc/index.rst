.. automtmm documentation master file, created by sphinx-quickstart on Tue May  5 16:34:54 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Automtmm Documentation
======================

.. toctree::
   :maxdepth: 2
    
   goals-and-background
   program-documentation
   bibliography

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

The document consists of two chapters. The first chapter explains the goals
and the background of the program, as well as its workings in a manner meant for
a broad audience. The second chapter, *Documentation*, documents the Python
and R modules, classes, and functions that make up the program. It is intended
as reference material for those who want to use or change the program.
