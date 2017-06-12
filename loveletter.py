import random,winsound
from statistics import median
while 1:
	score=0
	playerscore=0
	aiscore=0
	winsound.PlaySound('newgame.wav', winsound.SND_FILENAME)
	while aiscore<7>playerscore:
		print("New Round of Mocha's Love Letter Sim!",playerscore,"-",aiscore)
		winsound.PlaySound('round.wav', winsound.SND_FILENAME)

		deck=['Princess','Countess','King']+['Prince']*2+['Handmaid']*2+['Baron']*2+['Priest']*2+['Guard']*5
		player=[]
		ai=[]
		discard=[]
		winner=0

		#discard 1 wholly
		del deck[random.randint(0,15)]
		#reveal 3
		delenda=random.randint(0,14)
		discard+=[deck[delenda]]
		del deck[delenda]
		delenda=random.randint(0,13)
		discard+=[deck[delenda]]
		del deck[delenda]
		delenda=random.randint(0,12)
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
			winsound.PlaySound('choose.wav', winsound.SND_FILENAME)
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
			print('You discarded the',choice)
			if protectai==0:
				if choice=='Guard':
					#guess the ai's card
					winsound.PlaySound('guard.wav', winsound.SND_FILENAME)
					guess=0
					while guess not in ['Princess','Countess','King','Prince','Handmaid','Baron','Priest']:
						guess=input('Guess the card in the AI\'s deck: ')
					if guess in ai:
						winner='Player'
						break
					else:
						print('Wrong!')
				elif choice=='Priest':
					winsound.PlaySound('priest.wav', winsound.SND_FILENAME)
					print('AI\'s hand:',ai[0])
				elif choice=='Baron':
					winsound.PlaySound('baron.wav', winsound.SND_FILENAME)
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
					winsound.PlaySound('prince.wav', winsound.SND_FILENAME)
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
					winsound.PlaySound('king.wav', winsound.SND_FILENAME)
					temp=player
					player=ai
					ai=temp
			if choice=='Handmaid':
				winsound.PlaySound('handmaid.wav', winsound.SND_FILENAME)
				protectplayer=1
			elif choice=='Princess':
				winsound.PlaySound('princess.wav', winsound.SND_FILENAME)
				winner='AI'
				break
			#AI's turn~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			if deck!=[]:
				protectai=0
				#draw
				danda=random.randint(0,len(deck)-1)
				ai+=[deck[danda]]
				del deck[danda]
				#check to see if a king or prince forces a countess:
				print('AI is choosing...')
				winsound.PlaySound('aichoose.wav', winsound.SND_FILENAME)
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
						winsound.PlaySound('guard.wav', winsound.SND_FILENAME)
						guess='Guard'
						while guess=='Guard':
							#guess the player's card - this is kinda cheating but it's simple
							guess=random.choice(player+deck)
						if guess in player:
							winner='AI'
							break
						else:
							print('AI Guessed wrong:',guess)
					elif choice=='Priest':
						winsound.PlaySound('priest.wav', winsound.SND_FILENAME)
						#print('Player\'s deck:',player)
						winsound.PlaySound('priest2.wav', winsound.SND_FILENAME)
					elif choice=='Baron':
						winsound.PlaySound('baron.wav', winsound.SND_FILENAME)
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
						winsound.PlaySound('prince.wav', winsound.SND_FILENAME)
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
						winsound.PlaySound('king.wav', winsound.SND_FILENAME)
						temp=player
						player=ai
						ai=temp
				if choice=='Handmaid':
					winsound.PlaySound('handmaid.wav', winsound.SND_FILENAME)
					protectai=1
				elif choice=='Princess':
					winsound.PlaySound('princess.wav', winsound.SND_FILENAME)
					winner='Player'
					break
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