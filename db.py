import mysql.connector as mysql


class conn():
    cnx = None
    cursor = None

    def __init__(self):
        self.cnx = mysql.connection.MySQLConnection(user='root',
                                                    password='xch19970208',
                                                    host='119.23.233.0',
                                                    database='OOADPro'
                                                    )
        self.cursor = self.cnx.cursor()

    def commit_change(self):
        self.cnx.commit()

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def __execute_sql_single(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except:
            result = None
        return result

    def __execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except:
            result = None
        return result

    def get_user_password(self, UID):
        sql = "select t.STUDENT_PASSWORD from OOADPro.STUDENTS t where t.SID = '{}'".format(UID)
        result = self.__execute_sql_single(sql)
        print(result[0])
        return str(result[0])

    def get_user_schedule(self, UID):
        sql = "SELECT sc.SID,COURSE_NAME,TERM FROM STUDENT_COURSE sc\
              JOIN COURSE ON sc.CID = COURSE.CID JOIN STUDENTS\
               ON sc.SID = STUDENTS.SID WHERE sc.SID = '{}';".format(UID)
        result = self.__execute_sql(sql)
        return result

    def change_user_password(self, UID, psw):
        sql = "UPDATE `OOADPro`.`STUDENTS` t SET t.`STUDENT_PASSWORD` = '{}' WHERE t.`SID` = '{}';".format(psw, UID)
        result = self.__execute_sql(sql)
        self.commit_change()
        return result

# if __name__ == '__main__':
#     a = conn()
#     a.get_user_password(11510102)
#     print(a.change_user_password(11510102,12345))
#     a.get_user_password(11510102)
#     a.close()
