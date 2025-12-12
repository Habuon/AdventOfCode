import requests
import time
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
		inp = self.get_input()
		first_answer = self.first_star(inp)
		correct = self.submit_answer(level=1, answer=first_answer)
		print(f"[*] First star result: {first_answer} ... {'correct' if correct else 'incorrect'}")
		if not correct:
			return False
			
		# time.sleep(10)
		
		# second_answer = self.second_star(inp)
		# correct = self.submit_answer(level=2, answer=second_answer)
		# print(f"[*] Second star result: {second_answer} ... {'correct' if correct else 'incorrect'}")
		
		# return correct


class Solution(AocMeta):
	def process_input(self, inp: str) -> dict:
		shapes = dict()
		spaces = []

		shape = None
		for line in inp.split("\n"):
			line = line.strip()
			if len(line) == 0:
				shape = None
				continue
			if "x" in line:
				shape = False
			if shape is None:
				shape = int(line.split(":")[0]) + 1
				continue
			if shape:
				shapes[shape - 1] = shapes.get(shape - 1, []) + [list(line)]
			else:
				size, required_shapes = line.split(":")
				required_shapes = [int(x) for x in required_shapes.split(" ") if len(x) != 0]
				rows, cols = [int(x) for x in size.split("x")]
				spaces.append(((rows, cols), required_shapes))
		shapes = {key: sum([x.count("#") for x in value]) for key, value in shapes.items()}
		return {"shapes": shapes, "spaces": spaces}
	  

	def first_star(self, inp):
		shapes, spaces = inp["shapes"], inp["spaces"]
		heuristic_constant = 1.25
		result = 0
		for space in spaces:
			size, required_shapes = space
			row, col = size
			shape_size = sum([shapes[index] * required_shapes[index] for index in range(len(required_shapes))])
			space_size = row * col
			if shape_size > space_size:
				continue
			if shape_size * heuristic_constant > space_size:
				continue
			result += 1
		return result
		   
	def second_star(self, inp):
		# TODO implement me 
		...



def main():
	day = "12"
	cookies = {"session": "<SESSION_ID>"}
	
	solution = Solution(day=day, cookies=cookies)
		
	with Clock():
		solution.run()



if __name__ == "__main__":
    main()
