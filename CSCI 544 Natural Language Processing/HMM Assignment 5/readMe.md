Overview

In this assignment you will write a Hidden Markov Model part-of-speech tagger for Catalan. The training data is provided tokenized and tagged; the test data will be provided tokenized, and your tagger will add the tags. The assignment will be graded based on the performance of your tagger, that is how well it performs on unseen test data compared to the performance of a reference tagger.

Data

A set of training and development data will be made available as a compressed ZIP archive on Blackboard. The uncompressed archive will have the following format:

A file with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.
A file with untagged development data, with words separated by spaces and each sentence on a new line.
A file with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.
A readme/license file (which you won’t need for the exercise).
The grading script will train your model on all of the tagged training and development data, and test the model on unseen data in a similar format.

Programs

You will write two programs: hmmlearn.py will learn a hidden Markov model from the training data, and hmmdecode.py will use the model to tag new data. If using Python 3, you will name your programs hmmlearn3.py and hmmdecode3.py. The learning program will be invoked in the following way:

> python hmmlearn.py /path/to/input

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt. The format of the model is up to you, but it should contain sufficient information for hmmdecode.py to successfully tag new data.

The tagging program will be invoked in the following way:

> python hmmdecode.py /path/to/input

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.
