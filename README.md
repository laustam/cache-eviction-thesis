# Cache eviction algorithms

## Overview

> This repository contains the source code and written report for my bachelor thesis titled [INSERT TITLE HERE].

## Repository Structure

Notable files and directories are outlined here:

```
├── report/                         # LaTeX source of the thesis report
├── code/                           # Code used for the thesis experiment, using the libCacheSim code as a base
|   ├── data/                       # Workloads used in the experiment are stored here
|   |    
|   ├── scripts/
|   |   ├── gen_zipf_worklaod.py    # Script to generate a workload following a Zipf-like distribution. Result is stored in code/data
|   |   └── ...
|   ├── libCacheSim/
|   |   ├── bin/
|   |   |   ├── cachesim/
|   |   |   |   ├── cache_init.h    # Code for cache initialisation
|   |   |   |   └── ...
|   |   |   └── ...
|   |   ├── cache/
|   |   |   ├── eviction/           # Contains my implementations for different eviction algorithms
|   |   |   |   ├── myFIFO.c
|   |   |   |   ├── myFIFO.h
|   |   |   |   ├── myHelpers.h
|   |   |   |   ├── myLRU.c
|   |   |   |   ├── myLRU.h
|   |   |   |   ├── mySieve.c
|   |   |   |   ├── mySieve.h
|   |   |   |   └── ...
|   |   |   └── ...
|   |   └── ...
|   └── ...
├── README.md
└── .gitignore
```
