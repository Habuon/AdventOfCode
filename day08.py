import requests
import time
import math
import uuid
from abc import ABC, abstractmethod


def compute_distances(points):
	distances = dict()
	for i in range(len(points)):
		for j in range(i+1, len(points)):
			x1,y1,z1 = points[i]
			x2,y2,z2 = points[j]
			d = math.dist((x1,y1,z1),(x2,y2,z2))
			
			distances[i] = distances.get(i, dict())
			distances[i][j] = d
			
			distances[j] = distances.get(j, dict())
			distances[j][i] = d
	return distances


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
	def process_input(self, inp: str) -> dict:
		boxes = []
		for line in inp.split("\n"):
			if len(line.strip()) == 0:
				continue
			x, y, z = [int(i) for i in line.strip().split(",")]
			boxes.append((x, y, z))
			
		distances = compute_distances(boxes)
		sorted_points = [(p1, p2) for p1, p2, _ in sorted(((p1, p2, v) for p1, dd in distances.items() for p2, v in dd.items()), key=lambda x: x[2])]
		sorted_points = [sorted_points[i] for i in range(len(sorted_points)) if i % 2 == 0]
			
		return {"boxes": boxes, "distances": compute_distances(boxes), "sorted_points": sorted_points}
		   
	def first_star(self, inp):
		circuits = dict()
		boxes, distances, sorted_points = inp["boxes"], inp["distances"], inp["sorted_points"]
				
		circuits = {str(uuid.uuid4()) : [index] for index in range(len(boxes))}
		
		step = 0
		while step < 1000:
			pair = sorted_points.pop(0)
			p1, p2 = pair
			
			circuit_uuid1 = [key for key in circuits.keys() if p1 in circuits[key]][0]
			circuit_uuid2 = [key for key in circuits.keys() if p2 in circuits[key]][0]
			
			if circuit_uuid1 != circuit_uuid2:
				circuits[circuit_uuid1] += circuits.pop(circuit_uuid2)			
			
			step += 1
			
		result = math.prod(sorted([len(x) for x in circuits.values()], reverse=True)[:3])		
		return result
		
		
		   
	def second_star(self, inp):
		circuits = dict()
		boxes, distances, sorted_points = inp["boxes"], inp["distances"], inp["sorted_points"]
				
		circuits = {str(uuid.uuid4()) : [index] for index in range(len(boxes))}
		
		last_connected = None
		
		while len(sorted_points) != 0:
			pair = sorted_points.pop(0)
			p1, p2 = pair
			
			circuit_uuid1 = [key for key in circuits.keys() if p1 in circuits[key]][0]
			circuit_uuid2 = [key for key in circuits.keys() if p2 in circuits[key]][0]
			
			if circuit_uuid1 != circuit_uuid2:
				last_connected = pair
				circuits[circuit_uuid1] += list(circuits[circuit_uuid2])
				circuits.pop(circuit_uuid2)
		p1, p2 = last_connected
		
		return boxes[p1][0] * boxes[p2][0]



def main():
	day = "8"
	cookies = {"session": "<SESSION_ID>"}
	
	solution = Solution(day=day, cookies=cookies)
		
	with Clock():
		solution.run()



if __name__ == "__main__":
    main()
