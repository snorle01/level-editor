import math

# returns the distance between two positions in 2D
def distance_between(position_0:tuple[int,int], position_1:tuple[int,int]) -> float:
        lenght_x = position_0[0] - position_1[0]
        lenght_y = position_0[1] - position_1[1]
        return math.sqrt(lenght_x*lenght_x + lenght_y*lenght_y)