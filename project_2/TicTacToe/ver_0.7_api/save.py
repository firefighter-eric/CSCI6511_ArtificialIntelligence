import pickle


class Save:
    def __init__(self, n, m, permission):
        self.filename = 'dict_n' + str(n) + '_m' + str(m)
        self.PERMISSION = permission

    def save(self, *objects):
        if not self.PERMISSION:
            return False
        out = objects[0]
        for o in objects[1:]:
            out.D.update(o.D)
        file = open(self.filename, 'wb')
        pickle.dump(out, file)
        file.close()
        return True

    def load(self):
        if not self.PERMISSION:
            return False
        try:
            file = open(self.filename, 'rb')
            out = pickle.load(file)
            file.close()
            return out
        except IOError:
            return False
