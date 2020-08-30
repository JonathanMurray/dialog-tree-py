from typing import List

import pygame
from pygame.font import Font
from pygame.mixer import Sound
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.time import Clock

from constants import Millis, Vec2, Vec3, BLACK, WHITE
from dialog import DialogComponent
from graph import DialogGraph, DialogNode, NodeGraphics, DialogChoice
from sound import SoundPlayer


def main():
    pygame.init()
    font = Font("examples/demo1/demo_font.dfont", 13)

    screen_size = (500, 500)
    dialog_margin = 30
    dialog_padding = 5
    outer_dialog_size = (screen_size[0] - dialog_margin * 2, 330)
    inner_dialog_size = (outer_dialog_size[0] - dialog_padding * 2, outer_dialog_size[1] - dialog_padding * 2)
    picture_component_size = (inner_dialog_size[0], 200)

    screen = pygame.display.set_mode(screen_size)
    dialog_surface = Surface(inner_dialog_size)

    images = {"demo1_background": filled_surface(picture_component_size, (0, 50, 35))}
    animations = {"demo1_animation": create_animation(picture_component_size)}
    blip_sound = Sound("examples/demo1/blip.ogg")
    select_blip_sound_id = "blip"
    sound_player = SoundPlayer(sounds={select_blip_sound_id: blip_sound}, text_blip_sound=blip_sound)

    dialog_graph = DialogGraph(
        root_node_id="ROOT",
        nodes=[
            DialogNode(
                node_id="ROOT",
                text="This is a minimal demo app. Let this text slowly appear or click any key to skip it. "
                     "Use the UP/DOWN keys to switch between your dialog choices, and click RETURN to go "
                     "for that choice.",
                graphics=NodeGraphics(animation_id="demo1_animation"),
                choices=[DialogChoice("See this dialog again", "ROOT"), DialogChoice("Close dialog", "DIALOG_CLOSED")]),
            DialogNode(
                node_id="DIALOG_CLOSED",
                text="",
                graphics=NodeGraphics(animation_id="demo1_animation"),
                choices=[]),

        ],
        title="DEMO 1",
        background_image_id="demo1_background"
    )

    pygame.display.set_caption(dialog_graph.title)

    dialog_component = DialogComponent(
        surface=dialog_surface,
        dialog_font=font,
        choice_font=font,
        images=images,
        animations=animations,
        sound_player=sound_player,
        dialog_graph=dialog_graph,
        picture_size=picture_component_size,
        select_blip_sound_id=select_blip_sound_id
    )

    clock = Clock()

    is_dialog_shown = True

    while True:

        elapsed_time = Millis(clock.tick())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _exit_game()
            if event.type == pygame.KEYDOWN:
                if is_dialog_shown:
                    dialog_component.on_skip_text_button()
                    if event.key == pygame.K_RETURN:
                        dialog_component.on_action_button()
                        if dialog_component.current_node_id() == "DIALOG_CLOSED":
                            is_dialog_shown = False
                    elif event.key == pygame.K_DOWN:
                        dialog_component.on_delta_button(1)
                    elif event.key == pygame.K_UP:
                        dialog_component.on_delta_button(-1)

        if is_dialog_shown:
            dialog_component.update(elapsed_time)
            dialog_component.redraw()

        screen.fill(BLACK)
        if is_dialog_shown:
            screen.blit(dialog_component.surface, (dialog_margin + dialog_padding, dialog_margin + dialog_padding))
        pygame.draw.rect(screen, (255, 100, 100), Rect((dialog_margin, dialog_margin), outer_dialog_size), width=1)

        fps_string = str(int(clock.get_fps())).rjust(3, ' ')
        rendered_fps = font.render(f"FPS: {fps_string}", True, WHITE, (0, 0, 0))
        screen.blit(rendered_fps, (5, 5))

        screen.blit(font.render("The dialog library is confined to the red rectangle above.", True, WHITE), (15, 400))
        screen.blit(font.render("This text is handled separately from the dialog.", True, WHITE), (15, 430))
        if not is_dialog_shown:
            screen.blit(font.render("Oops, you closed the dialog. Restart app to see it again.", True, (255, 150, 150)),
                        (15, 460))

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
