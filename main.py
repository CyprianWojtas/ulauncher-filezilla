import json
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction

from fz_connections import filter_connections, get_filezilla_sites

logger = logging.getLogger(__name__)


class FileZillaExtension(Extension):

	def __init__(self):
		super(FileZillaExtension, self).__init__()
		self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

	def on_event(self, event, extension):
		items = []
		logger.info('preferences %s' % json.dumps(extension.preferences))

		connections = get_filezilla_sites()

		if connections is None:
			items.append(ExtensionResultItem(
				icon='images/icon.png',
				name='FileZilla configuration file not found',
				description='Please make sure FileZilla is installed to use this extension',
				on_enter=DoNothingAction()
			))
			return RenderResultListAction(items)

		for connection in filter_connections(connections, event.get_argument()):

			items.append(ExtensionResultItem(
				icon='images/icon.png',
				name=connection['name'],
				description=f"{connection['user']}@{connection['host']}",
				on_enter=RunScriptAction('filezilla -c "' + connection['path'].replace('\\', '\\\\').replace('"', '\\"') + '"')
			))

		return RenderResultListAction(items)


if __name__ == '__main__':
	FileZillaExtension().run()
