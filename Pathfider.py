import numpy as np
from time import time


class Node:
    def __init__(self, pos=None, blocked=False, parent=None):
        self.parent = parent
        self.pos = pos
        self.blocked = blocked  # change if not allowed

        self.value = 1
        self.g = 0  # distance traveled
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos

    def show(self):
        # turn image x
        pass


def path_finder(maze, st_node, target, cher=False):  # st node is all zero anymays
    def test_fuc(node1, test_lis):
        return any(node1 == node2 for node2 in test_lis)

    def set_rage(ax):
        min_val = max([0, curr_node.pos[ax] - 1])
        up_val = min([curr_node.pos[ax] + 1, maze.shape[ax] - 1])
        return tuple((min_val, up_val + 1))

    open_ls = []
    closed_ls = []
    open_ls.append(st_node)

    while open_ls:  # always one in if move allowed
        # print(game.open_ls)
        cost_node = [nd.f for nd in open_ls]
        nd_ind = cost_node.index(min(cost_node))  # location in list
        curr_node = open_ls.pop(nd_ind)
        # print(curr_node.pos)
        # print(len(game.open_ls))
        closed_ls.append(curr_node)  # removes from open adds to xclosed

        if curr_node.pos == target:
            # get path
            node = curr_node
            path = [node.pos]
            while node.parent:  # still parent
                node = node.parent
                path.append(node.pos)
            return path

        pos_val = tuple(map(set_rage, range(2)))  # list of tuples, position in map corids, rem np
        for x in range(*pos_val[0]):  # - 1, pos_val[0] + 2):
            for y in range(*pos_val[1]):  # - 1, pos_val[1] + 2):
                if (x, y) == curr_node.pos:
                    continue
                # list of values if mave cores to corsd
                new_node = Node((x, y), maze[x, y])

                if not cher and all(new_node.pos[ni] != curr_node.pos[ni] for ni in range(2)):
                    # if both are differnt diag
                    new_node.value = np.sqrt(2) * new_node.value

                if test_fuc(new_node, closed_ls) or new_node.blocked:
                    # cant move, better move, need __eq__ for object equal
                    continue

                temp_cost = new_node.value + curr_node.f  # scince node might have diffent rout save best
                if test_fuc(new_node, open_ls):  #

                    if temp_cost < new_node.g:
                        new_node.g = temp_cost
                        new_node.parent = curr_node
                else:
                    new_node.g = temp_cost
                    new_node.parent = curr_node
                    open_ls.append(new_node)
                cost_sqaure(new_node, target, cher)
                new_node.f = new_node.h + new_node.g
    return []


def cost_sqaure(node, target, ch):
    # solve h
    # no g...distance
    dx_dy = np.subtract(target, node.pos)
    if ch:  # diag = 1, dx + dy
        h = sum(dx_dy)
    else:
        h = np.hypot(*dx_dy)
    node.h = h


class Pygame_Disp:
    def __init__(self):
        pass


def text_disp():
    maze = np.array([[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]])

    st_pos = (1, 2)
    start = Node(st_pos)
    end = (7, 6)
    ti = time()
    path = path_finder(maze, start, end)

    p_maze = maze.astype('str')

    for p in path:
        p_maze[p] = 'x'

    p_maze[st_pos] = 's'
    p_maze[end] = 'E'
    print(p_maze)
    path.reverse()
    print(path)
    print('steps: ', len(path))
    print('Time: ', time() - ti)


if __name__ == '__main__':
    text_disp()
