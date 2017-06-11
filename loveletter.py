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
player+=[deck[danda]]
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
			ai+=deck[draw]
			del deck[draw]
		elif choice=='King':
			temp=player
			player=ai
			ai=temp
	elif choice=='Princess':
		winner='AI'
		break
	#AI's turn
	input("END OF TEST")
print(winner,'wins!')