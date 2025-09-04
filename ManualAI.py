
from AI import AI
from Action import Action


class ManualAI( AI ):

	def getAction(self, number: int) -> "Action Object":
		""" Prompt user for type of action, and the coordinates of where to perform that action """
		""" Return an Action object storing that information """
	
		action = input("Enter an action: ").strip().lower()
		if action == "l":
			action = AI.Action.LEAVE
			return Action(action)
		elif action == "u":
			action = AI.Action.UNCOVER
		elif action == "f":
			action = AI.Action.FLAG
		elif action == "n":
			action = AI.Action.UNFLAG
			
		coordX = int(input("Enter the X coordinate of the tile: ").strip()) - 1
		coordY = int(input("Enter the Y coordinate of the tile: ").strip()) - 1

		return Action(action, coordX, coordY)

