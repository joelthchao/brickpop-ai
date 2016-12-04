from config import SEARCH_WIDTH, SEARCH_DEPTH, SEARCH_VERBOSE
from game import BrickMap


class GameState(object):
    def __init__(self, map):
        self.map = map.clone()
        self.action = None
        self.score = 0
        self.loss = None
        self.parent = None
        self.children = []

    def add_child(self, map, action, score, loss):
        gs = GameState(map)
        gs.action = action
        gs.score = score + self.score
        gs.loss = loss
        gs.parent = self
        self.children.append(gs)
        return gs


def greedy_step(map):
    current_map = map.clone()
    current_map.pprint()

    actions = current_map.find_purge_action()
    loss_action_pair = []
    for no, action in enumerate(actions):
        new_map = current_map.clone()
        new_map.purge(*action)
        loss = new_map.calculate_loss()
        loss_action_pair.append((loss, action))
    loss_action_pair.sort()

    print('Decision: {}'.format(loss_action_pair[0]))
    current_map.purge(*loss_action_pair[0][1])
    current_map.pprint()
    return current_map


def greedy_multstep(game_state, step):
    if step >= SEARCH_DEPTH:
        return

    # produce next step candidate
    current_map = game_state.map.clone()
    if SEARCH_VERBOSE:
        current_map.pprint()

    actions = current_map.find_purge_action()
    results = []
    for no, action in enumerate(actions):
        new_map = current_map.clone()
        score = new_map.purge(*action)
        if new_map.is_empty():
            loss = 0
            end = True
        else:
            loss = new_map.calculate_loss()
            end = False
        results.append((loss, score, action, new_map, end))
    results.sort()


    # launch next game state
    for loss, score, action, map, end in results[:SEARCH_WIDTH]:
        next_gs = game_state.add_child(map, action, score, loss)
        if not end:
            greedy_multstep(next_gs, step + 1)


def find_best_path(root_gs):
    all_paths = find_path(root_gs)
    all_paths.sort(key=lambda x: (x[-1].loss, -x[-1].score))
    print('Best paths: ')
    for no, gs in enumerate(all_paths[0][1:], 1):
        print('Step {}: {}, loss: {}, score: {}'.format(no, gs.action, gs.loss, gs.score))
    return all_paths[0][1].action


def find_path(root_gs):
    if not root_gs.children:
        return [[root_gs]]
    else:
        all_paths = []
        for child in root_gs.children:
            child_paths = find_path(child)
            for child_path in child_paths:
                all_paths.append([root_gs] + child_path)
        return all_paths


def play_step(map):
    root_game_state = GameState(map)
    greedy_multstep(root_game_state, 0)
    action = find_best_path(root_game_state)
    map.purge(*action)


def play(map_file):
    map = BrickMap()
    map.load_from_file(map_file)
    while True:
        if map.is_empty():
            break
        map.pprint()
        play_step(map)
        if input('continue? n to exit.') == 'n':
            break
    print('End game!')


if __name__ == '__main__':
    map_file = 'maps/map_easy.txt'
    play(map_file)
