import random,pygame
from statistics import median
pygame.mixer.init()
pygame.mixer.Sound('mus.wav').play(-1).set_volume(1/6)
pygame.mixer.Channel(1)
def wait():
	while pygame.mixer.Channel(1).get_queue()!=None:
		pass
def queue(filename):
        pygame.mixer.Channel(1).queue(pygame.mixer.Sound(filename))
def sfxguard():
	file=random.choice(['guard.wav','guard2.wav','guard3.wav'])
	wait()
	queue(file)
#def sfxpriest()
def sfxbaron():
	file=random.choice(['baron.wav'])
	wait()
	queue(file)
def sfxhandmaid():
	file=random.choice(['handmaid.wav'])
	wait()
	queue(file)
def sfxprince():
	file=random.choice(['prince.wav'])
	wait()
	queue(file)
def sfxking():
	file=random.choice(['king.wav'])
	wait()
	queue(file)
while 1:
	score=0
	playerscore=0
	aiscore=0
	wait()
	queue('newgame.wav')
	while aiscore<7>playerscore:
		print("New Round of Mocha's Love Letter Sim!",playerscore,"-",aiscore)
		wait()
		queue('round.wav')

		deck=['Princess','Countess','King']+['Prince']*2+['Handmaid']*2+['Baron']*2+['Priest']*2+['Guard']*5
		player=[]
		ai=[]
		discard=[]
		winner=0

		#discard 1 wholly
		numya=random.randint(0,15)
		numyo=[deck[numya]]
		del deck[numya]
		#reveal 3
		for i in range(3):
			delenda=random.randint(0,len(deck)-1)
			discard+=[deck[delenda]]
			del deck[delenda]
		#1 card to each player
		danda=random.randint(0,11)
		player+=[deck[danda]]
		del deck[danda]
		danda=random.randint(0,10)
		ai+=[deck[danda]]
		del deck[danda]

		#protection init
		protectai=0
		protectplayer=0

		lastseen=0
		while len(deck)>0:
			#player goes first
			protectplayer=0
			#draw
			danda=random.randint(0,len(deck)-1)
			player+=[deck[danda]]
			del deck[danda]
			#reminders
			print("Your hand:",player)
			print("Discard:",discard)
			#check to see if a king or prince forces a countess:
			wait()
			queue('choose.wav')
			if 'Countess' in player and ('King' in player or 'Prince' in player):
				choice='Countess'
			elif 'Princess' in player:
				for i in player:
					if i!='Princess':
						choice=i
						break
			elif player[0]==player[1]:choice=player[0]
			#else choose
			else:
				choice=0
				if protectai==1:print("AI is currently PROTECTED")
				while choice not in player:
					choice=input("Choose a card to discard: ")
			#move card from hand to discard
			player.remove(choice)
			discard+=[choice]
			if choice==lastseen:lastseen=0
			print('You discarded the',choice)
			if protectai==0:
				if choice=='Guard':
					#guess the ai's card
					sfxguard()
					guess=0
					while guess not in ['Princess','Countess','King','Prince','Handmaid','Baron','Priest']:
						guess=input('Guess the card in the AI\'s deck: ')
					if guess in ai:
						winner='Player'
						break
					else:
						print('Wrong!')
				elif choice=='Priest':
					wait()
					queue('priest.wav')
					print('AI\'s hand:',ai[0])
				elif choice=='Baron':
					sfxbaron()
					print(player[0],'v.',ai[0])
					if 'Princess' in player:
						winner='Player'
						break
					elif 'Princess' in ai:
						winner='AI'
						break
					elif 'Countess' in player:
						winner='Player'
						break
					elif 'Countess' in ai:
						winner='AI'
						break
					elif 'King' in player:
						winner='Player'
						break
					elif 'King' in ai:
						winner='AI'
						break
					elif 'Prince' in player and 'Prince' not in ai:
						winner='Player'
						break
					elif 'Prince' in ai and 'Prince' not in player:
						winner='AI'
						break
					elif 'Handmaid' in player and 'Handmaid' not in ai:
						winner='Player'
						break
					elif 'Handmaid' in ai and 'Handmaid' not in player:
						winner='AI'
						break
					elif 'Baron' in player and 'Baron' not in ai:
						winner='Player'
						break
					elif 'Baron' in ai and 'Baron' not in player:
						winner='AI'
						break
					elif 'Priest' in player and 'Priest' not in ai:
						winner='Player'
						break
					elif 'Priest' in ai and 'Priest' not in player:
						winner='AI'
						break
					else:
						print("There was a tie! Play resumes!")
				elif choice=='Prince':
					sfxprince()
					if ai[0]=='Princess':
						winner='Player'
						break
					try:
						draw=random.randint(0,len(deck)-1)
						print('AI discards the',ai[0])
						discard+=ai
						del ai[0]
						ai+=[deck[draw]]
					except:#game over if deck runs out
						break
					del deck[draw]
				elif choice=='King':
					sfxking()
					temp=player
					player=ai
					ai=temp
					lastseen=player[0]
			if choice=='Handmaid':
				sfxhandmaid()
				protectplayer=1
			#AI's turn~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			if deck!=[]:
				protectai=0
				#draw
				danda=random.randint(0,len(deck)-1)
				ai+=[deck[danda]]
				del deck[danda]
				#check to see if a king or prince forces a countess:
				print('AI is choosing...')
				if lastseen!=0:#DEBUG
					print("I know your hand is the",lastseen,">:3")#DEBUG
				wait()
				queue('aichoose.wav')
				if 'Countess' in ai and ('King' in ai or 'Prince' in ai):
					choice='Countess'
				#else choose
				else:
					#determines median-valued card in deck & player hand
					values=[]
					aimax=0#aside from baron cards
					#checks baron first
					if 'Baron' in ai:
						for i in player:
							if i=='Guard':values+=[1]
							if i=='Priest':values+=[2]
							if i=='Baron':values+=[3]
							if i=='Handmaid':values+=[4]
							if i=='Prince':values+=[5]
							if i=='King':values+=[6]
							if i=='Countess':values+=[7]
							if i=='Princess':values+=[8]
						for i in deck:
							if i=='Guard':values+=[1]
							if i=='Priest':values+=[2]
							if i=='Baron':values+=[3]
							if i=='Handmaid':values+=[4]
							if i=='Prince':values+=[5]
							if i=='King':values+=[6]
							if i=='Countess':values+=[7]
							if i=='Princess':values+=[8]
						for i in numyo:
							if i=='Guard':values+=[1]
							if i=='Priest':values+=[2]
							if i=='Baron':values+=[3]
							if i=='Handmaid':values+=[4]
							if i=='Prince':values+=[5]
							if i=='King':values+=[6]
							if i=='Countess':values+=[7]
							if i=='Princess':values+=[8]
						for i in ai:
							if 'Princess' in ai:aimax=8
							elif 'Countess' in ai:aimax=7
							elif 'King' in ai:aimax=6
							elif 'Prince' in ai:aimax=5
							elif 'Handmaid' in ai:aimax=4
							elif 'Priest' in ai:aimax=2
							elif 'Guard' in ai:aimax=1
						if aimax>median(values):choice='Baron'#will only discard with a >50% chance or player protection
					#choose the LOWEST value card
					if 'Guard' in ai:
						choice='Guard'
					elif 'Priest' in ai:
						choice='Priest'
					elif 'Baron' in ai and protectplayer==1:#will only discard with a >50% chance or player protection
						choice='Baron'
					elif 'Handmaid' in ai:
						choice='Handmaid'
					elif 'Prince' in ai:
						choice='Prince'
					elif 'Baron' in ai:
						choice='Baron'
					elif 'King' in ai:
						choice='King'
					else:
						choice='Countess'
				#move card from hand to discard
				ai.remove(choice)
				discard+=[choice]
				print('AI discards the',choice)
				if protectplayer==0:
					if choice=='Guard':
						sfxguard()
						guess='Guard'
						if lastseen!=0:guess=lastseen
						else:
							while guess=='Guard':
								#guess the player's card - this is kinda cheating but it's simple
								guess=random.choice(player+deck+numyo)
						if guess in player:
							winner='AI'
							break
						else:
							print('AI Guessed wrong:',guess)
					elif choice=='Priest':
						wait()
						queue('priest.wav')
						#print('Player\'s deck:',player)
						lastseen=player[0]
						queue('priest2.wav')
					elif choice=='Baron':
						sfxbaron()
						print(player[0],'v.',ai[0])
						if 'Princess' in player:
							winner='Player'
							break
						elif 'Princess' in ai:
							winner='AI'
							break
						elif 'Countess' in player:
							winner='Player'
							break
						elif 'Countess' in ai:
							winner='AI'
							break
						elif 'King' in player:
							winner='Player'
							break
						elif 'King' in ai:
							winner='AI'
							break
						elif 'Prince' in player and 'Prince' not in ai:
							winner='Player'
							break
						elif 'Prince' in ai and 'Prince' not in player:
							winner='AI'
							break
						elif 'Handmaid' in player and 'Handmaid' not in ai:
							winner='Player'
							break
						elif 'Handmaid' in ai and 'Handmaid' not in player:
							winner='AI'
							break
						elif 'Baron' in player and 'Baron' not in ai:
							winner='Player'
							break
						elif 'Baron' in ai and 'Baron' not in player:
							winner='AI'
							break
						elif 'Priest' in player and 'Priest' not in ai:
							winner='Player'
							break
						elif 'Priest' in ai and 'Priest' not in player:
							winner='AI'
							break
						else:
							print("There was a tie! Play resumes!")
					elif choice=='Prince':
						sfxprince()
						if player[0]=='Princess':
							winner='AI'
							break
						try:
							draw=random.randint(0,len(deck)-1)
							print('Player discards the',player[0])
							discard+=player
							del player[0]
							player+=[deck[draw]]
						except:#game over if deck runs out
							break
						del deck[draw]
					elif choice=='King':
						sfxking()
						temp=player
						player=ai
						ai=temp
						lastseen=player[0]
				if choice=='Handmaid':
					sfxhandmaid()
					protectai=1
			else:break
		if winner!=0:print(winner,'wins!')
		else:
			if 'Princess' in player:winner='Player'
			elif 'Princess' in ai:winner='AI'
			elif 'Countess' in player:winner='Player'
			elif 'Countess' in ai:winner='AI'
			elif 'King' in player:winner='Player'
			elif 'King' in ai:winner='AI'
			elif 'Prince' in player and 'Prince' not in ai:winner='Player'
			elif 'Prince' in ai and 'Prince' not in player:winner='AI'
			elif 'Handmaid' in player and 'Handmaid' not in ai:winner='Player'
			elif 'Handmaid' in ai and 'Handmaid' not in player:winner='AI'
			elif 'Baron' in player and 'Baron' not in ai:winner='Player'
			elif 'Baron' in ai and 'Baron' not in player:winner='AI'
			elif 'Priest' in player and 'Priest' not in ai:winner='Player'
			elif 'Priest' in ai and 'Priest' not in player:winner='AI'
			if winner!=False:print(winner,'wins!')
			else:print('Tie!')
		if winner=='Player':playerscore+=1
		elif winner=='AI':aiscore+=1
	if playerscore==7:print('Player is first to 7! ( AI had',aiscore,')')
	else:print('AI is first to 7! ( You had',playerscore,')')
	input()