from xml.etree import ElementTree
from datetime import datetime

"""
	debates major-heading minor-heading speech
	division divisioncount memberlist member
	dt dd p li ul
"""


class Hansard(object):
	def __init__(self, filename):
		self.filename = filename
		
def _parse_xml_file(filename):
	tree = ElementTree.parse(filename)
	old = False
	if old:
		for node in tree.getiterator():
	#		print node.tag,
			if node.tag == "debates":
				node.filename = filename
				_parse_debate(node)
			else:
				print node.tag

	else:

		for debate in tree.iter("debate"):
			print debate


def _parse_debate(debate):
	for node in debate.getiterator():
		print node.tag


def _parse_debate_old(debate):
	major = minor = None
	for node in debate.getiterator():
		if node.tag == "major-heading":
			major = node
			if "BILL" in major.text:
				major.filename = debate.filename
				major.bill = True
			else:
				major.bill = False
				print "Bill"
			#else:
			#	print "%s %s" % (major.tag, major.text.strip())
		elif node.tag == "minor-heading":
			minor = node
			if "BILL" in major.text:
				print "%s %s" % (minor.tag, minor.text.strip())
		elif node.tag == "speech":
			_parse_speech(node, major, minor)
		elif node.tag == "division":
			_parse_division(node, major, minor)
		else:
		#	print node.tag,
			pass	


"""
<speech id="uk.org.publicwhip/lords/2006-02-07.6.1" speakerid="uk.org.publicwhip/lord/100116" speakername="Rod Kemp" time="13:00:00" url="http://parlinfo.aph.gov.au/parlInfo/search/display/display.w3p;query=Id:chamber/hansards/2006-02-07/0000">
"""
def _parse_speech(speech, major=None, minor=None):
	if major.bill:
		for node in speech.getiterator():
			if node.tag == "speech":
				print "speech %s" % node.tag
				if "speakerid" in node.attrib:
					speaker = Speaker(speaker_id=node.attrib["speakerid"], speaker_name=node.attrib["speakername"])
					#print node.attrib
					print speaker
				else:
					speaker = Speaker()

				aph_id = node.attrib['id']
				time = node.attrib['time']
				filename = major.filename
				speach_date = filename[:-4]
				speach_date = datetime.date(speach_date.split("-"))
				d = date, time
				print d
				print speaker.speaker_hash
				url = node.attrib['url']

				this_speech = Speech(speaker_hash=speaker.speaker_hash, aph_id=aph_id, datetime=time, url=url)

	pass


"""
<division divdate="2006-02-07" divnumber="1" id="uk.org.publicwhip/debate/2006-02-07.33.1" nospeaker="true" time="16:32:00" url="http://parlinfo.aph.gov.au/parlInfo/search/display/display.w3p;query=Id:chamber/hansardr/2006-02-07/0000">

division divisioncount
<divisioncount ayes="34" noes="38" tellerayes="1" tellernoes="1"/>

division memberlist
<memberlist vote="aye">

division member
<member id="uk.org.publicwhip/lord/100003" vote="aye">Lyn Fay Allison</member>
"""
def _parse_division(division, major=None, minor=None):
	for node in division.getiterator():
		# print "division %s" % node.tag
		pass


class Speaker(object):
	def __init__(self, speaker_id="", speaker_name=""):
		self.speaker_name = speaker_name.strip()
		self.speaker_id = speaker_id.strip()
		self.generate_hash()

	def __str__(self):
		return self.speaker_name
	
	def generate_hash(self):
		import hashlib
		m = hashlib.sha1()
		m.update(self.speaker_id+self.speaker_name)
		self.speaker_hash = m.hexdigest()

	"""
		Save to db and return speaker id
	"""
	def put(self):
		return None

	"""
		Retrieve a speaker from the db
	"""
	def get(self):
		return None


class Speech(object):
	def __init__(self, speaker_hash, aph_id, datetime, url):
		pass


def test():
	# source = "2006-02-07.xml"
	source = "2011-06-01.xml"
	_parse_xml_file(source)


test()