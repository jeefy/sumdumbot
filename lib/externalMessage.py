import sqlite3

class ExternalMessage:
    def __init__(self, factory, config):
        self.factory = factory
        self.config  = config
        self.conn    = sqlite3.connect(config['dbPath'])
        self.curs    = self.conn.cursor()
        
        self._create()
    
    def check(self):
        self.curs.execute('SELECT rowid, source, message FROM external_messages WHERE read=\'0\' order by rowid;')
        rows = self.curs.fetchall()
        for row in rows:
            self.factory.bot.msg(self.factory.home, str(row[1]) + ': ' + str(row[2]) )
            self._update(row[0])
        return False
    
    def _create(self):
        self.curs.execute('''CREATE TABLE  if not exists external_messages
             (source text, message text, read int)''')
        return False
    
    def _update(self, rowid):
        self.curs.execute('UPDATE external_messages set read=1 where rowid=?', (rowid, ))
        self.conn.commit()
        return False