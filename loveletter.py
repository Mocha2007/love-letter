from random import randint, choice
from sys import argv

nosound = 'nosound' in argv
if not nosound:
	import pygame
	pygame.mixer.init()
	pygame.mixer.Sound('sfx/mus.wav').play(-1).set_volume(1/6)
	pygame.mixer.Channel(1)

values = {
	'Guard': 1,
	'Priest': 2,
	'Baron': 3,
	'Handmaid': 4,
	'Prince': 5,
	'King': 6,
	'Countess': 7,
	'Princess': 8,
}

sfx = {
	'guard': ['guard','guard2','guard3'],
	'priest': ['priest', 'priest2'],
	'baron': ['baron'],
	'handmaid': ['handmaid'],
	'prince': ['prince'],
	'king': ['king'],
}

def value(role: str) -> int:
	return values[role] if role in values else 0

def wait() -> None:
	while pygame.mixer.Channel(1).get_queue():
		pass

def queue(filename: str) -> None:
	pygame.mixer.Channel(1).queue(pygame.mixer.Sound(filename))

def p(filename: str) -> None:
	if nosound:
		return
	wait()
	queue(f'sfx/{filename}.wav')

def sfx_play(type: str) -> None:
	p(choice(sfx[type]))

# main
while 1:
	score = 0
	playerscore = 0
	aiscore = 0
	p('newgame')
	while aiscore < 7 > playerscore:
		print("New Round of Mocha's Love Letter Sim!")
		print(f"{playerscore} - {aiscore}")
		p('round')
		deck = ['Princess','Countess','King'] \
			+ ['Prince']*2 + ['Handmaid']*2 \
			+ ['Baron']*2 + ['Priest']*2 + ['Guard']*5
		player = []
		ai = []
		discard = []
		winner = 0
		# discard 1 wholly
		numya = randint(0,15)
		numyo = [deck[numya]]
		del deck[numya]
		# reveal 3
		for _ in range(3):
			delenda = randint(0, len(deck)-1)
			discard += [deck[delenda]]
			del deck[delenda]
		# 1 card to each player
		danda = randint(0, 11)
		player.append(deck[danda])
		del deck[danda]
		danda = randint(0, 10)
		ai.append(deck[danda])
		del deck[danda]
		# protection init
		protectai = False
		protectplayer = False
		lastseen = 0
		while len(deck):
			# player goes first
			protectplayer = False
			# draw
			danda = randint(0, len(deck)-1)
			player.append(deck[danda])
			del deck[danda]
			# reminders
			print(f"Your hand: {', '.join(player)}")
			print(f"Discard: {', '.join(discard)}")
			# check to see if a king or prince forces a countess:
			p('choose')
			if 'Countess' in player and ('King' in player or 'Prince' in player):
				ch = 'Countess'
			elif 'Princess' in player:
				for i in player:
					if i != 'Princess':
						ch = i
						break
			elif player[0] == player[1]:
				ch = player[0]
			# else choose
			else:
				ch = 0
				if protectai:
					print("AI is currently PROTECTED")
				while ch not in player:
					ch = input("Choose a card to discard: ")
			# move card from hand to discard
			player.remove(ch)
			discard.append(ch)
			if ch == lastseen:
				lastseen = 0
			print(f'You discarded the {ch}')
			if not protectai:
				if ch == 'Guard':
					# guess the ai's card
					sfx_play('guard')
					guess = 0
					while guess not in ['Princess', 'Countess', 'King', 'Prince', 'Handmaid', 'Baron', 'Priest']:
						guess = input('Guess the card in the AI\'s deck: ')
					if guess in ai:
						winner = 'Player'
						break
					else:
						print('Wrong!')
				elif ch == 'Priest':
					sfx_play('priest')
					print(f"AI's hand: {ai[0]}")
				elif ch == 'Baron':
					sfx_play('baron')
					print(f"{player[0]} v. {ai[0]}")
					if value(player[0]) > value(ai[0]):
						winner = 'Player'
						break
					elif value(player[0]) < value(ai[0]):
						winner = 'AI'
						break
					else:
						print("There was a tie! Play resumes!")
				elif ch == 'Prince':
					sfx_play('prince')
					if ai[0] == 'Princess':
						winner = 'Player'
						break
					try:
						draw = randint(0, len(deck)-1)
						print('AI discards the', ai[0])
						discard += ai
						del ai[0]
						ai.append(deck[draw])
					except: # game over if deck runs out
						break
					del deck[draw]
				elif ch == 'King':
					sfx_play('king')
					temp = player
					player = ai
					ai = temp
					lastseen = player[0]
			if ch == 'Handmaid':
				sfx_play('handmaid')
				protectplayer = True
			# AI's turn~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			if deck:
				protectai = False
				# draw
				danda = randint(0, len(deck)-1)
				ai.append(deck[danda])
				del deck[danda]
				# check to see if a king or prince forces a countess:
				print('AI is choosing...')
				if lastseen:
					p('aiknows')
					print(f"I know your hand is the {lastseen} >:3")
				p('aichoose')
				if 'Princess' in ai:
					ch = ai[1-ai.index('Princess')] # forced
				elif 'Countess' in ai and ('King' in ai or 'Prince' in ai):
					ch = 'Countess' # forced countess?
				elif 'Baron' in ai and lastseen and value(ai[1-ai.index('Baron')]) > value(player[0]):
					ch = 'Baron' # ai knows their other card is better than player's
				# else choose
				# if AI discards baron, does it have >50% chance of winning?
				elif 'Baron' in ai and 0.5 < sum(max(ai, key=value) > c \
						for c in player+deck+numyo)/len(player+deck+numyo):
					ch = 'Baron'
				# choose the LOWEST value card
				elif 'Guard' in ai:
					ch = 'Guard'
				elif 'Priest' in ai:
					ch = 'Priest'
				elif 'Baron' in ai and protectplayer:
					# will only discard with a >50% chance or player protection
					ch = 'Baron'
				elif 'Handmaid' in ai:
					ch = 'Handmaid'
				elif 'Prince' in ai:
					ch = 'Prince'
				elif 'King' in ai:
					ch = 'King'
				elif 'Baron' in ai: # idk if this is necessary, but...
					ch = 'Baron'
				else:
					ch = 'Countess'
				# move card from hand to discard
				ai.remove(ch)
				discard.append(ch)
				print(f'AI discards the {ch}')
				if not protectplayer:
					if ch == 'Guard':
						sfx_play('guard')
						guess = 'Guard'
						if 'Guard' != lastseen != 0:
							guess = lastseen
						else:
							while guess == 'Guard':
								# guess the player's card - this is kinda cheating but it's simple
								guess = choice(player+deck+numyo)
						if guess in player:
							winner = 'AI'
							break
						else:
							print(f'AI Guessed wrong: {guess}')
					elif ch == 'Priest':
						sfx_play('priest')
						# print('Player\'s deck:',player)
						lastseen = player[0]
					elif ch == 'Baron':
						sfx_play('baron')
						print(f"{player[0]} v. {ai[0]}")
						if value(player[0]) > value(ai[0]):
							winner = 'Player'
							break
						elif value(player[0]) < value(ai[0]):
							winner = 'AI'
							break
						else:
							print("There was a tie! Play resumes!")
					elif ch == 'Prince':
						sfx_play('prince')
						if player[0] == 'Princess':
							winner = 'AI'
							break
						try:
							draw = randint(0, len(deck)-1)
							print(f'Player discards the {player[0]}')
							discard += player
							del player[0]
							player.append(deck[draw])
							del deck[draw]
						except:
							# game over if deck runs out
							break
					elif ch == 'King':
						sfx_play('king')
						temp = player
						player = ai
						ai = temp
						lastseen = player[0]
				if ch == 'Handmaid':
					sfx_play('handmaid')
					protectai = True
			else: # deck empty
				print(f'Deck Empty! Player: {player[0]} v. AI: {ai[0]}')
				break
		if winner:
			print(winner,'wins!')
		else:
			if value(player[0]) > value(ai[0]):
				winner = 'Player'
			elif value(player[0]) < value(ai[0]):
				winner = 'AI'
			if winner:
				print(winner, 'wins!')
			else:
				print('Tie!')
		if winner == 'Player':
			playerscore += 1
		elif winner == 'AI':
			aiscore += 1
	if playerscore == 7:
		print(f'Player is first to 7! (AI had {aiscore})')
	else:
		print(f'AI is first to 7! (You had {playerscore})')
	input("-"*20)