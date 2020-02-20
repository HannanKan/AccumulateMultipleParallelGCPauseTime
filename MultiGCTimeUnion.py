#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta

## input: gc file with command " -XX:+PrintGCDetails -XX:+PrintGCDateStamps"
## file: gc log with above command
## returnee: list of tuples, tuple[0] is start, tuple[1] is end. type(tuple) is datetime
def get_gc_intervals_from_file(file):
    f1=open(file)
    # time: 2020-02-19T00:19:41.434 +0800
    # log: 2020-02-19T00:19:41.434+0800: [GC (Metadata GC Threshold) [PSYoungGen: 278161K->18420K(600576K)] 278161K->18500K(1972736K), 0.0301441 secs] [Times: user=0.62 sys=0.04, real=0.03 secs] 
    gc_interval_1=[]
    for line in f1:
        if line.strip()=="Heap":
            break
        ## parse start time
        t=line[0:line.index("[")]
        (h,m,s)=[int(ele) for ele in t[t.index("T")+1:t.index(".")].split(":")]
        ms=t[t.index(".")+1:t.index("+")]
        ms=int(ms+(6-len(ms))*"0")
        (yy,mm,dd)=[int(x) for x in line[0:line.index("T")].split("-")]
        start=datetime(yy,mm,dd,h,m,s,ms)

        ## parse pause
        duration_ms=int(float(line[line.index("real")+5:line.rfind("secs")])*1000000)
        duration_ms=timedelta(microseconds=duration_ms)
        gc_interval_1.append((start,start+duration_ms))
    print("print parsing interval of file: "+file)
    for x in gc_interval_1:
        print(x[0],x[1])
    return gc_interval_1

## judge whether two tuple is intersected or not
## prerequisite: tuple1[0]<tuple2[0]
def interval_is_intersected(tuple1,tuple2):
    if tuple1[0]> tuple2[0]:# or tuple1[0]==tuple2[0]:
        print("call this function inproperly!")
        exit(1)
    if tuple2[0]<tuple1[1] or tuple2[0]==tuple1[1]:
        return True
    else:
        return False

def takeFirst(elem):
    return elem[0]

## merge two given interval list, resulting in no intersection
## pass two tuple list
## returnee: one tuple list without intersection between intervals in this list 
def merge2gc_intervals(l1,l2):
    ## merge two lists and sort by first element
    l_merge=l1+l2
    l_merge.sort(key=takeFirst)
    i=0
    while i < len(l_merge):
        if i==0:
            i=i+1
            continue
        else:
            cur=l_merge[i]
            pre=l_merge[i-1]
        is_intersected=interval_is_intersected(pre,cur)
        if is_intersected:
            ##merge
            ## contain
            if (pre[1]>cur[1] or pre[1]==cur[1]) :
                l_merge.remove(cur)
            else:##intersected
                item_inserted=(pre[0],cur[1])
                l_merge.insert(i-1,item_inserted)
                del(l_merge[i:i+2])
        else: #do not intersected
            i=i+1
    return l_merge

## prerequisite: pass list with intervals,which do not intersect with each other
##returnee: accumulative time from intervals
def accumulate_intervals(intervals):
    acc=timedelta() ##initial with 0
    for i,e in enumerate(intervals):
        dur=e[1]-e[0]
        acc=acc+dur
        #print("after adding interval "+str(i+1)+" result is",acc)
    return acc

file_index=['0','1','2']
interval=[]
for i in file_index:
    ##tmp=get_gc_intervals_from_file("stdout-"+i)
    tmp=get_gc_intervals_from_file("./"+i+"/stdout")
    interval=merge2gc_intervals(interval,tmp)


import sys

sys.stdout.write("wall clock time of multiple gc is ")
print(accumulate_intervals(interval))

sys.stdout.write("i.e. ")
sys.stdout.write(str(accumulate_intervals(interval).total_seconds()))
print(" seconds")






