#!/bin/bash
path_to_millionaire=$(readlink -f ../millionaire/runner.py)
python3 "$path_to_millionaire"
