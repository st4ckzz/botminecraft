from config.config import BotConfig
from javascript import require

class MovementController:
    def __init__(self, bot):
        self.bot = bot
        self.pathfinder = require('mineflayer-pathfinder').pathfinder
        self.Movements = require('mineflayer-pathfinder').Movements
        self.goals = require('mineflayer-pathfinder').goals

        self.bot.loadPlugin(self.pathfinder)
        self.setup_movements()

    def setup_movements(self):
        self.movements = self.Movements(self.bot)
        self.bot.pathfinder.setMovements(self.movements)

    def move_to_position(self, x, y, z):
        goal = self.goals.GoalNear(x, y, z, 1)
        try:
            self.bot.pathfinder.setGoal(goal)
            return True
        except Exception as e:
            return False

    def follow_player(self, player_name):
        player = self.bot.players[player_name]
        if player:
            self.move_to_position(
                player.position.x,
                player.position.y,
                player.position.z
            )

    def stop_movement(self):
        self.bot.pathfinder.setGoal(None)

    def jump(self):
        self.bot.setControlState('jump', True)
        self.bot.setControlState('jump', False)