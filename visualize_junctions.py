import argparse
import pandas as pd
import sys
import subprocess


def generate_plot(r, input_bams_tsv, chrom_header, start_header, stop_header, annotation_header):
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

    command = 'python ggsashimi/sashimi-plot.py -b {} -c {}:{}-{} ' \
              ' -M 5 --shrink --alpha 0.6 --base-size=6 ' \
              '--ann-height=2 --height=3 --width=4 -P palette.txt -o {}'.format(input_bams_tsv,
                                                                                chrom, int(start)-10, int(stop)+10,
                                                                                label)

    try:
        subprocess.call(command.split())
    except:
        sys.stdout.write("Couldn't view region {} because of some error".format(label))


def main(args):
    junctions = args.junctions
    annotation_header = args.annotation_header
    chrom_header = args.chrom_header
    start_header = args.start_header
    stop_header = args.stop_header
    input_bams_tsv = args.input_bams_tsv

    if annotation_header.strip() == 'None':
        annotation_header = None

    junctions_df = pd.read_csv(junctions, sep='\t', header='infer')

    junctions_df.apply(generate_plot, axis=1, args=(input_bams_tsv, chrom_header, start_header, stop_header, annotation_header))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Filter normalized splice junctions file''')
    parser.add_argument('-input_bams_tsv', type=str)
    parser.add_argument('-junctions', help='tab separated list of junctions, each junction on a different line', type=str)
    parser.add_argument('-annotation_header', type=str, default='Gene')
    parser.add_argument('-chrom_header', type=str, default='Chrom')
    parser.add_argument('-start_header', type=str, default='Start')
    parser.add_argument('-stop_header', type=str, default='End')

    args = parser.parse_args()
    main(args)
