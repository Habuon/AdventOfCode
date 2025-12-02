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
	session = None 
	day = None


	@classmethod
	def initialize(cls, day, cookies):
		cls.session = requests.Session()
		requests.utils.add_dict_to_cookiejar(cls.session.cookies, cookies)
		cls.day = day
	
	
	@classmethod
	@abstractmethod
	def process_input(cls, inp: str) -> dict:
		...
		   
		    
	@classmethod
	@abstractmethod
	def first_star(cls, inp):
		...
		    
		    
	@classmethod
	@abstractmethod
	def second_star(cls, inp):
		...
	
	
	@classmethod
	def get_input(cls) -> dict:
		if cls.session is None:
			raise ValueError("Improperly initialized")
			
		resp = cls.session.get(f"https://adventofcode.com/2025/day/{cls.day}/input")
		result = resp.content.decode()
		
		result = cls.process_input(result)
		return result


	@classmethod
	def submit_answer(cls, level, answer):
		while True:
		    resp = cls.session.post(f"https://adventofcode.com/2025/day/{cls.day}/answer", data={"level": level, "answer": answer})
		    content = resp.content.decode()
		    if "That's not the right answer" in content:
		        return False
		    if "You gave an answer too recently" in content:
		        print("[*] Response sent too soon after each other")
		        time.sleep(30)
		        continue
		    return True
		
		
	@classmethod
	def run(cls):
		inp = cls.get_input()
		first_answer = cls.first_star(inp)
		correct = cls.submit_answer(level=1, answer=first_answer)
		print(f"[*] First star result: {first_answer} ... {'correct' if correct else 'incorrect'}")
		if not correct:
			return False
			
		time.sleep(10)
		
		second_answer = cls.second_star(inp)
		correct = cls.submit_answer(level=2, answer=second_answer)
		print(f"[*] Second star result: {second_answer} ... {'correct' if correct else 'incorrect'}")
		
		return correct


class Solution(AocMeta):
	possible_numbers = set()

	@classmethod
	def process_input(cls, inp: str) -> dict:
		result = []
		inp = inp.strip()
		ranges = [[int(y) for y in x.split("-")] for x in inp.split(",")]
		max_number = max([x[1] for x in ranges])
		
		ranges = [set(range(int(x), int(y) + 1)) for x, y in ranges]
		
		return {"ranges": ranges, "max_number": max_number}
	
	@classmethod
	def _possible_numbers(cls, max_number: int, max_repeat: int) -> None:
		max_length = len(str(max_number))
		for num in range(1, 10**(1 + max_length // 2)):
			for rep in range(2, max_repeat + 1):
				repeated_number = int(f"{num}" * rep)
				if repeated_number > max_number:
					continue
				cls.possible_numbers.add(repeated_number)
		  
		  
	@classmethod
	def first_star(cls, inp: dict) -> int:
		ranges, max_number = inp["ranges"], inp["max_number"]
		
		cls._possible_numbers(max_number=max_number, max_repeat=2)
		
		result = 0
		for num_range in ranges:
			result += sum(num_range.intersection(cls.possible_numbers))		
			
		return result
			

	@classmethod
	def second_star(cls, inp: dict) -> int:
		ranges, max_number = inp["ranges"], inp["max_number"]
		
		max_repeat = len(str(max_number))
		cls._possible_numbers(max_number=max_number, max_repeat=max_repeat)
				
		result = 0
		for num_range in ranges:
			result += sum(num_range.intersection(cls.possible_numbers))		
		
		return result


def main():
	day = "2"
	cookies = {"session": "<SESSION_ID>"}
	
	Solution.initialize(day, cookies)
	
	with Clock():
		Solution.run()


if __name__ == "__main__":
    main()
