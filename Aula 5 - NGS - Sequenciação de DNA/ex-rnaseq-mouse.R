BiocManager::install(c("Rsubread"))
library(Rsubread)

##### PART 1 - ALIGNMENT AND COUNTING ##### (may be skipped)

fastq.files <- list.files(path = "./Mouse-rnaseq-data/data", pattern = ".fastq.gz$", full.names = TRUE)
fastq.files

# building index
buildindex(basename="./Mouse-rnaseq-data/chr1_mm10",reference="./Mouse-rnaseq-data/chr1.fa")

# alignment
align(index="./Mouse-rnaseq-data/chr1_mm10",readfile1=fastq.files)

bam.files <- list.files(path = "./Mouse-rnaseq-data/data", pattern = ".BAM$", full.names = TRUE)
bam.files

props <- propmapped(files=bam.files)
props

# QC
qs <- qualityScores(filename="./Mouse-rnaseq-data/data/SRR1552450.fastq.gz",nreads=100)
dim(qs)
head(qs)
boxplot(qs)

fc <- featureCounts(bam.files, annot.inbuilt="mm10")
names(fc)
fc$stat
dim(fc$counts)
head(fc$counts)
head(fc$annotation)

