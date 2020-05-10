# CSCI561_SearchAlgorithms

Python code to perform Breadth First Search, Uniform Cost Search, and A* search on a matrix of data to help a mars rover move over a terrain.
Through this search, a minimum cost path is found from the source index to the destination index. 

## Constraints

Movement of the rover from on cell to another cell is possible if the difference in values ( Height/ z-index) of the cells is less than the minimum height that the rover can climb.
This minimum height is mentioned in the input file. 

The input file also mentions the type of search to be performed. 

## Output

The output of the code is the path from source to destination if there exist one or FAIL if there is no path. 
