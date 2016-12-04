from collections import Counter
from copy import deepcopy


class BrickMap(object):
    def __init__(self, map=None):
        if map:
            self.map = deepcopy(map)
        else:
            self.map = []

    def load_from_file(self, map_file):
        self.map = []
        with open(map_file, 'r') as f:
            for line in f:
                col = [int(x) for x in line.strip()]
                self.map.append(col)
        print('Loading map from {} and construct {} x {} map'.format(
              map_file, len(self.map), len(self.map[0])))

    def clone(self):
        return BrickMap(map=self.map)

    def normalize(self):
        # merge left
        for c in range(len(self.map) - 1, -1, -1):
            if sum(self.map[c]) == 0:
                del self.map[c]

        # drop down
        for no, col in enumerate(self.map):
            new_col = [c for c in col if c != 0]
            if len(new_col) < len(col):
                new_col.extend([0] * (len(col) - len(new_col)))
                self.map[no] = new_col

    def count_sum(self):
        return sum(sum(col) for col in self.map)

    def is_empty(self):
        return len(self.map) == 0

    def pprint(self):
        for r in range(len(self.map[0]) - 1, -1, -1):
            for c in range(len(self.map)):
                print(self.map[c][r], end=' ')
            print('')
        print('--' * len(self.map))

    def calculate_loss(self):
        num_col = len(self.map)
        num_row = len(self.map[0])

        # no neighbor loss
        total_loss = 0
        for c in range(num_col):
            for r in range(num_row):
                if self.map[c][r] and not self.check_purge(c, r):
                    total_loss += 1

        # game over (single value) loss
        counter = Counter([v for col in self.map for v in col])
        if any(c == 1 for v, c in counter.most_common()):
            total_loss += 9999

        return total_loss

    def check_purge(self, c, r):
        if self.map[c][r] == 0:
            return False

        val = self.map[c][r]
        num_col = len(self.map)
        num_row = len(self.map[0])
        neighbors = []
        for c_direct, r_direct in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_c, new_r = c + c_direct, r + r_direct
            if new_c >= 0 and new_c < num_col and new_r >= 0 and new_r < num_row:
                neighbors.append(self.map[new_c][new_r])
        if any(n == val for n in neighbors):
            return True
        else:
            return False

    def purge(self, c, r):
        prev_sum = self.count_sum()
        to_purge_value = self.map[c][r]
        self._purge(c, r)
        purge_size = (prev_sum - self.count_sum()) / to_purge_value
        score = purge_size * (purge_size - 1)
        return score

    def _purge(self, c, r, prev_val=0):
        if prev_val == 0:  # start
            pruge_val = self.map[c][r]
        else:  # propagate
            pruge_val = prev_val
        if pruge_val == 0:
            return

        num_col = len(self.map)
        num_row = len(self.map[0])
        self.map[c][r] = 0
        for c_direct, r_direct in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_c, new_r = c + c_direct, r + r_direct
            if new_c >= 0 and new_c < num_col and new_r >= 0 and new_r < num_row:
                if self.map[new_c][new_r] == pruge_val:
                    self._purge(new_c, new_r, prev_val=pruge_val)

        if prev_val == 0:
            self.normalize()

    def find_purge_action(self):
        num_col = len(self.map)
        num_row = len(self.map[0])
        action_map = [[True] * num_row for _ in range(num_col)]
        actions = []
        for c in range(num_col):
            for r in range(num_row):
                if action_map[c][r]:
                    if self.map[c][r] != 0 and self.check_purge(c, r):
                        actions.append((c, r))
                    self.purge_action(c, r, action_map)
        return actions

    def purge_action(self, c, r, action_map, prev_val=-1):
        if prev_val == -1:  # start
            pruge_val = self.map[c][r]
        else:  # propagate
            pruge_val = prev_val
        if pruge_val == -1:
            return

        num_col = len(self.map)
        num_row = len(self.map[0])
        action_map[c][r] = False
        for c_direct, r_direct in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_c, new_r = c + c_direct, r + r_direct
            if new_c >= 0 and new_c < num_col and new_r >= 0 and new_r < num_row:
                if action_map[new_c][new_r] and self.map[new_c][new_r] == pruge_val:
                    self.purge_action(new_c, new_r, action_map, prev_val=pruge_val)
