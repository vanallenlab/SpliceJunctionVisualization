workflow splicejunctionvisualization {
	Array[File] starAlignedBams
    Array[File] bamIndexFiles
    Array[String] sampleIds
    Int diskSpace
    String memory
    File spliceJunctionsFile
    String annotationsHeader_or_None="Gene"
    String chromHeader="Chrom"
    String startHeader="Start"
    String stopHeader="End"

    call RunSpliceJunctionVisualizationTask {
    	input:
        	starAlignedBams=starAlignedBams,
            bamIndexFiles=bamIndexFiles,
            sampleIds=sampleIds,
        	diskSpace=diskSpace,
            memory=memory,
            spliceJunctionsFile=spliceJunctionsFile,
            annotationsHeader_or_None=annotationsHeader_or_None,
            chromHeader=chromHeader,
            startHeader=startHeader,
            stopHeader=stopHeader
    }

    output {
    	RunSpliceJunctionVisualizationTask.snapshots
    }
}

task RunSpliceJunctionVisualizationTask {
	Array[File] starAlignedBams
    Array[File] bamIndexFiles
    Array[String] sampleIds
    Int diskSpace
    String memory
    File spliceJunctionsFile
    String annotationsHeader_or_None
    String chromHeader
    String startHeader
    String stopHeader

    command <<<
    	echo "Current directory and contents:"
        pwd
        ls -lh

        mv ${sep = ' ' starAlignedBams} .
        mv ${sep = ' ' bamIndexFiles} .

        touch sample_ids.txt
        for i in ${sep = ' ' sampleIds}; do
            echo $i | tr -d '-' >> sample_ids.txt
        done


        echo "Sample IDs are:"
        cat sample_ids.txt

        # Make list of samples -- first column will be sample label and second will be sample path.
        ls *.bam > bam_list.txt
        paste -d "\t" sample_ids.txt bam_list.txt > input_bams.tsv

        echo ".bam list is:"
        cat bam_list.txt

        echo "input_bams.tsv is"
        cat input_bams.tsv

        cp /palette.txt .
        cp /sashimi-plot.py .
        echo "copied palette.txt to here... checking:"
        ls -lh

    	python /visualize_junctions.py -input_bams_tsv input_bams.tsv -junctions ${spliceJunctionsFile} -annotation_header ${annotationsHeader_or_None} -chrom_header ${chromHeader} -start_header ${startHeader} -stop_header ${stopHeader}

        mkdir snapshots
        mv *.pdf snapshots

		echo "Snapshots generated:"
        ls -lh snapshots

        echo "Taring snapshots folder"
        tar -zcvf snapshots.gz snapshots

        echo "Finally dir status:"
        ls -lh
    >>>

    output {
    	File snapshots="snapshots.gz"
    }

    runtime {
    	docker: "vanallenlab/ggsashimi_adapted:1.0"
        memory: "${memory}"
        disks: "local-disk ${diskSpace} HDD"
        bootDiskSizeGb: 10
        preemptible: 5
    }
}
