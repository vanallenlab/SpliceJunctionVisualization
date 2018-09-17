# SpliceJunctionVisualizer

FireCloud-ready script for high-throughput visualization of sashimi splots for a list of splice junction coordinates.
This implementation uses the ggsashimi visualization library created by Emilio Palumbo <emilio.palumbo@crg.eu>.

## Docker Image <a name="docker_build"></a>

The FireCloud-ready docker image can be constructed by navigating to the SpliceJunctionVisualizer folder and running
the following command, which adds ggsashimi, R, samtools, Python, and the visualization_junctions.py script itself to
the docker image:

```
docker build -f ggsashimi/docker/Dockerfile -t vanallenlab/ggsashimi_adapted:1.0 .
```