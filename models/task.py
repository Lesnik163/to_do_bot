class Task:
	def __init__(self, id, name, is_completed=False):
		if name.strip() == "":
			raise ValueError("Название задачи не может быть пустым")
		self.id = id
		self.name = name
		self.is_completed = is_completed

	def __str__(self):
		status = "✅" if self.is_completed else "❌"
		return f"Задача №{self.id}: {self.name} {status}"


	def complete(self):
		self.is_completed = True
