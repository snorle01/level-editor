from engine.engine import engine_class
from scenes.test_scene import test_scene

import pygame, sys
engine = engine_class(test_scene)

while True:
    for event in pygame.event.get():

        engine.scene.event(event)

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # destroy
            engine.destroy()
            pygame.quit()
            sys.exit()

    # update
    engine.scene.update()

    # draw
    engine.ctx.clear(color=engine.clear_color)

    engine.scene.render()

    pygame.display.flip()
    engine.clock.tick(60)