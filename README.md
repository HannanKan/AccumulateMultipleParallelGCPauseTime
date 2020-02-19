# AccumulateMultipleParallelGCPauseTime
This repository hold utility which is used to accumulate multiple parallel Java garbage collection pause time in distributed Spark.

## Scenario
Multiple JVMs run in parallel from a certain point $s$ to $e$. During time interval\[$s$,$e$], gc time interval in different JVMs may overlap or not. If you want to compute wall time used by gc in all JVMs during \[$s$,$e$], this is for you!
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
## Development Plan
visualizing one JVM gc time in one axis while multiple JVM gc time sharing same time scale just like this<br>
jvm 1 gc|----    ----    ---- <br>
jvm 1 gc|   -----    -----    <br>
jvm 1 gc|  ---   ---   -----   --- <br>
----------------------------------------> time
