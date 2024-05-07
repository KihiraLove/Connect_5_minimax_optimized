import random


class Bot:
    # TODO: Track open 3 and 4 long chains
    # TODO: Hardcore win condition
    # TODO: Block opponent 4 chains open from one side, 3 chains open from both sides
    # TODO: Cache subtree
    # TODO: clean up directionality
    # TODO: Check all direction calculations for wrong calculations
    # TODO: switch set[i] operations to list(set)[i] operations

    def __init__(self, board):
        self.board = board
        self.x_index_chains = []
        self.o_index_chains = []

    def recalculate_chains(self):
        self.recalculate_chain(True)
        self.recalculate_chain(False)

    def recalculate_chain(self, is_player_x):
        for index_chain in self.x_index_chains if is_player_x else self.o_index_chains:
            new_index_chain = self.board.shift_indexes(index_chain)
            index_chain.clear()
            index_chain.update(new_index_chain)

    def add_last_move(self, move, is_player_x):
        index = self.board.calculate_index_from_position(move[0], move[1])
        matches = self.board.get_neighbours(index, is_player_x)
        if len(self.x_index_chains if is_player_x else self.o_index_chains) == 0 or len(matches) == 0:
            self.x_index_chains.append({index}) if is_player_x else self.o_index_chains.append({index})
        else:
            for neighbour in matches:
                self.add_index_to_chain(index, neighbour, is_player_x)
        opponent = not is_player_x
        opponent_matches = self.board.get_neighbours(index, opponent)
        for neighbour in opponent_matches:
            self.vet_closed_chains(index, neighbour, opponent)

    def vet_closed_chains(self, index, neighbour, is_opponent_x):
        deletable_indexes = []
        # Check the opponents chains
        for i, index_chain in enumerate(self.x_index_chains if is_opponent_x else self.o_index_chains):
            if len(index_chain) == 1:
                neighbours = self.board.calculate_true_neighbouring_indexes(index)
                neighbour_count = len(neighbours)
                if neighbour_count == len(self.board.x_indexes.intersection(neighbours) if is_opponent_x else self.board.o_indexes.intersection(neighbours)):
                    deletable_indexes.append(i)
            if neighbour not in index_chain:
                continue
            chain = list(index_chain)
            chain_direction = abs(chain[1] - chain[0])
            negative_closing_index = chain[0] - chain_direction
            positive_closing_index = chain[-1] + chain_direction
            if negative_closing_index != index and positive_closing_index != index:
                continue

            negative_match = negative_closing_index == index
            positive_match = positive_closing_index == index
            negative_in_chain = negative_closing_index in self.board.x_indexes if is_opponent_x else self.board.o_indexes
            positive_in_chain = positive_closing_index in self.board.x_indexes if is_opponent_x else self.board.o_indexes
            if (negative_match and positive_in_chain) or (positive_match and negative_in_chain):
                deletable_indexes.append(i)

        if len(deletable_indexes) > 0:
            self.delete_indexes_from_chain(sorted(deletable_indexes, reverse=True), is_opponent_x)

    def add_index_to_chain(self, index, neighbour, is_player_x):
        # TODO: rewrite this garbage
        direction = abs(index - neighbour)
        changed_chains_index_direction = []
        hit = False
        for i, index_chain in enumerate(self.x_index_chains) if is_player_x else enumerate(self.o_index_chains):
            if neighbour not in index_chain:
                continue
            hit = True
            if len(index_chain) == 1:
                index_chain.add(index)
                changed_chains_index_direction.append((i, abs(index - neighbour)))
                continue
            sorted_chain = list(index_chain)
            chain_direction = abs(sorted_chain[0] - sorted_chain[1])
            if direction == chain_direction:
                index_chain.add(index)
                changed_chains_index_direction.append((i, chain_direction))
        # Create a new chain and add it to the list is we form a new chain with an index from al already existing chain
        if hit:
            self.x_index_chains.append({index, neighbour}) if is_player_x else self.o_index_chains.append({index, neighbour})

        if len(changed_chains_index_direction) > 1:
            self.check_for_overlap(changed_chains_index_direction, is_player_x)

    def check_for_overlap(self, changed_chains, is_player_x):
        removable_chains = []
        while len(changed_chains) != 0:
            chain_index, chain_direction = changed_chains.pop()
            for index, direction in changed_chains:
                if direction == chain_direction:
                    self.x_index_chains[chain_index].update(self.x_index_chains[index]) if is_player_x else self.o_index_chains[chain_index].update(self.o_index_chains[index])
                    removable_chains.append(index)
        self.delete_indexes_from_chain(sorted(removable_chains, reverse=True), is_player_x)

    def delete_indexes_from_chain(self, indexes, is_player_x):
        for index in indexes:
            if is_player_x:
                del self.x_index_chains[index]
            else:
                del self.o_index_chains[index]

    def check_for_open_chains(self, length):
        pass

    def smart_move(self, last_move, enlarged):
        if enlarged:
            self.recalculate_chains()
        self.add_last_move(last_move, True)
        # TODO: make bot chose move
        move = [random.randint(0, 20), random.randint(0, 20)]
        self.add_last_move(move, False)
        return move
