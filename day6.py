import requests
import time
import math
from abc import ABC, abstractmethod


class Clock:
    def __init__(self):
        self.start_time = 0
    def __enter__(self):
        self.start_time = time.time()
    def __exit__(self, *args, **kwargs):
        stop_time = time.time()
        print(f"[i] Took {int(stop_time - self.start_time) // 60} min. and {int(stop_time - self.start_time) % 60}s in total")


class AocMeta(ABC):

	def __init__(self, day, cookies):
		self.session = requests.Session()
		self.day = day		
		
		requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)
	
	
	@abstractmethod
	def process_input(self, inp: str) -> dict:
		...
		   
		    
	@abstractmethod
	def first_star(self, inp):
		...
		    
		    
	@abstractmethod
	def second_star(self, inp):
		...
	
	def get_input(self) -> dict:
		if self.session is None:
			raise ValueError("Improperly initialized")
			
		resp = self.session.get(f"https://adventofcode.com/2025/day/{self.day}/input")
		result = resp.content.decode()
		result = self.process_input(result)
		return result

	def submit_answer(self, level, answer):
		while True:
		    resp = self.session.post(f"https://adventofcode.com/2025/day/{self.day}/answer", data={"level": level, "answer": answer})
		    content = resp.content.decode()
		    if "That's not the right answer" in content:
		        return False
		    if "You gave an answer too recently" in content:
		        print("[*] Response sent too soon after each other")
		        time.sleep(30)
		        continue
		    return True
		
		
	def run(self):
		self.first = True
		inp = self.get_input()
		first_answer = self.first_star(inp)
		correct = self.submit_answer(level=1, answer=first_answer)
		print(f"[*] First star result: {first_answer} ... {'correct' if correct else 'incorrect'}")
		if not correct:
			return False
			
		time.sleep(10)

		self.first = False
		inp = self.get_input()
		second_answer = self.second_star(inp)
		correct = self.submit_answer(level=2, answer=second_answer)
		print(f"[*] Second star result: {second_answer} ... {'correct' if correct else 'incorrect'}")
		
		return correct


class Solution(AocMeta):
	def process_input(self, inp: str) -> dict:
		if self.first:
			inp = inp.replace("  ", " ")
			result = [[item.strip() for item in line.strip().split(" ") if len(item.strip()) != 0] for line in inp.split("\n") if len(line.strip()) != 0]
			operations = result.pop(-1)
			result = [[int(num) for num in row if len(num) != 0] for row in result]
			return {"numbers": result, "operations": operations}
		else:
			array = [list(item) for item in inp.split("\n") if len(item.strip()) != 0]
			operations = array.pop(-1)
			start_indices = [index for index in range(len(operations)) if operations[index] != " "]
			numbers = []

			for index in range(len(operations)):
				numbers.append("".join([array[row][index] for row in range(len(array))]))
			
			result = []
			line = []
			for number in numbers:
				number = number.strip()
				if len(number) == 0:
					result.append(line)
					line = []
					continue
				line.append(int(number))
			if len(line) != 0:
				result.append(line)

			return {"numbers": result, "operations": [x.strip() for x in operations if len(x.strip()) != 0]}
		   
	def first_star(self, inp):
		input_numbers, operations = inp["numbers"], inp["operations"]
		result = 0
		for index in range(len(operations)):
			operation = operations[index]
			numbers = [row[index] for row in input_numbers]
			result += sum(numbers) if operation == "+" else math.prod(numbers)
		
		return result
		   
	def second_star(self, inp):
		input_numbers, operations = inp["numbers"], inp["operations"]
		result = 0
		for index in range(len(operations)):
			result += sum(input_numbers[index]) if operations[index] == "+" else math.prod(input_numbers[index])
		
		return result



def main():
	day = "6"
	cookies = {"session": "<SESSION_ID>"}
	
	solution = Solution(day=day, cookies=cookies)
		
	with Clock():
		solution.run()



if __name__ == "__main__":
    main()
