import numpy as np

cube_dim = 3
cube_pos = np.arange(cube_dim ** 3).reshape((cube_dim, cube_dim, cube_dim))  # loop create plocks


class Block:
    def __init__(self, colors):
        self.colors = colors


# either mat revesed or mat, index
# alow input from norm, slash self alg
def shift_blocks(start):
    # if row, all col, if col all rows
    start_r = start
    start_col = 1
    stop_row = 1
    stop_col = 1
    cube_pos[start_r:stop_row, start_col:stop_col] = np.rot90(np.copy(cube_pos[start_r:stop_row, start_col:stop_col]))


def alg_from_list(alg_str):
    for op in alg_str.upper():
        # split at inverse
        if op == 'T' or op == 'U':
            shift_blocks()