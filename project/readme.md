# EBS Homework

A program (written in Python) that generates random sets of subscriptions and publications that has the following features:
- choosing the total number of messages, as well as the message type (publication/subscription) at the command line
- fixed frequency procents for the fields that can be changed at ```data.json```
- every field has a frequency procent for the '=' operator, again, this can be changed at ```data.json```
- parallel execution: a threading feature that generates simultaneously publications and subscriptions
- execution of generating either publications or subscriptions, without using the threading feature

# Results
## Processor details
OS Name: Microsoft Windows 10 Education

Processor:	Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz   2.59 GHz

Device ID:	587407AC-EBBA-4AE3-AAA9-4D124CEA5CDF

Product ID:	00328-00095-24679-AA482

System type: 64-bit operating system, x64-based processor

Installed RAM:	8.00 GB

Total Physical Memory:	7.89 GB

Available Physical Memory:	1.27 GB

Total Virtual Memory:	16.3 GB

Available Virtual Memory:	3.45 GB

## Tests with a single thread

One thread generated 10000 publications in an execution time of 3.8786258697509766 seconds and 10000 subscriptions in 1.8399782180786133 seconds.

## Tests with multiple threads operating only a single type of set

5 threads generated each 100000 publications in 18.51911449432373 seconds, while the same 5 threads can generate 10000 subscriptions in 9.051119089126587 seconds.

## Tests with multiple threads operating both publications and subscriptions

In this case we have, as an example, 2 threads that generate publications and other 3 that generate subscriptions, each of them in 10000 exemplaries. The execution of these threads can be done in cca. 7 seconds.

## Commands

        To generate a specific number of pubs/subs:
        py publish.py -n 500
        py subscribe.py -n 500

        To generate pubs/subs with a single thread:
        py parallelworks.py -t 1 -s p -n 100000
        py parallelworks.py -t 1 -s s -n 100000

        To generate only pubs/only subs/both with multiple threads:
        py parallelworks.py -t 5 -s p -n 100000
        py parallelworks.py -t 5 -s s -n 100000
        py parallelworks.py -t 5 -s b -n 100000