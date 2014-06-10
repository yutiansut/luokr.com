import os, re, time, random, base64, collections
try:
    import hashlib
    sha1 = hashlib.sha1
except ImportError:
    import sha
    sha1 = sha.new

try:
    import cPickle as pickle
except ImportError:
    import pickle

class Session(collections.MutableMapping):
    expired_lifetime = 86400
    cleanup_interval = 86400
    _lastime_cleanup = time.time()

    def __init__(self, sess_id = None, storage = None):
        if storage is None:
            storage = Storage()
        self._storage = storage

        if sess_id is None:
            sess_id = self.build_sess_id()
        assert self.valid_sess_id(sess_id)
        self._sess_id = sess_id

        if self._sess_id in self._storage:
            self._session = self._storage[self._sess_id]
        else:
            self._session = {}

    def build_sess_id(self):
        if time.time() - Session._lastime_cleanup > Session.cleanup_interval:
            Session._lastime_cleanup = time.time()
            self.clear_expired(Session.expired_lifetime)

        while True:
            sess_id = sha1("%s%s" %(os.urandom(16), time.time()))
            sess_id = sess_id.hexdigest()
            if sess_id not in self._storage:
                return sess_id

    def valid_sess_id(self, sess_id):
        return re.compile('^[0-9a-fA-F]+$').match(sess_id)

    def fetch_sess_id(self):
        return self._sess_id

    def store_session(self):
        self._storage[self._sess_id] = self._session

    def clear_session(self):
        self._session = {}
        self.store_session()

    def clear_expired(self, secs):
        self._storage.cleanup(secs)

    def __repr__(self):
        return '<sess_id: %s session: %s>' % (self._sess_id, self._session)

    def __getitem__(self, key):
        return self._session[key]

    def __setitem__(self, key, value):
        self._session[key] = value

    def __delitem__(self, key):
        del self._session[key]

    def keys(self):
        return self._session.keys()

    def __iter__(self):
        return self._session.__iter__()

    def __len__(self):
        return len(self._session.keys())

class Storage:
    def __init__(self, root = '/tmp'):
        self.root = root
        if not os.path.exists(self.root):
            os.mkdir(self.root)

    def __contains__(self, name):
        path = self._locate(name)
        return os.path.exists(path)

    def __getitem__(self, name):
        path = self._locate(name)
        if os.path.exists(path):
            return self._decode(open(path).read())
        else:
            raise KeyError, name

    def __setitem__(self, name, value):
        try:
            file = open(self._locate(name), 'w')
            try:
                file.write(self._encode(value))
            finally:
                file.close()
        except IOError:
            pass

    def __delitem__(self, name):
        path = self._locate(name)
        if os.path.exists(path):
            os.remove(path)

    def cleanup(self, secs):
        now = time.time()
        for name in filter(lambda x: x.endswith(self._suffix()), os.listdir(self.root)):
            path = os.path.join(self.root, name)
            if os.path.exists(path) and now - os.stat(path).st_atime > secs:
                os.remove(path)

    def _suffix(self):
        return '.sess'

    def _locate(self, name):
        if os.path.sep in name:
            raise ValueError, "Bad name: %s" % repr(name)
        return os.path.join(self.root, name + self._suffix())

    def _encode(self, sess):
        return base64.encodestring(pickle.dumps(sess))

    def _decode(self, data):
        return pickle.loads(base64.decodestring(data))

