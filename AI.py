
from abc import ABCMeta, abstractmethod
from enum import Enum, unique


class AI:
	__metaclass__ = ABCMeta

	@unique
	class Action (Enum):
		LEAVE = 0
		UNCOVER = 1
		FLAG = 2
		UNFLAG = 3
		
	@abstractmethod
	def getAction(self, number: int) -> "Action Oject":
		pass
