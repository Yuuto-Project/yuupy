import cogs.minigame.questions as miniq
from discord.ext import commands
from enum import Enum
from typing import Dict, List, Tuple
import asyncio
import discord
import marshmallow_dataclass
import random
import time
import datetime
import logging


class GameState(Enum):
    OFF = 0
    STARTING = 1
    IN_PROGRESS = 2
    END = 3


class Minigame(object):
    ongoing_games = dict()
    standby_messages: List[int] = list()

    def __init__(self, channel_id: int, rounds: int):
        self.max_rounds = rounds
        self.current_round = 1
        self.timer = time.perf_counter()
        self.channel_id = channel_id
        self.message_id = 0
        self.players: List[discord.User] = list()
        self.score_board: Dict[int, int] = dict()
        self.questions = miniq.get_questions()
        self.yuuto_pink = 0xFF93CE
        random.shuffle(self.questions)

    async def destroy(self, ctx: commands.Context, show_scoreboard: bool = False):
        if show_scoreboard:
            pairs = [(k, v) for k, v in sorted(self.score_board.items(), key=lambda item: item[1], reverse=True)]
            mapped_scores = list()
            for pair in list(enumerate(pairs)):
                for player in self.players:
                    if player.id == pair[1][0]:
                        mapped_scores.append(f'{pair[0]+1}) {player.mention} with {pair[1][1]} points')
                        break
            embed = discord.Embed(color=self.yuuto_pink,
                                  title='Minigame ended!', 
                                  description='Total points:\n{}'.format('\n'.join(mapped_scores)))
            await ctx.send(embed=embed)
        Minigame.ongoing_games.pop(self.channel_id)

    async def start(self, ctx: commands.Context):
            embed = discord.Embed(title='Minigame Starting!', 
                                  description='React below to join the game! \n'\
                                              'This game may contain spoilers or NSFW themes.\n'\
                                              'Please type `skip` in order to skip a question.', 
                                  color=self.yuuto_pink)
            message = await ctx.send(embed=embed)

            await message.add_reaction('🎲')
            Minigame.standby_messages.append(message.id)

            self.message_id = message.id
            for i in range(10, -1, -2):
                players = list(map(lambda x: x.mention, self.players))
                player_mentions = ', '.join(players)
                embed.description = 'React below to join the game! \n'\
                                    'This game may contain spoilers or NSFW themes.\n'\
                                    'Please type `skip` in order to skip a question.\n'\
                                    'Current players: {}\n'\
                                    '{} seconds left!'.format(player_mentions, i)
                await message.edit(embed=embed)
                await asyncio.sleep(2.0)

            if len(self.players) == 0:
                embed.title = 'Minigame cancelled!'
                embed.description = 'Nobody joined...'
                await message.edit(embed=embed)
                Minigame.standby_messages.remove(self.message_id)
                await self.destroy(ctx)
                return False

            embed.title = 'Minigame started!'
            embed.description = 'The game has begun!'
            await message.edit(embed=embed)
            Minigame.standby_messages.remove(self.message_id)
            for player in self.players:
                self.score_board[player.id] = 0
            return True

    async def ask(self, ctx, question):
        # Verify if user is playing in the game
        def check_participation(m: discord.Message) -> bool:
            return m.author in self.players

        while True:
            # Wait for a message from a participating player
            message = await ctx.bot.wait_for('message', check=check_participation, timeout=30)
            if message.content.lower() in question['answers']:
                self.score_board[message.author.id] += 1
                await ctx.send(f'{message.author.mention} got the point!')
                self.current_round += 1
                break
            elif message.content.lower() == 'skip':
                await ctx.send('Skipping question...')
                break
            else:
                # Reset timeout
                self.timer = time.perf_counter()
        
    async def prog(self, ctx): 
        current_question: Question
        try:
            current_question = self.questions.pop()
        except IndexError:
            await ctx.send('Oh no! I messed up the questions! Game over.')
            logging.error('Minigame failed due to index error')
            await self.destroy(ctx, True)
            return

        # Fill in the gap style questions
        if current_question['type'] == 'FILL':
            current_question['answers'] = list(map(lambda x: x.lower(), current_question['answers']))
            await ctx.send(current_question['question'])
            
        # Multiple choice type questions
        elif current_question['type'] == 'MULTIPLE':
            current_question['wrong'].append(current_question['answers'][0])
            random.shuffle(current_question['wrong'])

            # Generate one sendable string
            def map_multiple_answers(answer: Tuple[int, str]) -> str:
                ordinal = answer[0] + 1
                option = f'{ordinal}) {answer[1]}'
                if answer[1] in current_question['answers']:
                    current_question['answers'].append(str(ordinal))
                return option

            answers = list(map(map_multiple_answers, list(enumerate(current_question['wrong']))))
            message = '{}\n{}'.format(current_question['question'], '\n'.join(answers))
            await ctx.send(message)

        # Get answer
        try:
            await self.ask(ctx, current_question)
        except asyncio.TimeoutError:
            await ctx.send('Cancelling stale game...')
            await self.destroy(ctx)
            return False

        self.timer = time.perf_counter()
        return True

    async def game(self, ctx: commands.Context):
        # Attempt start
        # Returns false if nobody joins/errors occure
        if await self.start(ctx) == False:
            return

        # Ask the questions
        for i in range(self.max_rounds):
            if await self.prog(ctx) == False:
                return

        # End and destory session
        await self.destroy(ctx, True)
        return
                        
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
