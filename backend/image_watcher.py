import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from storage import read_images

class ImageDirectoryWatcher(FileSystemEventHandler):
    def __init__(self, websocket):
        self._websocket = websocket
        self._image_event = asyncio.Event()

    # Override event handlers...

    async def watch_directory(self):
        while True:
            await self._image_event.wait()
            await self._websocket.send_json(read_images())
            self._image_event.clear()

def start_watcher(path: str):
    watcher = ImageDirectoryWatcher()
    observer = Observer()
    observer.schedule(watcher, path, recursive=True)
    observer.start()
    return watcher
