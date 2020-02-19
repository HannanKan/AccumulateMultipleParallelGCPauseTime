# AccumulateMultipleParallelGCPauseTime
This repository hold utility which is used to accumulate multiple parallel Java garbage collection pause time in distributed Spark.

## Requirement
to use this utility, you have to set following gc log printint option running Java program
```shell
-XX:+PrintGCDetails -XX:+PrintGCDateStamps
```
## File
```shell
stdout-1
stdout-2
stdout-3
```
is gc log file used as test case.

## Usage
```shell
python MultiGCTimeUnion.py 
```
