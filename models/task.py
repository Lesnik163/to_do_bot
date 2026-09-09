class Task:
	next_id = 1

	def __init__(self, name):
		if name.strip() == "":
			raise ValueError("Название задачи не может быть пустым")
		self.name = name

		self.id = Task.next_id
		Task.next_id += 1

		self.is_completed = False

	def __str__(self):
		status = "✅" if self.is_completed else "❌"
		return f"Задача №{self.id}: {self.name} {status}"


	def complete(self):
		self.is_completed = True

if __name__ == "__main__":
    a = Task("Купить хлеб")
    b = Task("Позвонить")
    print(a)
    print(b)
    b.complete()
    print(b)