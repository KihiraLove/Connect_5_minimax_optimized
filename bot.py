import random


class Bot:
    # TODO: Track open 3 and 4 long chains
    # TODO: check chain boundaries
    # TODO: Block opponent 4 chains open from one side, 3 chains open from both sides
    # TODO: Cache subtree

    def __init__(self, board):
        self.board = board
        self.x_index_chains = []
        self.o_index_chains = []

    def recalculate_chains(self):
        """
        Recalculates the saved chains after enlargement
        """
        self.recalculate_chain(True)
        self.recalculate_chain(False)

    def recalculate_chain(self, is_player_x):
        """
        Recalculate a specific chain after enlargement
        :param is_player_x: boolean indicating whether the player is X or not
        """
        for index_chain in self.x_index_chains if is_player_x else self.o_index_chains:
            new_index_chain = self.board.shift_indexes(index_chain)
            index_chain.clear()
            index_chain.update(new_index_chain)

    def add_last_move(self, move, is_player_x):
        """
        Add the last move to the cache
        :param move: (x, y) tuple containing the coordinates of the last move
        :param is_player_x: boolean indicating whether the player is X or not
        """
        index = self.board.calculate_index_from_position(move[0], move[1])
        matches = self.board.get_neighbours(index, is_player_x)
        if len(self.x_index_chains if is_player_x else self.o_index_chains) == 0 or len(matches) == 0:
            self.add_new_chain({index}, is_player_x)
        else:
            for neighbour in matches:
                self.add_index_to_chain(index, neighbour, is_player_x)
        opponent = not is_player_x
        opponent_matches = self.board.get_neighbours(index, opponent)
        for neighbour in opponent_matches:
            self.vet_closed_chains(index, neighbour, opponent)

    def vet_closed_chains(self, index, neighbour, is_opponent_x):
        """
        Check if any of the opponents chains were closed by the last move, remove closed chains from the cache
        :param index: index of the last move
        :param neighbour: neighbouring index of the last move
        :param is_opponent_x: boolean indicating whether the opponent is X
        """
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
            chain_direction = self.calculate_direction_of_neighbours(chain[0], chain[1])
            negative_closing_index = chain[0] - chain_direction
            positive_closing_index = chain[-1] + chain_direction
            if negative_closing_index != index and positive_closing_index != index:
                continue

            negative_match = negative_closing_index == index
            positive_match = positive_closing_index == index
            negative_in_chain = negative_closing_index in self.board.x_indexes if is_opponent_x else self.board.o_indexes
            positive_in_chain = positive_closing_index in self.board.x_indexes if is_opponent_x else self.board.o_indexes
            negative_off_the_board = self.board.neighbour_breaks_rule(negative_closing_index, chain[0])
            positive_off_the_board = self.board.neighbour_breaks_rule(positive_closing_index, chain[-1])
            positive_closing = positive_in_chain or positive_off_the_board
            negative_closing = negative_in_chain or negative_off_the_board
            # TODO: finish these rules
            false_positive = ((chain_direction == 19 and chain[0] >= self.board.size)
                              or (chain_direction == 1 and chain[0] % self.board.size > 0))

            if (negative_match and positive_closing) or (positive_match and negative_closing):
                deletable_indexes.append(i)

        if len(deletable_indexes) > 0:
            self.delete_chain_by_index(deletable_indexes, is_opponent_x)

    def add_index_to_chain(self, index, neighbour, is_player_x):
        """
        Add an index of a move to chains that contain neighbour
        :param index: index of the move to be added
        :param neighbour: index neighbouring the index parameter
        :param is_player_x: boolean indicating whether the player is X or not
        """
        direction = self.calculate_direction_of_neighbours(index, neighbour)
        changed_chains_index_direction = []
        for i, index_chain in enumerate(self.x_index_chains) if is_player_x else enumerate(self.o_index_chains):
            if neighbour not in index_chain:
                continue
            if len(index_chain) == 1:
                index_chain.add(index)
                changed_chains_index_direction.append((i, direction))
                continue
            sorted_chain = list(index_chain)
            chain_direction = self.calculate_direction_of_neighbours(sorted_chain[0], sorted_chain[1])
            if direction == chain_direction:
                index_chain.add(index)
                changed_chains_index_direction.append((i, direction))
            else:
                # Create a new chain and add it to the list, if we form a new chain
                # with an index, from all already existing chain
                self.add_new_chain({index, neighbour}, is_player_x)

        if len(changed_chains_index_direction) > 1:
            self.check_for_overlap(changed_chains_index_direction, is_player_x)

    def check_for_overlap(self, changed_chains, is_player_x):
        """
        Checks the chains that were chained by the last move in case they overlap
        in case of overlap the function merges the two chains into one
        :param changed_chains: tuple containing the index of the chain in the list of chains
                                and the direction of the chain
        :param is_player_x: boolean indicating whether the player is X or not
        """
        removable_chains = []
        while len(changed_chains) != 0:
            chain_index, chain_direction = changed_chains.pop()
            for index, direction in changed_chains:
                if direction == chain_direction:
                    self.merge_chains(chain_index, index, is_player_x)
                    removable_chains.append(index)
        self.delete_chain_by_index(removable_chains, is_player_x)

    def merge_chains(self, index_to_merge_to, index_to_merge, is_player_x):
        """
        Merge to index chains together by their indexes in the list of chains
        :param index_to_merge_to: index in the list of the chain to merge into
        :param index_to_merge: index in the list of the chain to merge
        :param is_player_x: boolean indicating whether the player is X or not
        """
        if is_player_x:
            self.x_index_chains[index_to_merge_to].update(self.x_index_chains[index_to_merge])
        else:
            self.o_index_chains[index_to_merge_to].update(self.o_index_chains[index_to_merge])

    def add_new_chain(self, chain, is_player_x):
        """
        Add new chain to the list of chains for player
        :param chain: chain to be added to list
        :param is_player_x: boolean indicating whether the player is X or not
        """
        if is_player_x:
            self.x_index_chains.append(chain)
        else:
            self.o_index_chains.append(chain)

    def delete_chain_by_index(self, indexes, is_player_x):
        """
        Delete chains from players index chains by their indexes
        :param indexes: list of indexes of the chains to be deleted
        :param is_player_x: boolean indicating whether the player is X or not
        """
        # Reverse sort the indexes, so we don't have to shift them
        indexes = sorted(indexes, reverse=True)
        for index in indexes:
            if is_player_x:
                del self.x_index_chains[index]
            else:
                del self.o_index_chains[index]

    def calculate_direction_of_neighbours(self, index, neighbour):
        """
        Calculate the direction of a chain from neighbouring indexes
        :param index: index of a move
        :param neighbour: index of a move neighbouring the index parameter
        :return: returns direction
        """
        return abs(index - neighbour)

    def check_for_open_chains(self, length, is_player_x):
        """
        Checks is there is a chain with desired length for the player, return the first one
        :param length: length of the chain
        :param is_player_x: boolean indicating whether the player is X
        :return: index of the chain in the list, or None if there is no chain with desired length
        """
        if is_player_x:
            for i, chain in enumerate(self.x_index_chains):
                if len(chain) == length:
                    return i
        else:
            for i, chain in enumerate(self.o_index_chains):
                if len(chain) == length:
                    return i
        return None

    def check_for_4_move(self, is_player_x):
        """
        Check if the bot has a 4 long chain to win
        or check if the opponent has a 4 long chain that the bot has to block
        :param is_player_x: boolean indicating whether the player is X
        :return: coordinates of the move or None
        """
        index_of_chain = self.check_for_open_chains(4, is_player_x)
        move = None
        if index_of_chain is not None:
            # Bot can win with 4 long chain
            # Player can win with 4 win chain, bot has to block it
            chain = list(self.x_index_chains[index_of_chain] if is_player_x else self.x_index_chains[index_of_chain])
            direction = self.calculate_direction_of_neighbours(chain[0], chain[1])
            negative_closing_index = chain[0] - direction
            positive_closing_index = chain[-1] + direction
            if self.board.is_index_occupied(negative_closing_index):
                move = self.board.calculate_position_from_index(positive_closing_index)
            else:
                move = self.board.calculate_position_from_index(negative_closing_index)
        return move

    def smart_move(self, last_move, enlarged):
        move_found = False
        if enlarged:
            self.recalculate_chains()
        self.add_last_move(last_move, True)
        # Check for win condition
        move = self.check_for_4_move(False)
        if move is None:
            # Check for opponent win condition to block
            move = self.check_for_4_move(True)

        # TODO: make bot chose move
        move = (random.randint(1, 20), random.randint(1, 20))
        self.add_last_move(move, False)
        return move
