import operator
import random


class Player:
    def __init__(self, name, active=True, games_played=0):
        self.name = name
        self.active = active
        self.games_played = games_played

    def sit(self):
        self.active = False

    def unsit(self):
        self.active = True

    def play(self):
        self.games_played += 1
        print("\t{} is playing! ({})".format(self.name, self.games_played))

    def get_name(self):
        return self.name

    def get_games_played(self):
        return self.games_played

    def is_active(self):
        return self.active


class Game:
    def __init__(self, capacity=0, players=[]):
        self.capacity = capacity
        self.players = players
        self.games_played = 0

    def set_capacity(self, capacity):
        self.capacity = int(capacity)

    def get_capacity(self):
        return self.capacity if self.capacity < len(self.get_active_players()) else len(self.get_active_players())

    def add_player(self, n, active=True, games_played=-1):
        if self.games_played == 0:
            games_played = 0
        if games_played == -1:
            games_played = self.games_played-1
        self.players.append(Player(n, active, games_played))
        print('{} added!'.format(n))

    def remove_player(self, n):
        player = self.get_player(n)
        if player:
            self.players.remove(player)
            print("{} has been removed.".format(n))
        else:
            print("{} is not playing.".format(n))

    def sit_player(self, n):
        player = self.get_player(n)
        player.sit()
        print('{} is now sitting out'.format(n))

    def unsit_player(self, n):
        player = self.get_player(n)
        player.unsit()
        print('{} is no longer sitting'.format(n))

    def all_in(self):
        for player in self.players:
            player.unsit()

    def get_active_players(self):
        active = []
        for player in self.players:
            if player.is_active():
                active.append(player)
        return active

    def pick_players(self):
        active_pool = self.get_active_players()
        active_pool.sort(key=operator.attrgetter('games_played'))

        min_max = 0  # determine guaranteed cut off
        for player in active_pool[:self.capacity]:
            target = player.get_games_played()
            if min_max < target:
                min_max = target

        # Note: if player is exactly the target number, he is not guarenteed a spot
        this_round = []
        for player in active_pool[:self.capacity]:
            if player.get_games_played() < min_max:
                this_round.append(player)
                active_pool.remove(player)

        while len(this_round) < self.get_capacity():
            rng = random.randrange(0, self.get_capacity()-len(this_round), 1)
            this_round.append(active_pool[rng])
            active_pool.remove(active_pool[rng])

        self.games_played += 1
        print("This rounds players:")
        for players in this_round:
            players.play()

    def get_player(self, players):
        found = False
        i = 0
        while not found and i < len(players):
            if name == self.players[i].get_name():
                found = True
                i -= 1
            i += 1

        return self.players[i] if found else None

    def player_list(self):
        print("All Players: ({} active/{} capacity)".format(len(self.get_active_players()), self.capacity))
        for player in self.players:
            print('\t{} ({})'.format(player.get_name(), "active" if player.is_active() else "sitting"))


playing = True
commands = {
    'capacity <set num>': 'set the number of concurrent players',
    'help, h': 'show list of commands',
    'player <add/remove/sit/unsit> name': 'add, remove, sit, or unsit a player',
    'player <list>': 'lists all players and their status',
    'play': 'gets next set of players',
    'stop': 'ends game session'
}

game = Game()

print("Ben's Player Picker!")
print("Enter \"h\" or \"help\" for help.")
while playing:
    cmd = input(">>> ")
    c = cmd.lower()
    if c == "":
        pass
    elif c == 'h' or c == 'help':
        print("Commands: \n\t{}".format(
            '\n\t'.join(['{}\t\t= =\t\t{}'.format(k, commands[k]) for k in commands])
        ))
    elif c.split()[0] == 'player' or c.split()[0] == 'players':
        params = c.split()[1:]
        action = params[0]      # add/remove/sit/play
        name = ' '.join(params[1:]) if len(params) >= 2 else None        # "Dave"

        if action == 'list':
            game.player_list()
        elif action == 'add':
            game.add_player(name)
        elif action == 'remove' or action == 'rm':
            game.remove_player(name)
        elif action == 'sit':
            game.sit_player(name)
        elif action == 'unsit':
            if name == 'all':
                game.all_in()
                print("All players are in!")
            else:
                game.unsit_player(name)
    elif c == 'list':
        game.player_list()
    elif c == 'play':
        game.pick_players()
    elif c.split()[0] == 'capacity':
        params = c.split()[1:]
        cap = params[0]
        game.set_capacity(cap)
        print("Game capacity set to {}".format(cap))
    elif c == 'stop' or c == 'gg' or c == 'ggs':
        playing = False
        print("GGs")
    else:
        print("\"{}\" is not a recognized command.".format(cmd))

