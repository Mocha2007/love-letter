import random

deck=['Princess','Countess','King']+['Prince']*2+['Handmaid']*2+['Baron']*2+['Priest']*2+['Guard']*5
player=[]
ai=[]
discard=[]
winner=None

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
	if 'Countess' in player and ('King' in player or 'Prince' in player):
		choice='Countess'
	#else choose
	else:
		choice=0
		while choice not in player:
			choice=input("Choose a card to discard: ")
	#move card from hand to discard
	player.remove(choice)
	discard+=[choice]
	print('You discarded the',choice)
	if protectai==0:
		if choice=='Guard':
			#guess the ai's card
			guess=input('Guess the card in the AI\'s deck: ')
			if guess in ai:
				winner='Player'
				break
			else:
				print('Wrong!')
		elif choice=='Priest':
			print('AI\'s deck:',ai)
		elif choice=='Baron':
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
		elif choice=='Handmaid':
			protectplayer=1
		elif choice=='Prince':
			discard+=ai
			del ai[0]
			draw=random.randint(0,len(deck)-1)
			ai+=[deck[draw]]
			del deck[draw]
		elif choice=='King':
			temp=player
			player=ai
			ai=temp
	elif choice=='Princess':
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
		if 'Countess' in ai and ('King' in ai or 'Prince' in ai):
			choice='Countess'
		#else choose
		else:
			#choose the LOWEST value card
			if 'Guard' in ai:
				choice='Guard'
			elif 'Priest' in ai:
				choice='Priest'
			elif 'Baron' in ai and ('Prince' in ai or 'King' in ai or 'Countess' in ai or 'Princess' in ai):#will only discard with prince+
				choice='Baron'
			elif 'Handmaid' in ai:
				choice='Handmaid'
			elif 'Prince' in ai:
				choice='Prince'
			elif 'King' in ai:
				choice='King'
			elif 'Baron' in ai:
				choice='Baron'
			else:
				choice='Countess'
		#move card from hand to discard
		ai.remove(choice)
		discard+=[choice]
		print('AI discard the',choice)
		if protectplayer==0:
			if choice=='Guard':
				#guess the player's card - this is kinda cheating but it's simple
				guess=random.choice(player+deck)
				if guess in player:
					winner='AI'
					break
				else:
					print('AI Guessed wrong!')
			elif choice=='Priest':
				#print('Player\'s deck:',player)
				pass
			elif choice=='Baron':
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
			elif choice=='Handmaid':
				protectai=1
			elif choice=='Prince':
				discard+=player
				del player[0]
				draw=random.randint(0,len(deck)-1)
				player+=[deck[draw]]
				del deck[draw]
			elif choice=='King':
				temp=player
				player=ai
				ai=temp
		elif choice=='Princess':
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