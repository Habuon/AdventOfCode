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

		second_answer = self.second_star(inp)
		correct = self.submit_answer(level=2, answer=second_answer)
		print(f"[*] Second star result: {second_answer} ... {'correct' if correct else 'incorrect'}")
		
		return correct


class Solution(AocMeta):
	def process_input(self, inp: str) -> dict:
		array = [list(row) for row in inp.split("\n") if len(row.strip()) != 0]
		splitters = [(row, col) for row in range(len(array)) for col in range(len(array[row])) if array[row][col] == "^"]
		start = [(row, col) for row in range(len(array)) for col in range(len(array[row])) if array[row][col] == "S"][0]

		splitters_dict = dict()
		for splitter in splitters:
			row, col = splitter
			splitters_dict[row] = splitters_dict.get(row, []) + [col]
		
		splitters_cols = dict()
		for splitter in splitters:
			row, col = splitter
			splitters_cols[col] = splitters_cols.get(col, []) + [row]

		return {"array": array, "splitters": splitters_dict, "start": start, "splitters_cols": splitters_cols}
		   
	def first_star(self, inp):
		array, splitters, start = inp["array"], inp["splitters"], inp["start"]
		
		result = 0
		beams = {start[1]}
		for row in range(1, len(array)):
			new_beams = set(beams)
			splitted_beams = beams.intersection(set(splitters.get(row, [])))
			result += len(splitted_beams)
			new_beams -= splitted_beams
			new_beams = new_beams.union({beam + 1 for beam in splitted_beams}.union({beam - 1 for beam in splitted_beams}))
			beams = set(new_beams)
			
		return result
		   
	def second_star(self, inp):
		array, splitters, start, splitters_cols = inp["array"], inp["splitters"], inp["start"], inp["splitters_cols"]

		cache = dict()

		def possible_routes(start_row, start_col):
			if start_row in cache and start_col in cache[start_row]:
				return cache[start_row][start_col]
			if all([x < start_row for x in splitters_cols.get(start_col, [])]):
				return 1
			else:
				split_rows = [x for x in splitters_cols.get(start_col, []) if x > start_row]
				split_row = min(split_rows)
				right = possible_routes(start_row=split_row, start_col=start_col + 1)
				left = possible_routes(start_row=split_row, start_col=start_col - 1)
				cache[start_row] = cache.get(start_row, dict())
				cache[start_row][start_col] = left + right
				return cache[start_row][start_col]

		start_row, start_col = start
		result = possible_routes(start_row=start_row, start_col=start_col)

		return result



def main():
	day = "7"
	cookies = {"session": "<SESSION_ID>"}
	
	solution = Solution(day=day, cookies=cookies)
		
	with Clock():
		solution.run()



if __name__ == "__main__":
    main()
