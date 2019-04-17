import unittest
from SI507project_tools import *


class Test1(unittest.TestCase):
	def test_university_type1(self):
		uni1 = data.get('The George Washington University')
		self.assertEqual(type(uni1), dict)

	def test_university_type2(self):
		uni2 = data.get('Wesleyan University')
		self.assertEqual(type(uni2), dict)

	def test_university_type3(self):
		uni3 = data.get('Yale University')
		self.assertEqual(type(uni3), dict)


class Test2(unittest.TestCase):
	def test_course1(self):
		uni1 = data.get('University of Arizona')
		courses = ["Astrobiology: Exploring Other Worlds", "Introduction to the Orbital Perspective", "Biosphere 2 Science for the Future of Our Planet", "Roman Art and Archaeology", "Astronomy: Exploring Time and Space"]
		self.assertEqual(uni1['courses'],courses)

	def test_course2(self):
		uni2 = data.get('New Teacher Center')
		courses =["Blended Learning: Personalizing Education for Students"]
		self.assertEqual(uni2['courses'],courses)

	def test_course3(self):
		uni3 = data.get('Cisco')
		courses = ["Cisco Networking Basics Specialization"]
		self.assertEqual(uni3['courses'],courses)


class Test3(unittest.TestCase):
	def test_instructor1(self):
		uni1 = data.get('H2O')
		instructors = ["Darren Cook"]
		self.assertEqual(uni1['instructors'],instructors)

	def test_instructor2(self):
		uni2 = data.get('University of Kentucky')
		instructors =["Dr. Allison Soult", "Dr. Kim Woodrum"]
		self.assertEqual(uni2['instructors'],instructors)

	def test_instructor3(self):
		uni3 = data.get('Palo Alto Networks')
		instructors = ['James Dalton']
		self.assertEqual(uni3['instructors'],instructors)




