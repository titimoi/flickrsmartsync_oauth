from iptcinfo import IPTCInfo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
import os

logger = logging.getLogger("flickrsmartsync_oauth")

class Local(object):
    def __init__(self, cmd_args):
        self.cmd_args = cmd_args

    def build_photo_sets(self, path, extensions):
        # Build local photo sets
        photo_sets = {} # Dictionary
        skips_root = [] # List
        keywords = set(self.cmd_args.keyword) if self.cmd_args.keyword else ()

        for r, dirs, files in os.walk(path, followlinks=True):

            if self.cmd_args.starts_with and not r.startswith('{}{}'.format(self.cmd_args.sync_path, self.cmd_args.starts_with)):
                continue

            files = [f for f in files if not f.startswith('.')]
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                ext = file.lower().split('.').pop()
                if ext in extensions:
                    if r == self.cmd_args.sync_path:
                        skips_root.append(file)
                    else:
                        # If filtering by keyword...
                        if keywords:
                            file_path = os.path.join(r, file)

                            # Create object for file that may or may not (force=TRUE) have IPTC metadata.
                            info = IPTCInfo(file_path, force=True)

                            # intersection(*others): Return a new set with elements common to the set and all others.
                            matches = keywords.intersection(info.keywords)

                            if not matches:
                                # No matching keyword(s) found, skip file
                                logger.info('Skipped file [%s] because it does not match any keywords [%s].' % (file, list(keywords)))
                                continue

                        photo_sets.setdefault(r, [])
                        file_path = os.path.join(r, file)
                        file_stat = os.stat(file_path)
                        photo_sets[r].append((file, file_stat))

        if skips_root:
            logger.warning('Root photos are not synced to avoid disorganized flickr sets. Sync at the topmost level of your photos directory to avoid this warning.')
            logger.warning('Skipped files: %s.' % skips_root)
        return photo_sets

    def watch_for_changes(self, upload_func):
        logger.info('Monitoring [{}].'.format(self.cmd_args.sync_path))
        event_handler = WatchEventHandler(self.cmd_args.sync_path, upload_func)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.cmd_args.sync_path, recursive=True)
        self.observer.start()

    def wait_for_quit(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class WatchEventHandler(FileSystemEventHandler):
    sync_path = None

    def __init__(self, sync_path, upload_func):
        self.sync_path = sync_path.rstrip(os.sep)
        self.upload_func = upload_func

    # When a file is created...
    def on_created(self, event):
        super(WatchEventHandler, self).on_created(event)

        if not event.is_directory:
            self.upload_func(event.src_path)

    # When a file is moved...
    def on_moved(self, event):
        super(WatchEventHandler, self).on_moved(event)

        if not event.is_directory and os.path.dirname(event.dest_path).replace(self.sync_path, ''):
            self.upload_func(event.dest_path)

