# SpliceJunctionVisualizer

FireCloud-ready script (method at ekofman/splice_junction_visualization) for high-throughput visualization of sashimi
splots for a list of splice junction coordinates. This implementation uses the ggsashimi visualization library created
by Emilio Palumbo <emilio.palumbo@crg.eu>.

## Docker Image <a name="docker_build"></a>

The FireCloud-ready docker image can be constructed from the top level of this repository by running
the following command, which adds ggsashimi, R, samtools, Python, and the visualization_junctions.py script itself to
the docker image:

```
docker build -f ggsashimi/docker/Dockerfile -t vanallenlab/ggsashimi_adapted:0.0 .
```


## Usage <a name="usage"></a>
```
python /visualize_junctions.py -input_bams_tsv input_bams.tsv -junctions splice_junctions.tsv
```

Input to -junctions is expected to be a tab-separated file containing columns for chromosome (default header title
"Chrom"), splice junction start position (default header title "Start"), and splice junction end position (default
header title "End"). By default the presence of a 4th column, "Gene", is assumed, but this can be overriden by providing
"None" for the -annotation_header argument to the script. "Chrom," "Start," and "End" as column headers can also be
overriden by providing desired alternative headers via the -chrom_header, -start_header and -stop_header arguments,
respectively.

## Output <a name="output"></a>

Output is one PDF image for each splice junction, containing sashimi plots for each sample.

## Example <a name="output"></a>

You can test the script using the examples in the "examples" folder in an interactive session of the docker image.

From the top level of this repository:
```
docker run -it -w $PWD -v $PWD:$PWD vanallenlab/ggsashimi_adapted:0.0
```

Once in the interactive docker session:
```
python visualize_junctions.py -junctions examples/sample_sites.tsv -input_bams_tsv examples/input_bams_two_cols.tsv
```
