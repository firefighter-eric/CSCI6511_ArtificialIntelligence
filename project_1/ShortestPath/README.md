# Shortest Path

## Introduction of the project

The program is in the file shortestpath.py.

~/shortestpath.py ~/graphs/e.txt    ~/graphs/v.txt  should be but before execution.

For example

```
Project ----- shortest.py.py
      |
      | ------ graphs ------- v.txt
                 |
                 | ------- e.txt
```

Numpy and Pandas should be prepared in the python3 environment.
In the bash, input “python3 shortest.py.py”, then there will be the result.

## Performance comparison

A* Algorithm is faster than the Dijkstra Algorithm about 2 times.

Dijkstra always outputs optimal path. Sometimes A\* Algorithm doesn’t output the optimal path, because h doesn’t strictly less than h\* in this program. In small graph, such as the 100 vertices graph, the accuracy is closely 100% in A\*.
