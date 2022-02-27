from pittapi import course

class Node:
	def __init__(self): 		# Default Constructor: Node()
		self.dept_code = ""		# str
		self.course_no = "" 	# str
		self.course_name = "" 	# str
		self.description = "" 	# str
		self.preqs = None 		# List[(Node, bool)]
		self.completed = False	# bool
		self.prereq_count = 0
	
	def __init__(self, course_obj): 	# Overloaded constructor: Node(course_obj)
		self.dept_code = course_obj.subject_code
		self.course_no = course_obj.course_number
		self.course_title = course_obj.course_title
		self.section_details = course.get_extra_section_details(section=course_obj.sections[0], term=course_obj.sections[0].term, class_number=self.course_no)
		self.description = self.section_details.description
		# self.preqs = self.parse_preqs(section_details.preqs)
		self.completed = False
		self.prereq_count = 0

	def __str__(self):		# toString() of Node
		return self.dept_code + " " + self.course_no

	def toJSON(self):		# Convert Node to JSON format
		return {
			"dept_code" : self.dept_code,
			"id" : self.course_no, 				# can change back to course_no, would need to modify js code
			"course_title" : self.course_title,
			"description" : self.description,
			"completed" : self.completed,
			"prereq_count" : self.prereq_count
		}
	
	def parse_preqs(self, preqs):
		listOfReqs = []
		someAndList = [True]
		someOrList = [False]
		dept_code_len = len(dept_code)
		preqs_string = dict[num].section_details.preqs
		for i in range(len(preqs_string)-dept_code_len):
			# We have reached the end of the string
			if preqs_string[i] == ';':
				break
			# contains parentheses first
			if preqs_string[i] == '(':
				# create an innerlist 
				# ASSUMES THAT EVERY PARENTHESES BEGINNING WITH AN '(' ENDS WITH AN ')'
				while preqs_string[i] != ')':
					if i + 1 + dept_code_len >= len(preqs_string)-dept_code_len:
						break
					if preqs_string[i+1:i+1+dept_code_len] == dept_code:
						i += 1
						code = preqs_string[i+dept_code_len+1:i+dept_code_len+5]
						i = i+dept_code_len+6

						# Case where we add the last course in the string
						if i >= len(preqs_string)-dept_code_len:
							if len(someAndList) > 1:
								someAndList += [code] 
							elif len(someOrList) > 1:
								someOrList += [code]
							break
					# Question: Can both lists contain code at the same time?
						if preqs_string[i:i+3] == 'and' and code not in someAndList:
							someAndList += [code]
						if preqs_string[i:i+2] == 'or' and code not in someOrList:
							someOrList += [code] # [False, CS 0441, CS 0406]
					else:
						i += 1
				if len(someAndList) > 1:
					#someAndList = [someAndList]
					listOfReqs.append(someAndList)
				if len(someOrList) > 1:
					#someOrList = [someOrList] # [False, CS 0441, CS 0406]
					listOfReqs.append(someOrList)
				# Resets And and Or Lists Values
				someAndList = [True]
				someOrList = [False]
				
			# contains non-parentheses first
			elif preqs_string[i:i+dept_code_len] == dept_code:
				code = preqs_string[i+dept_code_len+1:i+dept_code_len+5]
				# append to listOfReqs
		return listOfReqs 

		def outer_paran_parse_preqs(listOfReqs, someAndList, someOrList, dept_code_len, preqs_string, ):
			while preqs_string[i] != ';':
				for i in range(len(preqs_string) - dept_code_len):
					if preqs_string[i] == ')': 
						if i + 2 < (len(preqs_string) - dept_code_len):
							if preqs_string[i + 2] == 'a':
								pass

				
			

				



			# Matches dept_code --> Ex: 1501 --> (CS 0441 or CS 0406) and (CS 0445 or CS 0455 or COE 0445), match "CS" so code is "0441", "0406", etc
			if preqs_string[i:i+dept_code_len] == dept_code:
				code = preqs_string[i+dept_code_len+1:i+dept_code_len+5]
				# Add 1501 node (dependent) to 445 parent (prereq) in dict
				if code in dict:
					self.add_node_ele(dict[code], dict[num])

class Graph:	# Graph class
	# Adjacency list: key is parent node (prereq), value is list of nodes (courses that need prereq)
	def __init__(self, term="", dept_code=""):
		# Empty graph
		if term == "" and dept_code == "":
			self.adjacency_list = {}
			self.course_map = {}
		# Fill graph with courses from term and department
		else:
			self.adjacency_list = {}
			self.course_map = self.fill_dict(term, dept_code)
			self.term = term

	# Add parent node as prereq to list of nodes that is initially empty (Ex: Add 445 node to graph)
	def add_list_ele(self, node):
		self.adjacency_list[node] = []

	# Add parent node as prereq with a node that needs parent as prereq (Ex: 445 prereq adds 1501 to list of nodes)
	def add_node_ele(self, prereq, node):
		self.adjacency_list[prereq].append(node)

	# toString() of	Graph, prints (key, value) pairs of prereq and list of dependent nodes
	def __str__(self):
		output = ""
		for key, val in self.adjacency_list.items():
			output += "{" + str(key) + " : ["
			for node in val:
				output += str(node) + ", "
			output += "]}\n"
		return output

	# Fill dictionary with courses in particular term and department
	def fill_dict(self, term, dept_code):
		dict = {} 

		# Iterate thru course_num and course_obj of courses in a specific term/department
		for num, obj in course.get_courses(term, dept_code).courses.items():
			# Do not account for grad level courses (above 2000)
			if int(num[0:4]) >= 2000:
				return dict
			# If valid, map course_num to node (course_obj)
			try:
				dict[num] = Node(obj)
			except TypeError:
				print("type error on class", num)
				continue
			
			# Add node to graph (just prereq, no dependent nodes)
			self.add_list_ele(dict[num])

			# Ex: "CS" has length 2, preqs_string of "441" has full str of all prereqs for "441"
			dept_code_len = len(dept_code)
			preqs_string = dict[num].section_details.preqs

			# Loop through preqs_string
			for i in range(len(preqs_string)-dept_code_len):
				# Reached the end of the available prereqs in string
				if preqs_string[i] == ';':
					break
				# Match dept_code --> Ex: 1501 is (CS 0441 or CS 0406) and (CS 0445 or CS 0455 or COE 0445)
				# Would match "CS" so code is "0441", "0406", etc
				if preqs_string[i:i+dept_code_len] == dept_code:
					code = preqs_string[i+dept_code_len+1:i+dept_code_len+5]
					# Add 1501 node (dependent) to 445 parent (prereq) in dict assuming 445 exists as prereq in dictionary
					if code in dict:
						self.add_node_ele(dict[code], dict[num])
						dict[num].prereq_count += 1
			print(num, dict[num].prereq_count)
		return dict

	# Convert Graph to JSON format
	def toJSON(self):
		nodes = []
		for entry in self.course_map.values():
			nodes.append(entry.toJSON())
		links = []
		for key, value in self.adjacency_list.items():
			for ele in value:
				links.append({"source":key.course_no, "target":ele.course_no})
		# return {
		# 	"nodes" : [ entry.toJSON() for entry in course_map.values() ],
		# 	"links" : [ { "source": key, "target": value.course_no} for key, value in adjacency_list.items() ]
		# }
		return { "nodes" : nodes, "links" : links }


