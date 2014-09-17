#!/usr/bin/env python

import sys
import os
import argparse
import glob

from ruffus import *
from genblastA_to_gff3 import genblastA_process

parser = argparse.ArgumentParser(description='Use Ruffus to process .out files from genblastA')
parser.add_argument('--input_pattern', '-I', default='.out')
parser.add_argument('--working_directory', '-W', default='.')
parser.add_argument('--num_threads', '-N', type=int, default=1)
args = parser.parse_args()

os.chdir(args.working_directory)
starting_files = glob.glob('*' + args.input_pattern)

def safe_open(filename, mode='r'):
	try:
		file_obj = open(filename, mode)
	except IOError as e:
		sys.stderr.write('Failed to open {}: {}'.format(filename, str(e)))
		sys.exit(1)
	return file_obj

@transform(starting_files, 
			suffix(args.input_pattern),
			'.genblastA.gff3')
def genblastA_to_gff3(input_file, output_file):
	in_file = safe_open(input_file)
	out_file = safe_open(output_file, 'w')
	genblastA_process(in_file, out_file, min_perc_coverage=80.0)

pipeline_run(multiprocess=args.num_threads)
