""" Image directory watcher. """
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from storage import read_images

class ImageDirectoryWatcher(FileSystemEventHandler):
    """ A class that watches the image directory for changes 
    and notifies the WebSocket when a new image is added. """
    def __init__(self, websocket):
        self._websocket = websocket
        self._image_event = asyncio.Event()

    # Override event handlers...

    async def watch_directory(self):
        """ A coroutine that watches the image directory for changes 
        and notifies the WebSocket when a new image is added. """
        while True:
            await self._image_event.wait()
            await self._websocket.send_json(read_images())
            self._image_event.clear()

def start_watcher(path: str) -> ImageDirectoryWatcher:
    """ Start a new image directory watcher. """
    watcher = ImageDirectoryWatcher()
    observer = Observer()
    observer.schedule(watcher, path, recursive=True)
    observer.start()
    return watcher
