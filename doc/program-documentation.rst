Documentation
=============

.. toctree::
   :maxdepth: 2

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



LISREL input and output processing
----------------------------------

Module that reads and interprets LISREL input and output files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: parse_lisrel
    :members:

.. autoclass:: LisrelInput
    :members:


Module that calculates analytical derivatives of the standardized coefficients with respect to the free parameters of the model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: read_maxima
    :members:

Module that runs the LISREL input files and gathers the results
---------------------------------------------------------------

.. automodule:: walk_and_run
    :members:
