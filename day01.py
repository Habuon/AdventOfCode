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
	@classmethod
	def process_input(cls, inp: str) -> dict:
		result = []
		for line in inp.split("\n"):
			line = line.strip()
			if len(line) == 0:
				continue
			direction, number = line[0], int(line[1:])
			result.append((direction, number))
		return {"turns": result}
		   

	@classmethod
	def first_star(cls, inp) -> int:
		current = 50
		turns = inp["turns"]
		result = 0
		
		for turn in turns:
			direction, number = turn
			current = (current + number if direction == "R" else current - number) % 100
			if current == 0:
				result += 1
		return result
			

	@classmethod
	def second_star(cls, inp):
		current = 50
		previous = current
		turns = inp["turns"]
		result = 0
		
		for turn in turns:
			direction, number = turn
			previous = current
			current = current + number if direction == "R" else current - number
						
			delta = (abs(current) // 100)
			if previous > 0 and current < 0:
				delta += 1
			elif previous < 0 and current > 0:
				delta += 1
			elif current == 0:
				delta += 1
			
			result += delta
			
			current %= 100
		return result


def main():
	day = "1"
	cookies = {"session": "<SESSION_ID>"}
	
	Solution.initialize(day, cookies)
	
	with Clock():
		Solution.run()


if __name__ == "__main__":
    main()
