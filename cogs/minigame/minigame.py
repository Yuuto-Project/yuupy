from cogs.minigame.question import Question
from discord.ext import commands
from enum import Enum
from typing import Dict, List, Optional
import asyncio
import discord
import marshmallow_dataclass
import time


class GameState(Enum):
    OFF = 0
    STARTING = 1
    IN_PROGRESS = 2


class Minigame(object):
    questions_schema = marshmallow_dataclass.class_schema(Question)
    with open('assets/minigame.json') as file:
        questions = questions_schema().loads(json_data=file.read(), many=True)
    ongoing_games = dict()
    standby_messages: List[int] = list()

    def __init__(self, channel_id: int, rounds: int):
        self.rounds = rounds
        self.timer = time.perf_counter()
        self.state = GameState.STARTING
        self.channel_id = channel_id
        self.message_id = 0
        self.players: List[discord.User] = list()

    async def progress(self, ctx: commands.Context):
        client: discord.Client = ctx.bot
        color = discord.Color.from_rgb(255, 147, 206)
        if self.state == GameState.STARTING:
            embed = discord.Embed(title='Minigame Starting!', description='React below to join the game! \nThis game may contain spoilers or NSFW themes.\nPlease run `skip` in order to skip a question.', color=color)
            message = await ctx.send(embed=embed)
            await message.add_reaction('🇴')
            Minigame.standby_messages.append(message.id)
            self.message_id = message.id
            for i in range(10, -1, -2):
                players = list(map(lambda x: x.mention, self.players))
                player_mentions = ', '.join(players)
                embed.description = 'React below to join the game! \nThis game may contain spoilers or NSFW themes.\nPlease run `skip` in order to skip a question.\nCurrent players: {}\n{} seconds left!'.format(player_mentions, i)
                await message.edit(embed=embed)
                await asyncio.sleep(2.0)

            if len(self.players) == 0:
                embed.title = 'Minigame cancelled!'
                embed.description = 'Nobody joined...'
                await message.edit(embed=embed)
                Minigame.ongoing_games.pop(self.channel_id)
                return

            embed.title = 'Minigame started!'
            embed.description = 'The game has begun!'
            await message.edit(embed=embed)
            self.state = GameState(self.state.value + 1)
            await self.progress(ctx)
            return
        if self.state == GameState.IN_PROGRESS:
            Minigame.ongoing_games.pop(self.channel_id)
            await ctx.send('Testing ended...')

    @classmethod
    def register_player(cls, channel_id: int, user: discord.User):
        game: Minigame = cls.ongoing_games.get(channel_id)
        if game is not None:
            game.players.append(user)

    @classmethod
    async def create(cls, ctx: commands.Context, rounds: Optional[int] = 7):
        if ctx.channel.id in cls.ongoing_games.keys():
            current_game: Minigame = cls.ongoing_games.get(ctx.channel.id)
            if time.perf_counter() - current_game.timer > 30.0:
                await ctx.send('Cancelling stale game...')
                cls.ongoing_games.pop(ctx.channel.id)
            else:
                await ctx.send('A game is already running!')
                return
        game = cls(ctx.channel.id, rounds)
        cls.ongoing_games[ctx.channel.id] = game
        return game

    @property
    def timer(self) -> float:
        return self._timer

    @timer.setter
    def timer(self, value: float):
        self._timer = value

    @property
    def channel_id(self) -> int:
        return self._channel_id

    @channel_id.setter
    def channel_id(self, value: int):
        self._channel_id = value

    @property
    def message_id(self) -> int:
        return self._message_id

    @message_id.setter
    def message_id(self, value: int):
        self._message_id = value
