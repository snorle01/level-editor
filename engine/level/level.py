import pygame
from typing import List

class level_class:
    def __init__(self, size:tuple[int, int], floor_dir:str, wall_dir:str, ceiling_dir:str):
        self.size = size
        # get data from image
        def get_data(surface:pygame.Surface):
            data = []
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    if surface.get_at((x, y)) == (255, 255, 255):
                        data.append(1)
                    else:
                        data.append(0)
            return data
        
        surface_floor = pygame.image.load(floor_dir).convert()
        self.floor = get_data(surface_floor)

        surface_wall = pygame.image.load(wall_dir)
        self.wall = get_data(surface_wall)

        surface_ceiling = pygame.image.load(ceiling_dir)
        self.ceiling = get_data(surface_ceiling)

    def index_to_X(self, index: int) -> int:
        return index % self.size[0]

    def index_to_Y(self, index: int) -> int:
        return index // self.size[0]

    def index_to_XY(self, index: int) -> tuple[int, int]:
        return (self.index_to_X(index), self.index_to_Y(index))

    # the position tule must contain int's or it will return an float value
    def XY_to_index(self, position:tuple[int, int]) -> int:
        return position[0] + (position[1] * self.size[0])
    
    def path_to(self, start_pos:tuple[int, int], end_pos:tuple[int, int]):

        class pending_pos:
            def __init__(self, pos:tuple[int, int], direction:str):
                self.pos = pos
                self.direction = direction
        
        path_dict = {}
        pending_positions = [pending_pos(end_pos, None)]

        def is_pos_valid(pos:tuple[int, int]):
            # if pos has allready been proseced
            if pos in path_dict:
                return False
            
            # outside X
            if pos[0] < 0 or pos[0] > self.size[0] - 1:
                return False
            # outside Y
            if pos[1] < 0 or pos[1] > self.size[1] - 1:
                return False
            
            # if pos is a wall
            if self.wall[self.XY_to_index(pos)] == 1:
                return False
            
            return True

        while len(pending_positions) > 0:
            pos_class = pending_positions[0]

            if is_pos_valid(pos_class.pos):
                path_dict[pos_class.pos] = pos_class.direction

                pending_positions.append(pending_pos((pos_class.pos[0] + 1, pos_class.pos[1]), "left"))
                pending_positions.append(pending_pos((pos_class.pos[0] - 1, pos_class.pos[1]), "right"))
                pending_positions.append(pending_pos((pos_class.pos[0], pos_class.pos[1] + 1), "up"))
                pending_positions.append(pending_pos((pos_class.pos[0], pos_class.pos[1] - 1), "down"))

            pending_positions.pop(0)

            if pos_class.pos == start_pos:
                break

        return path_dict