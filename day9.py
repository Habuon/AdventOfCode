import requests
import time
from abc import ABC, abstractmethod

from shapely.geometry import Polygon, box


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
			
		time.sleep(10)
		
		second_answer = self.second_star(inp)
		correct = self.submit_answer(level=2, answer=second_answer)
		print(f"[*] Second star result: {second_answer} ... {'correct' if correct else 'incorrect'}")
		
		return correct


class Solution(AocMeta):
	def _compute_area(self, point1, point2):
		row1, col1 = point1
		row2, col2 = point2

		delta_row, delta_col = abs(row1 - row2) + 1, abs(col1 - col2) + 1
		return delta_row * delta_col


	def process_input(self, inp: str) -> dict:
		tiles = list()
		for line in inp.split("\n"):
			if len(line.strip()) == 0:
				continue
			row, col = [int(x) for x in line.strip().split(",")]
			tiles.append((row, col))
		squares = dict()

		for index1 in range(len(tiles)):
			for index2 in range(index1 + 1, len(tiles)):
				area = self._compute_area(tiles[index1], tiles[index2])
				squares[index1] = squares.get(index1, dict())
				squares[index1][index2] = area
		
		best_points = [(p1, p2, v) for p1, p2, v in sorted(((p1, p2, v) for p1, dd in squares.items() for p2, v in dd.items()), key=lambda x: x[2], reverse=True)]

		return {"tiles": tiles, "squares": squares, "best_points": best_points}
			   
	def first_star(self, inp):
		tiles, squares, best_points = inp["tiles"], inp["squares"], inp["best_points"]

		point1, point2, area = best_points[0]

		return area
		   
	def second_star(self, inp):		
		tiles, squares, best_points = inp["tiles"], inp["squares"], list(inp["best_points"])

		poly = Polygon(tiles)

		while len(best_points) != 0:
			point1, point2, area = best_points.pop(0)
			row1, col1 = tiles[point1]
			row2, col2 = tiles[point2]

			rect = box(min(row1, row2), min(col1, col2), max(row1, row2), max(col1, col2))
			if poly.contains(rect) or poly.touches(rect):
				return area
			



def main():
	day = "9"
	cookies = {"session": "<SESSION_ID>"}
	
	solution = Solution(day=day, cookies=cookies)
		
	with Clock():
		solution.run()



if __name__ == "__main__":
    main()
