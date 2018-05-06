"""
    This file is part of Space Jumper.

    Space Jumper is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Space Jumper is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Space Jumper.  If not, see <http://www.gnu.org/licenses/>. 2
"""

""" Cette classe definit des constantes du jeu """

class CONSTS:
    FLIGHT_ORIGIN_ROCKET        = 1

    SETTINGS_FPS                = 60
    SETTINGS_GRAVITY            = .4
    SETTINGS_STANDARD_JUMP_VEL  = 10
    SETTINGS_RANDOM             = .85
    SETTINGS_MAX_RANDOM         = .97

    OBJ_RND_SPRING              = .94
    OBJ_RND_TRAMPOLINE          = .96
    OBJ_RND_MONSTER             = .96
    OBJ_RND_ROCKET              = .983
    OBJ_RND_AUTODESTRUCT        = .75

    OBJ_SCROLL_SPRING           = 600
    OBJ_SCROLL_TRAMPOLINE       = 800
    OBJ_SCROLL_MONSTER          = 2000
    OBJ_SCROLL_ROCKET           = 4000
    OBJ_SCROLL_AUTODESTRUCT     = 5000

    BONUS_MONSTER_SHOT          = 100

    SOUND_JUMP                  = "rc/sounds/jump.wav"
    SOUND_SPRING                = "rc/sounds/feder.wav"
    SOUND_TRAMPOLINE            = "rc/sounds/trampoline.wav"
    SOUND_MONSTER               = "rc/sounds/jumponmonster.wav"
    SOUND_MONSTER_DEAD          = "rc/sounds/monster-crash.wav"
    SOUND_MONSTER_SHOT          = "rc/sounds/monsterpogodak.wav"
    SOUND_ROCKET                = "rc/sounds/jetpack.wav"
    SOUND_SHOT                  = "rc/sounds/pucanje.wav"
    SOUND_FALL                  = "rc/sounds/pada.wav"
    SOUND_AUTODESTRUCT          = "rc/sounds/explodingplatform.wav"

    FILE_SCORES                 = "scores.txt"
