import os
import random
import arcade

SPRITE_NATIVE_SIZE = 128
SPRITE_SCALING = 0.5
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TITLE = "Vampyre Chase"  # Python games MUST HAVE PY HAHHAHA

# Viewport margins
VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150

# Game physics
GRAVITY = 0.5
MOVEMENT_SPEED = 5
JUMP_SPEED = 15


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", SPRITE_SCALING)

        self.jumping = False


class Game(arcade.Window):
    def __init__(self, curr_dir: str):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)

        # Change to directory where the files are stored, this will help with PyInstaller later (hopefully)
        os.chdir(curr_dir)

        self.player_sprite = None

        # Sprite lists
        self.platforms_list = None
        self.player_list = None
        self.enemy_list = None
        self.vampire_list = None
        self.gems_list = None

        # Pressed keys
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Cameras
        self.camera = None
        self.camera_gui = None

        # How far the vampire is from the character. He starts on the left part of the screen
        self.vampire_close = 0

        # Score
        self.score = 0

        # Physics
        self.physics_engine = None

    def setup(self):
        self.platforms_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.vampire_list = arcade.SpriteList()
        self.gems_list = arcade.SpriteList()

        # I need to draw platforms as the player moves, need to figure out how to do it
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            platform = arcade.Sprite(":resources:images/tiles/stoneMid.png", SPRITE_SCALING)

            platform.bottom = 0
            platform.left = x
            self.platforms_list.append(platform)

        vampire = arcade.Sprite(":resources:images/animated_characters/zombie/zombie_idle.png", 4)
        vampire.bottom = SPRITE_SIZE
        vampire.left = 0
        self.vampire_list.append(vampire)

        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.platforms_list,
            gravity_constant=GRAVITY,
            walls=self.platforms_list,
        )

    def process_keychange(self):
        if (
            self.up_pressed
            and not self.down_pressed
            and self.physics_engine.can_jump(y_distance=10)
            and not self.jump_needs_reset
        ):
            self.player_sprite.change_y = JUMP_SPEED
            self.jump_needs_reset = True

        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_draw(self):
        self.clear()

        self.platforms_list.draw()
        self.vampire_list.draw()
        self.player_list.draw()

    def on_key_press(self, key: int, modifiers: int):
        if key in [arcade.key.UP, arcade.key.W]:
            self.up_pressed = True
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.down_pressed = True
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = True
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W]:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.down_pressed = False
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = False
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = False

        self.process_keychange()

    def on_update(self, delta_time):
        self.physics_engine.update()

        self.player_sprite.can_jump = not self.physics_engine.can_jump()
