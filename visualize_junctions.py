import argparse
import pandas as pd
import sys
import subprocess
import math
import os

def generate_plot(r, input_bams_tsv, chrom_header, start_header, stop_header, annotation_header, max_charts_per_page):
    """Generate a sashimi plot for this site. If there is an annotation column use this in the file name
    and folder scheme"""

    chrom = r[chrom_header]
    start = r[start_header]
    stop = r[stop_header]
    if annotation_header:
        annotation = '{}-'.format(r[annotation_header])
    else:
        annotation = ''

    label = '{}{}-{}-{}'.format(annotation, chrom, start, stop)
    sys.stdout.write("Looking at {}\n".format(label))

    new_tsv_paths = []
    with open(input_bams_tsv, 'r') as f:
        tsv_lines = f.readlines()
        num_files = int(math.ceil(len(tsv_lines)/float(max_charts_per_page)))
        sys.stdout.write("Maximum of {} charts per PDF...\n".format(max_charts_per_page))
        sys.stdout.write("Splitting {} lines into {} files\n".format(len(tsv_lines), num_files))
        for i in range(0, num_files):
            subfile_name = '{}/input_bams_{}.tsv'.format(os.path.dirname(input_bams_tsv), i)
            if subfile_name.startswith('/input_bams'):
                subfile_name = subfile_name[1:]
            with open(subfile_name, 'w') as fragment:
                for j in range(i*max_charts_per_page, (i+1)*max_charts_per_page):
                    if j < len(tsv_lines):
                        fragment.write(tsv_lines[j])
            new_tsv_paths.append(subfile_name)

    index = 0
    for subfile_path in new_tsv_paths:
        sys.stdout.write('\tGenerating plots for {}\n'.format(subfile_path))
        command = 'python /sashimi-plot.py -b {} -c {}:{}-{} ' \
                  ' -M 5 --shrink --alpha 0.6 --base-size=6 ' \
                  '--ann-height=2 --height=3 --width=4 -P palette.txt -o {}_{}'.format(subfile_path,
                                                                                    chrom, int(start)-10, int(stop)+10,
                                                                                    label, index)

        try:
            subprocess.call(command.split())
        except:
            sys.stdout.write("Couldn't view region {} because of some error".format(label))
        index += 1


def main(args):
    junctions = args.junctions
    annotation_header = args.annotation_header
    chrom_header = args.chrom_header
    start_header = args.start_header
    stop_header = args.stop_header
    input_bams_tsv = args.input_bams_tsv
    max_charts = args.max_charts

    if annotation_header.strip() == 'None':
        annotation_header = None

    junctions_df = pd.read_csv(junctions, sep='\t', header='infer')

    junctions_df.apply(generate_plot, axis=1, args=(input_bams_tsv, chrom_header, start_header, stop_header, annotation_header, max_charts))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Filter normalized splice junctions file''')
    parser.add_argument('-input_bams_tsv', type=str)
    parser.add_argument('-junctions', help='tab separated list of junctions, each junction on a different line', type=str)
    parser.add_argument('-annotation_header', type=str, default='Gene')
    parser.add_argument('-chrom_header', type=str, default='Chrom')
    parser.add_argument('-start_header', type=str, default='Start')
    parser.add_argument('-stop_header', type=str, default='End')
    parser.add_argument('-max_charts', type=int, default=5)

    args = parser.parse_args()
    main(args)
