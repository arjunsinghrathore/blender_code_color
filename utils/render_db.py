#!/usr/bin/env python
import os
from .logging import announce
from pymongo import MongoClient
from datetime import datetime
from .dictionaries import replace_in_nested_dict
import sshtunnel

sshtunnel.DAEMON = True  # Prevent hanging process due to forward thread
from config import db_use_tunnel, db_username, db_keyfile, db_name, db_collection, db_port, db_ip, db_host

# DB holder class: Keeps max one DB open
class RenderDB:
    __loaded_db = None
    __reference_count = 0

    def __init__(self):
        self.client = None
        self.database = None
        self.collection = None
        self.forward = None

    def __enter__(self):
        if RenderDB.__loaded_db is None:
            self.client, self.database, self.collection, self.forward = self.__open_db()
            RenderDB.__loaded_db = self
        else:
            self.client = RenderDB.__loaded_db.client
            self.database = RenderDB.__loaded_db.database
            self.collection = RenderDB.__loaded_db.collection
            self.forward = RenderDB.__loaded_db.forward
        RenderDB.__reference_count += 1
        return RenderDB.__loaded_db

    def __exit__(self, exc_type, exc_value, traceback):
        RenderDB.__reference_count -= 1
        if not RenderDB.__reference_count:
            if self.forward is not None:
                self.forward.close()
            RenderDB.__loaded_db = None
        self.collection = None
        self.database = None
        self.client = None
        self.forward = None
        return False

    def __open_db(self):
        if db_use_tunnel:
            forward = sshtunnel.SSHTunnelForwarder((db_host, 22),
                                                   remote_bind_address=(db_ip, db_port),
                                                   ssh_username=db_username,
                                                   ssh_pkey=db_keyfile)
            forward.start()
            port = forward.local_bind_port
            announce("Bound on port {0}".format(port))
        else:
            forward = None
            port = 27017
        client = MongoClient('localhost', port)
        client.forward = forward  # Put port forward reference into mongoclient scope so they are deleted together
        database = client[db_name]
        collection = database[db_collection]
        # Perform one operation on DB to cause early fail if connection isn't working
        announce("{0} entries in DB.".format(collection.count()), '~', force=True)
        return client, database, collection, forward

    def save_entry(self, render_condition, render_filename):
        def get_relative_resource_path(path):
            return os.path.relpath(path, render_condition['resources_path'])

        def replace_with_relative_path(key):
            replace_in_nested_dict(render_condition, [key] + ['parameters', 'files'], get_relative_resource_path)
            replace_in_nested_dict(render_condition, [key] + ['parameters', 'directory'], get_relative_resource_path)

        for resource in ['model','material','background']:
            replace_with_relative_path(resource)

        timestamp = datetime.fromtimestamp(render_condition['time'])

        # save the new collection in the mongoDB database
        col = {"filepath": render_filename, "condition": render_condition, "timestamp": timestamp}
        self.collection.insert(col)

        announce('Entry saved in DB')
