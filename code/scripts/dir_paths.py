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
├── tables/                     # TABLES DIR
└── ...
"""

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.dirname(SCRIPTS_DIR)
BASE_DIR = os.path.dirname(CODE_DIR)
DATA_DIR = os.path.join(CODE_DIR, 'data')
RESULTS_DIR = os.path.join(CODE_DIR, 'results')
PROCESSED_DATA_DIR = os.path.join(CODE_DIR, 'processed_data')
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')
TABLES_DIR = os.path.join(BASE_DIR, 'tables')
FIGURES_WORKLOADS_DIR = os.path.join(FIGURES_DIR, 'workloads')
FIGURES_SIMULATIONS_DIR = os.path.join(FIGURES_DIR, 'simulations')


CACHESIM_PATH = os.path.join(CODE_DIR, '_build', 'bin', 'cachesim')
WORKLOADS_PKL_PATH = os.path.join(PROCESSED_DATA_DIR, 'data_df.pkl')
RESULTS_PKL_PATH = os.path.join(PROCESSED_DATA_DIR, 'results_df.pkl')
