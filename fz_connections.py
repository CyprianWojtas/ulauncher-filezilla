import os
from pathlib import Path

from xml.dom import minidom

def get_filezilla_sites():
	path = os.path.join(Path.home(), '.config/filezilla/sitemanager.xml')
	dom = minidom.parse(path)
	elements = dom.getElementsByTagName('Server')
	
	servers = []
	
	for server in elements:
		name = server.getElementsByTagName('Name')[0].firstChild.nodeValue
		host = server.getElementsByTagName('Host')[0].firstChild.nodeValue
		user = server.getElementsByTagName('User')[0].firstChild.nodeValue

		parent_node = server.parentNode
		folder = []

		while parent_node.nodeName == 'Folder':
			folder.insert(0, parent_node.firstChild.nodeValue)
			parent_node = parent_node.parentNode

		folder = '/'.join(folder) + '/' if folder else ''

		servers.append({
			'name': name,
			'host': host,
			'user': user,
			'path': '0/' + folder + name
		})
	
	return servers




def sort_connections(connection, text):
	"""
	Sort connections based on the provided text.
	"""

	order = ''

	if connection['name'].lower().startswith(text.lower()):
		order = '0'
	elif text.lower() in connection['name'].lower():
		order = '1'
	elif connection['host'].lower().startswith(text.lower()):
		order = '2'
	elif text.lower() in connection['host'].lower():
		order = '3'
	else:
		order = '4'
	
	order += connection['name']
	
	return order


def filter_connections(connections, filter_text):
	"""
	Filter connections based on the provided filter text.
	"""
	if not filter_text:
		return connections

	filtered_connections = []

	for connection in connections:
		if filter_text.lower() in connection['name'].lower() or filter_text.lower() in connection['host'].lower():
			filtered_connections.append(connection)
	

	filtered_connections = sorted(filtered_connections, key=lambda x: sort_connections(x, filter_text))

	return filtered_connections


if __name__ == '__main__':
	print(get_filezilla_sites())
