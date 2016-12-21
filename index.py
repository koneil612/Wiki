import mysql.connector
import config


class Entry:
    def __init__(self, id=0, title=""):
        # this is going to pull the wiki. saying that if there is no wiki with that title name then set a new id. if that title exists then to pull it.
        # self.id=result_set[0]
        self.title=title
        self.content = ""
        self.mdate = ""
        self.authormod= ""

        if(not type (id)==int):
            id=int(id)
        whereclause = "false"
        if id>0:
            whereclause = "id=%d" %id
        if len(title)>0:
            whereclause = "title ='%s'" % title

        query = "SELECT id, title, content, mdate, authormod FROM page WHERE %s" % whereclause
        result_set = Database.getResult(query, True)
        if not result_set is None:
            self.id=result_set[0]
            self.title=result_set[1]
            self.content = result_set[2]
            self.mdate = result_set[3]
            self.authormod= result_set[4]
        return

    def save(self):
        if self.id>0:
            return self.update()
        else:
            return self.insert()
    def insert(self):
        query = ("INSERT into page (title, content, mdate,authormod) values (\"%s\", \"%s\", \"%s\", \"%s\")") % (Database.escape(self.title), self.content, self.mdate, self.authormod)
        self.id = Database.doQuery(query)
        return self.id
    def update(self):
        query="UPDATE page set title='%s', content='%s', mdate=%s, authormod=%s WHERE id=%d" % (Database.escape(self.title), content, mdate, authormod, self.id)
        return Database.doQuery(query)
    @staticmethod
    def getObjects():
        query= "SELECT id, title, content, mdate, authormod FROM page"
        result_set = Database.getResult(query)
        entries=[]
        for item in result_set:
            id = int(item[0])
            entries.append(Entry(id))
        return entries

class Database(object):
    # this entire class does a lot:
    # the getConnection is pulling our database connection through. I created a config.py that it's looking for wiht the user pw host info ect. so if we change the database we just update config and don't need to change this form
    # escape is looking for an apostrophe that a user may input in and will override it so it doesn't crash the system
    # the doQuery part is actually executing all the cursor connections that we need for example the connection the execution and then the closing of the cursor and the connection.
    @staticmethod
    def getConnection():
        return mysql.connector.connect(user=config.dbuser, password=config.dbpassword, host=config.dbhost, database=config.dbname)
    @staticmethod
    def escape(value):
        return value.replace(" ' ", "''")
    @staticmethod
    def getResult(query,getOne=False):
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        if getOne:
            result_set = cur.fetchone()
        else:
            result_set = cur.fetchall()
        cur.close()
        conn.close()
        return result_set
    @staticmethod
    def doQuery(query):
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        lastId = cur.lastrowid
        cur.close()
        conn.close()
        return lastId
