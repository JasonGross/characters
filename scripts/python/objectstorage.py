#!/usr/bin/python
# Filename: objectstorage.py
from __future__ import with_statement
import os
import datetime
import tempfile
try:
    import cPickle as pickle
except ImportError:
    import pickle
from library import touch

__all__ = ['get_object', 'register_save_object_callback', 'save_object',
           'get_object_file_name', 'set_default_object_directory',
           'timestamp_object', 'get_timestamp']

_default_object_storage_directory = tempfile.gettempdir()
_save_object_call_backs = {}

def set_default_object_directory(new_directory):
    global _default_object_storage_directory
    _default_object_storage_directory = new_directory

def register_save_object_callback(object_name, method):
    if object_name not in _save_object_call_backs:
        _save_object_call_backs[object_name] = []
    _save_object_call_backs[object_name].append(method)

def timestamp_object(object_name, timestamp_dir=None):
    if not timestamp_dir:
        touch(os.path.join(_default_object_storage_directory, object_name + '.timestamp.txt'))
    else:
        if os.path.exists(timestamp_dir):
            touch(os.path.join(timestamp_dir, object_name + '.timestamp.txt'))
            update_directory_timestamp(timestamp_dir)

def update_directory_timestamp(timestamp_dir):
    if os.path.exists(timestamp_dir):
        touch(os.path.join(timestamp_dir, 'timestamp.txt'))

def get_timestamp(object_name, timestamp_dir=None):
    if not timestamp_dir: timestamp_dir = _default_object_storage_directory
    path = os.path.join(timestamp_dir, object_name + '.timestamp.txt')
    if os.path.exists(path):
        return os.stat(os.path.join(timestamp_dir, object_name + '.timestamp.txt')).st_atime
    else:
        return None

def get_object(object_name, object_maker, timestamp_dir=None, is_old=None, protocol=0):
    file_name = get_object_file_name(object_name)
    timestamp = get_timestamp(object_name, timestamp_dir=timestamp_dir)
    if os.path.exists(file_name) and timestamp:
        version = os.stat(file_name).st_atime
        if version >= timestamp:
            try:
                with open(file_name, 'rb') as f:
                    obj = pickle.load(f)
                if is_old is None or not is_old(obj):
                    return obj
            except (IOError,): # add more as needed
                pass
    obj = object_maker()
    save_object(object_name, obj, timestamp_dir=timestamp_dir, protocol=protocol)
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f, protocol=protocol)
    return obj

def save_object(object_name, obj, timestamp_dir=None, protocol=0):
    timestamp_object(object_name, timestamp_dir)
    with open(get_object_file_name(object_name), 'wb') as f:
        pickle.dump(obj, f, protocol=protocol)
    if object_name in _save_object_call_backs:
        for method in _save_object_call_backs[object_name]:
            method()
    return obj

def get_object_file_name(object_name):
    return os.path.join(_default_object_storage_directory, object_name + '.obj')
