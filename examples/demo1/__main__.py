from typing import List

import pygame
from pygame.font import Font
from pygame.mixer import Sound
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.time import Clock

from constants import Millis, Vec2, Vec3
from dialog import DialogComponent
from graph import DialogGraph, DialogNode, NodeGraphics, DialogChoice
from sound import SoundPlayer


def main():
    pygame.init()
    font = Font("examples/demo1/demo_font.dfont", 13)

    screen_size = (500, 500)
    picture_component_size = (500, 200)

    screen = pygame.display.set_mode(screen_size)

    images = {"demo1_background": filled_surface(picture_component_size, (0, 50, 35))}
    animations = {"demo1_animation": create_animation(picture_component_size)}
    sound_player = SoundPlayer(sounds={}, text_blip_sound=Sound("examples/demo1/text_blip.ogg"))

    dialog_graph = DialogGraph(
        root_node_id="ROOT",
        nodes=[
            DialogNode(
                node_id="ROOT",
                text="This is a minimal demo app. Let this text slowly appear OR click any key to skip it.",
                graphics=NodeGraphics(animation_id="demo1_animation"),
                choices=[DialogChoice("Click RETURN to restart!", "ROOT")])
        ],
        title="DEMO 1",
        background_image_id="demo1_background"
    )

    pygame.display.set_caption(dialog_graph.title)

    dialog_component = DialogComponent(
        surface=screen,
        dialog_font=font,
        choice_font=font,
        images=images,
        animations=animations,
        sound_player=sound_player,
        dialog_graph=dialog_graph,
        picture_size=picture_component_size
    )

    clock = Clock()

    while True:

        elapsed_time = Millis(clock.tick())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _exit_game()
            if event.type == pygame.KEYDOWN:
                dialog_component.on_skip_text_button()
                if event.key == pygame.K_RETURN:
                    dialog_component.on_action_button()

        dialog_component.update(elapsed_time)

        dialog_component.redraw()

        screen.blit(dialog_component.surface, (0, 0))

        fps_string = str(int(clock.get_fps())).rjust(3, ' ')
        rendered_fps = font.render(f"FPS: {fps_string}", True, (255, 255, 255), (0, 0, 0))
        screen.blit(rendered_fps, (5, 5))

        pygame.display.update()


def create_animation(size: Vec2) -> List[Surface]:
    frames = []
    for i in range(10):
        frame = Surface(size)
        pygame.draw.rect(frame, (0, 255, 255), Rect(30 + i * 10, 30 + i * 15, 70, 70))
        pygame.draw.rect(frame, (200, 100, 100), Rect(100, i * 5, 50, 50), width=4)
        pygame.draw.rect(frame, (200, 100, 100), Rect(200, 50 + i * 7, 60, 60), width=4)
        pygame.draw.rect(frame, (200, 100, 100), Rect(330, 100 + i * 9, 70, 70), width=4)
        frames.append(frame)
    return frames


def filled_surface(size: Vec2, color: Vec3):
    surface = Surface(size)
    surface.fill(color)
    return surface


def _exit_game():
    print("Exiting.")
    pygame.quit()
    exit(0)


if __name__ == '__main__':
    main()
