from cogs.minigame.question import Question
from discord.ext import commands
from enum import Enum
from typing import Dict, List, Tuple
import asyncio
import discord
import marshmallow_dataclass
import random
import time


class GameState(Enum):
    OFF = 0
    STARTING = 1
    IN_PROGRESS = 2
    END = 3


class Minigame(object):
    questions_schema = marshmallow_dataclass.class_schema(Question)
    with open('assets/minigame.json') as file:
        questions: List[Question] = questions_schema().loads(json_data=file.read(), many=True)
    ongoing_games = dict()
    standby_messages: List[int] = list()

    def __init__(self, channel_id: int, rounds: int):
        self.max_rounds = rounds
        self.current_round = 1
        self.timer = time.perf_counter()
        self.state = GameState.STARTING
        self.channel_id = channel_id
        self.message_id = 0
        self.players: List[discord.User] = list()
        self.score_board: Dict[int, int] = dict()
        self.questions = Minigame.questions
        random.shuffle(self.questions)

    async def destroy(self, ctx: commands.Context, show_scoreboard: bool = False):
        if show_scoreboard:
            pairs = [(k, v) for k, v in sorted(self.score_board.items(), key=lambda item: item[1], reverse=True)]
            mapped_scores = list()
            for pair in list(enumerate(pairs)):
                for player in self.players:
                    if player.id == pair[1][0]:
                        mapped_scores.append('{}) {} with {} points'.format(pair[0] + 1, player.mention, pair[1][1]))
                        break
            embed = discord.Embed(color=discord.Color.from_rgb(255, 147, 206), title='Minigame ended!', description='Total points:\n{}'.format('\n'.join(mapped_scores)))
            await ctx.send(embed=embed)
        Minigame.ongoing_games.pop(self.channel_id)

    async def progress(self, ctx: commands.Context):
        client: discord.Client = ctx.bot
        color = discord.Color.from_rgb(255, 147, 206)

        def check_participation(m: discord.Message) -> bool:
            return m.author in self.players

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
                Minigame.standby_messages.remove(self.message_id)
                await self.destroy(ctx)
                return

            embed.title = 'Minigame started!'
            embed.description = 'The game has begun!'
            await message.edit(embed=embed)
            Minigame.standby_messages.remove(self.message_id)
            self.state = GameState(self.state.value + 1)
            for player in self.players:
                self.score_board[player.id] = 0
            await self.progress(ctx)

        elif self.state == GameState.IN_PROGRESS:
            if self.current_round > self.max_rounds:
                self.state = GameState(self.state.value + 1)
                await self.progress(ctx)
                return

            current_question: Question
            try:
                current_question = self.questions.pop(0)
            except IndexError:
                self.state = GameState(self.state.value + 1)
                await self.progress(ctx)
                return

            if current_question.type == 'FILL':
                current_question.answers = list(map(lambda x: x.lower(), current_question.answers))
                await ctx.send(current_question.question)
                try:
                    while True:
                        message = await ctx.bot.wait_for('message', check=check_participation, timeout=30)
                        if message.content.lower() in current_question.answers:
                            self.score_board[message.author.id] += 1
                            await ctx.send(f'{message.author.mention} got the point!')
                            self.current_round += 1
                            break
                        elif message.content.lower() == 'skip':
                            await ctx.send('Skipping question...')
                            break
                        else:
                            self.timer = time.perf_counter()
                except asyncio.TimeoutError:
                    await ctx.send('Cancelling stale game...')
                    await self.destroy(ctx)
                    return

            elif current_question.type == 'MULTIPLE':
                current_question.wrong.append(current_question.answers[0])
                random.shuffle(current_question.wrong)

                def map_multiple_answers(answer: Tuple[int, str]) -> str:
                    ordinal = answer[0] + 1
                    option = '{}) {}'.format(ordinal, answer[1])
                    if answer[1] in current_question.answers:
                        current_question.answers.append(str(ordinal))
                    return option

                answers = list(map(map_multiple_answers, list(enumerate(current_question.wrong))))
                message = '{}\n{}'.format(current_question.question, '\n'.join(answers))
                await ctx.send(message)
                try:
                    while True:
                        message = await ctx.bot.wait_for('message', check=check_participation, timeout=30)
                        if message.content in current_question.answers:
                            self.score_board[message.author.id] += 1
                            await ctx.send(f'{message.author.mention} got the point!')
                            self.current_round += 1
                            break
                        elif message.content.lower() == 'skip':
                            await ctx.send('Skipping question...')
                            break
                        else:
                            self.timer = time.perf_counter()
                except asyncio.TimeoutError:
                    await ctx.send('Cancelling stale game...')
                    await self.destroy(ctx)
                    return

            self.timer = time.perf_counter()
            await self.progress(ctx)

        elif self.state == GameState.END:
            await self.destroy(ctx, True)

    @classmethod
    def register_player(cls, channel_id: int, user: discord.User):
        game: Minigame = cls.ongoing_games.get(channel_id)
        if game is not None:
            game.players.append(user)

    @classmethod
    def deregister_player(cls, channel_id: int, user: discord.User):
        game: Minigame = cls.ongoing_games.get(channel_id)
        if game is not None:
            game.players.remove(user)

    @classmethod
    async def create(cls, ctx: commands.Context, rounds: int):
        if ctx.channel.id in cls.ongoing_games.keys():
            current_game: Minigame = cls.ongoing_games.get(ctx.channel.id)
            if time.perf_counter() - current_game.timer > 30.0:
                await ctx.send('Cancelling stale game...')
                cls.ongoing_games.pop(ctx.channel.id)
            else:
                await ctx.send('A game is already running!')
                return
        await ctx.send(f'Starting a game with {rounds} rounds...')
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
