import cv2
import pygame.sprite
import numpy
from ....common.game_objects.sprites.setup import calibration
from ..config import config


def relative_to_absolute(relative_coord, centre_coord):
    centre_x, centre_y = centre_coord
    relative_x, relative_y = relative_coord
    return centre_x + relative_x, centre_y + relative_y


def square_anchor_from_centre(centre_xy, square_length):
    half_square_length = square_length / 2
    centre_x, centre_y = centre_xy
    anchor = int(centre_x - half_square_length), int(centre_y - half_square_length)
    return anchor


class Calibrator:
    def __init__(self, calibrate_sprites, font, projector_resolution):
        self.complete = False
        self.results = {}
        self.calibrate_sprites = calibrate_sprites
        self.font = font
        self.projector_resolution = projector_resolution
        self.instruction = None
        self.relative_anchor_positions = {
            # x, y relative to centre
            'red': (-150, -150),
            'blue': (150, 150),
            # 'purple': (0, 150)
        }
        self.transform_matrices = {}

    def is_complete(self):
        return self.complete

    def get_results(self):
        return self.results

    def start(self):
        title = calibration.CalibrationTitle(
            self.font, 'Calibrating', 'Please wait', self.projector_resolution, None, None
        )
        self.calibrate_sprites.add(title)
        # 1. This should project 4 squares on the playing surface, doesn't matter where -
        # but the locations are known in the projector coordinate frame
        piece_tiles = calibration.CalibrationTiles(self.projector_resolution, None, None)
        self.calibrate_sprites.add(piece_tiles)
        piece_tiles.add_tile(
            pygame.Color('red'),
            square_anchor_from_centre(self.relative_anchor_positions.get('red'), 30),
            30
        )
        # piece_tiles.add_tile(pygame.Color('green'), 150, 100)
        piece_tiles.add_tile(
            pygame.Color('blue'),
            square_anchor_from_centre(self.relative_anchor_positions.get('blue'), 30),
            30
        )
        # piece_tiles.add_tile(
        #     pygame.Color('purple'),
        #     square_anchor_from_centre(self.relative_anchor_positions.get('purple'), 30),
        #     30
        # )
        title.set_subtitle('Place coloured pieces onto tiles')
        self.instruction = title
        # 2. The player places 4 colored pieces in those squares

    def step_2(self):
        # 2. The player places 4 colored pieces in those squares
        self.instruction.set_subtitle('Press space when ready')

    def step_3(self):
        # 3. The camera detects the location of the pieces in the camera frame
        # 4. Line up the two frames
        self.instruction.set_subtitle('Please wait')

    def align_frames(self, tokens):
        # 4. Line up the two frames
        """
        Align the coordinate frames of the camera and the projector.
        Assuming that the camera and projector stay relative to each other,
        but the board may move

        tokens: dict of color: (x, y)
        :return: A transformation matrix from the camera's coordinates to the projector's coordinates
        """

        projector_size = config.get_property(['resolution', 'projector'])

        projector_centre_x = int(projector_size.get('x') / 2)
        projector_centre_y = int(projector_size.get('y') / 2)
        projector_centre = projector_centre_x, projector_centre_y

        red_camera = numpy.array(tokens.get('red'))
        blue_camera = numpy.array(tokens.get('blue'))
        red_projector = numpy.array(relative_to_absolute(self.relative_anchor_positions.get('red'), projector_centre))
        blue_projector = numpy.array(relative_to_absolute(self.relative_anchor_positions.get('blue'), projector_centre))

        # SCALE - find how much the camera (which may already be scaled)
        # needs to be scaled by to get to the projector scale
        dcx = blue_camera[0] - red_camera[0]
        dpx = blue_projector[0] - red_projector[0]
        sfx = dpx / dcx
        dcy = blue_camera[1] - red_camera[1]
        dpy = blue_projector[1] - red_projector[1]
        sfy = dpy / dcy
        # Move red_camera to origin
        translate_to_origin_matrix = red_camera * -1
        red_camera = red_camera + translate_to_origin_matrix
        blue_camera = blue_camera + translate_to_origin_matrix
        # Scale
        # red_camera at origin
        scale_matrix = numpy.array([[sfx, 0],
                                    [0, sfy]])
        blue_camera = numpy.dot(scale_matrix, blue_camera)

        # ROTATE s.t. the angle of camera_rec(origin) to camera_blue is the same as p_red to p_blue
        # Calc target angle, angle is anticlockwise in rads
        projector_red_blue_vector = blue_projector - red_projector  # [300, 300]
        projector_vector_x = projector_red_blue_vector[0]
        projector_vector_y = projector_red_blue_vector[1]
        target_angle = numpy.arctan2(projector_vector_x, projector_vector_y)  # pi/4 == 45deg
        # Calc actual angle
        actual_angle_x = blue_camera[0]
        actual_angle_y = blue_camera[1]
        actual_angle = numpy.arctan2(actual_angle_x, actual_angle_y)
        transform_angle = target_angle - actual_angle
        rotation_matrix = numpy.array([[numpy.cos(transform_angle), -numpy.sin(transform_angle)],
                                       [numpy.sin(transform_angle), numpy.cos(transform_angle)]])
        # rotation matrix applied to a (x, y) vector
        blue_camera = numpy.dot(rotation_matrix, blue_camera)

        # TRANSLATE into final position
        translate_to_final_matrix = red_projector

        # don't return but set to data vars
        # return translate_to_origin_matrix, scale_matrix, rotation_matrix, translate_to_final_matrix

        self.transform_matrices = {
            'translate_to_origin': translate_to_origin_matrix,
            'scale': scale_matrix,
            'rotate': rotation_matrix,
            'translate_to_final': translate_to_final_matrix
        }

    def transform_point(self, point):
        # Translate towards origin
        point = point + self.transform_matrices.get('translate_to_origin')
        point = numpy.dot(self.transform_matrices.get('scale'), point)
        point = numpy.dot(self.transform_matrices.get('rotate'), point)
        point = point + self.transform_matrices.get('translate_to_final')
        return point.astype(int)

    def step_5(self, tokens):
        self.instruction.set_subtitle('Remove all pieces from the board')
        return len(tokens) == 0
