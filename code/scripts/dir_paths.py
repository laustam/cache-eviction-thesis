import os

"""
# DIRECTORY SETUP:

├── code/                       # PARENT_DIR
|   ├── bin/
|   |   ├── bin/
|   |   |   ├── cachesim        # CACHESIM_PATH
|   |   |   └── ...
|   ├── data/                   # DATA_DIR
|   ├── scripts/                # SCRIPTS_DIR
|   ├── results/                # RESULTS DIR
|   └── ...
├── figures/                    # FIGURES_DIR
└── ...
"""

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.dirname(SCRIPTS_DIR)
BASE_DIR = os.path.dirname(CODE_DIR)
DATA_DIR = os.path.join(CODE_DIR, 'data')
RESULTS_DIR = os.path.join(CODE_DIR, 'results')
CACHESIM_PATH = os.path.join(CODE_DIR, '_build', 'bin', 'cachesim')
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')
