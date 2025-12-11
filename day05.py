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
		submit = True
		correct = False
		inp = self.get_input()
		
		first_answer = self.first_star(inp)
		if submit:
			correct = self.submit_answer(level=1, answer=first_answer)
			print(f"[*] First star result: {first_answer} ... {'correct' if correct else 'incorrect'}")
			if not correct:
				return False
				
			time.sleep(10)
		else:
			print(f"[*] First star result: {first_answer}")
		
		second_answer = self.second_star(inp)
		if submit:
			correct = self.submit_answer(level=2, answer=second_answer)
			print(f"[*] Second star result: {second_answer} ... {'correct' if correct else 'incorrect'}")
		else:
			print(f"[*] Second star result: {second_answer}")
		
		return correct


class Solution(AocMeta):
	def process_input(self, inp: str) -> dict:
		ranges = []
		ingrediences = set()
		
		for line in inp.split("\n"):
			line = line.strip()
			if len(line) == 0:
				continue
			if "-" in line:
				ranges.append([int(x) for x in line.split("-")])
			else:
				ingrediences.add(int(line))
		
		return {"ranges": self._remove_overlaps(ranges), "ingrediences": ingrediences}
		

	def _remove_overlaps(self, array: list) -> list:
		sorted_array = sorted(array, key=lambda x: x[0])	
		new_array = []
		new_item = sorted_array[0]
		
		for index in range(1, len(sorted_array)):
			lower, upper = new_item
			next_lower, next_upper = sorted_array[index]
			if next_lower <= upper:
				new_item = (lower, max(upper, next_upper))
			else:
				new_array.append(new_item)
				new_item = sorted_array[index]
		
		new_array.append(new_item)
		return new_array
			
		   
	def first_star(self, inp: dict) -> int:
		ingrediences, ranges = inp["ingrediences"], inp["ranges"]
		fresh = 0
		
		for number_range in ranges:
			to_remove = set()
			lower, upper = number_range
			
			for ingredient in ingrediences:
				if lower <= ingredient <= upper:
					to_remove.add(ingredient)
			
			ingrediences -= to_remove
			fresh += len(to_remove)
			if len(ingrediences) == 0:
				break

		return fresh

		   
	def second_star(self, inp: dict) -> int:
		ingrediences, ranges = inp["ingrediences"], inp["ranges"]
		result = sum([y - x + 1 for x,y in ranges])
		return result


def main():
	day = "5"
	cookies = {"session": "<SESSION_ID>"}
	
	solution = Solution(day=day, cookies=cookies)
		
	with Clock():
		solution.run()



if __name__ == "__main__":
    main()
