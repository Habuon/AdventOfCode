import requests
import time
from abc import ABC, abstractmethod

import networkx as nx


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
		edges = dict()
		for edge in inp.split("\n"):
			edge = edge.strip()
			if len(edge) == 0:
				continue
			
			src, dst =  edge.split(":")
			dst = [x.strip() for x in edge.split(" ") if len(x.strip()) > 0]
			edges[src] = edges.get(src, []) + dst
			
		return {"edges": edges}

	def first_star(self, inp):
		edges = inp["edges"]
		G = nx.DiGraph(edges)

		paths = list(nx.all_simple_paths(G, "you", "out"))
		return len(paths) 

	def second_star(self, inp):

		def count_all_paths_from_source(graph: nx.DiGraph, source: str) -> dict:
			# sort nodes into tree
			topological = list(nx.topological_sort(graph))

			dynamic_program = {node: 0 for node in topological}
			dynamic_program[source] = 1

			for node in topological:
				for successor in graph.successors(node):
					dynamic_program[successor] += dynamic_program[node]
			
			return dynamic_program


		def count_paths_containing_two_nodes(graph, source, target, point1, point2):
			# The graph must be a Direct Acyclic Graph for this algorithm to work
			if not nx.is_directed_acyclic_graph(graph):
				raise ValueError("Graph is not a DAG")

			# Count all paths from each required starting point
			dp_source = count_all_paths_from_source(graph, source=source)
			dp_point1 = count_all_paths_from_source(graph, source=point1)
			dp_point2 = count_all_paths_from_source(graph, source=point2)

			# Combine the counts using the formula
			order1 = dp_source[point1] * dp_point1[point2] * dp_point2[target]   # source → point1 → point2 → target
			order2 = dp_source[point2] * dp_point2[point1] * dp_point1[target]   # source → point2 → point1 → trget

			return order1 + order2


		edges = inp["edges"]
		G = nx.DiGraph(edges)

		result = count_paths_containing_two_nodes(graph=G, source="svr", target="out", point1="dac", point2="fft")
		return result


def main():
	day = "11"
	cookies = {"session": "<SESSION_ID>"}
	
	solution = Solution(day=day, cookies=cookies)
		
	with Clock():
		solution.run()


if __name__ == "__main__":
    main()
