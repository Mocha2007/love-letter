import random,pygame
from statistics import median
pygame.mixer.init()
pygame.mixer.Sound('mus.wav').play(-1).set_volume(1/6)
pygame.mixer.Channel(1)
def value(role):
	if role=='Guard':return 1
	if role=='Priest':return 2
	if role=='Baron':return 3
	if role=='Handmaid':return 4
	if role=='Prince':return 5
	if role=='King':return 6
	if role=='Countess':return 7
	if role=='Princess':return 8
	return 0
def wait():
	while pygame.mixer.Channel(1).get_queue()!=None:
		pass
def queue(filename):
        pygame.mixer.Channel(1).queue(pygame.mixer.Sound(filename))
def p(filename):
	wait()
	queue(filename)
def sfxguard():
	file=random.choice(['guard.wav','guard2.wav','guard3.wav'])
	p(file)
def sfxpriest():
	file=random.choice(['priest.wav','priest2.wav'])
	p(file)
def sfxbaron():
	file=random.choice(['baron.wav'])
	p(file)
def sfxhandmaid():
	file=random.choice(['handmaid.wav'])
	p(file)
def sfxprince():
	file=random.choice(['prince.wav'])
	p(file)
def sfxking():
	file=random.choice(['king.wav'])
	p(file)
while 1:
	score=0
	playerscore=0
	aiscore=0
	p('newgame.wav')
	while aiscore<7>playerscore:
		print("New Round of Mocha's Love Letter Sim!",playerscore,"-",aiscore)
		p('round.wav')
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
			p('choose.wav')
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
					sfxpriest()
					print('AI\'s hand:',ai[0])
				elif choice=='Baron':
					sfxbaron()
					print(player[0],'v.',ai[0])
					if value(player[0])>value(ai[0]):
						winner='Player'
						break
					elif value(player[0])<value(ai[0]):
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
					p('aiknows.wav')
					print("I know your hand is the",lastseen,">:3")#DEBUG
				p('aichoose.wav')
				if 'Countess' in ai and ('King' in ai or 'Prince' in ai):choice='Countess'#forced countess?
				elif 'Baron' in ai and lastseen!=0 and value(ai[1-ai.index('Baron')])>value(player[0]):choice='Baron'#ai knows their other card is better than player's
				#else choose
				else:
					#determines median-valued card in deck & player hand
					values=[]
					aimax=3#aside from baron card
					#checks baron first
					if 'Baron' in ai:
						for i in player:
							values+=[value(i)]
						for i in deck:
							values+=[value(i)]
						for i in numyo:
							values+=[value(i)]
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
						if 'Guard'!=lastseen!=0:guess=lastseen
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
						sfxpriest()
						#print('Player\'s deck:',player)
						lastseen=player[0]
					elif choice=='Baron':
						sfxbaron()
						print(player[0],'v.',ai[0])
						if value(player[0])>value(ai[0]):
							winner='Player'
							break
						elif value(player[0])<value(ai[0]):
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
			if value(player[0])>value(ai[0]):winner='Player'
			elif value(player[0])<value(ai[0]):winner='AI'
			if winner!=False:print(winner,'wins!')
			else:print('Tie!')
		if winner=='Player':playerscore+=1
		elif winner=='AI':aiscore+=1
	if playerscore==7:print('Player is first to 7! ( AI had',aiscore,')')
	else:print('AI is first to 7! ( You had',playerscore,')')
	input("-"*20)