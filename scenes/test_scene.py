import glm, pygame, json
from engine.scene import base_scene
from models.square_model import square_frame_model, square_model
from models.text_model import text_model
from typing import List

class test_scene(base_scene):
    def __init__(self, engine):
        super().__init__(engine)

        self.floor_text = text_model(self.engine, "floor", (-1, 0.9, 0), (0.1, 0.1, 1))
        self.wall_text = text_model(self.engine, "wall", (-1, 0.9, 0), (0.1, 0.1, 1))
        self.ceiling_text = text_model(self.engine, "ceiling", (-1, 0.9, 0), (0.1, 0.1, 1))
        self.text_layer = [self.floor_text, self.wall_text, self.ceiling_text]

        self.grid = (10, 10)
        
        squares_floors: List[square_model] = []
        self.create_squares(squares_floors)
        squares_walls: List[square_model] = []
        self.create_squares(squares_walls)
        squares_ceiling: List[square_model] = []
        self.create_squares(squares_ceiling)

        values_floor: List[int] = []
        self.create_values(values_floor)
        values_walls: List[int] = []
        self.create_values(values_walls)
        values_ceiling: List[int] = []
        self.create_values(values_ceiling)
        
        self.layer_index = 0
        self.squares_layers = [squares_floors, squares_walls, squares_ceiling]
        self.values_layers = [values_floor, values_walls, values_ceiling]

    def create_values(self, value_list: List[int]):
        for i in range(self.grid[0] * self.grid[1]):
            value_list.append(0)

    def create_squares(self, squares_list: List[square_model]):
        screen_width = pygame.display.get_window_size()[0]
        screen_height = pygame.display.get_window_size()[1]

        square_width = (2 * (screen_height / screen_width)) / self.grid[0]
        square_height = 2 / self.grid[1]

        square_y = -1
        for yi in range(self.grid[1]):
            square_x = -1
            for xi in range(self.grid[0]):
                squares_list.append(square_model(self.engine, (square_x, square_y, 0), (square_width, square_height, 1)))
                self.add_object(square_frame_model(self.engine, (square_x, square_y, 0), (square_width, square_height, 1), glm.vec3(0.0, 0.0, 0.0)))
                square_x += square_width
            
            square_y += square_height

    def event(self, event:pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            screen_width = pygame.display.get_window_size()[0]
            screen_height = pygame.display.get_window_size()[1]

            if mouse_pos[0] <= screen_height:
                on_color = glm.vec3(0.0, 1.0, 0.0)
                off_color = glm.vec3(1.0, 0.0, 0.0)

                x = int(mouse_pos[0] // (screen_height / self.grid[0]))
                fliped_y = int(mouse_pos[1] // (screen_height / self.grid[1]))
                y = (self.grid[1] - 1) - fliped_y
                index = x + (y * self.grid[0])

                if self.values_layers[self.layer_index][index] == 0:
                    self.values_layers[self.layer_index][index] = 1
                    self.squares_layers[self.layer_index][index].color = on_color
                else:
                    self.values_layers[self.layer_index][index] = 0
                    self.squares_layers[self.layer_index][index].color = off_color

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # up
                self.layer_index += 1
                if self.layer_index > 2:
                    self.layer_index = 0

            if event.key == pygame.K_DOWN: # DOWN
                self.layer_index -= 1
                if self.layer_index < 0:
                    self.layer_index = 2

            if event.key == pygame.K_s: # save
                dictionary = {
                    "size": self.grid,
                    "floors": self.values_layers[0],
                    "walls": self.values_layers[1],
                    "ceiling": self.values_layers[2]
                }

                with open("level_data.json", "w") as f:
                    json.dump(dictionary, f, indent=4)

                # """ old code. unable to modify existing file
                # Serializing json
                json_object = json.dumps(dictionary, indent=4)

                # Writing to sample.json
                with open("level_data.json", "w") as outfile:
                    outfile.write(json_object)
                # """
                
            if event.key == pygame.K_l: # load
                on_color = glm.vec3(0.0, 1.0, 0.0)
                off_color = glm.vec3(1.0, 0.0, 0.0)

                with open('level_data.json', 'r') as file:
                    data = json.load(file)

                    self.values_layers[0] = data["floors"]
                    self.values_layers[1] = data["walls"]
                    self.values_layers[2] = data["ceiling"]

                    for list_index in range(len(self.values_layers)):
                        for index in range(self.grid[0] * self.grid[1]):
                            if self.values_layers[list_index][index] == 0:
                                self.squares_layers[list_index][index].color = off_color
                            else:
                                self.squares_layers[list_index][index].color = on_color

    def render(self):
        super().render()

        self.text_layer[self.layer_index].render()

        for square in self.squares_layers[self.layer_index]:
            square.render()