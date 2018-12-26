import mysql.connector as mysql
from random import *


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
            result = self.cursor.fetchone()[0]
            # self.cursor.fetchall()
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
        try:
            result = self.__execute_sql_single(sql)
        except:
            result = None
        # print(result)
        return str(result)

    def get_user_schedule(self, UID):
        sql = "SELECT sc.SID,COURSE_NAME,TERM FROM STUDENT_COURSE sc\
              JOIN COURSE ON sc.CID = COURSE.CID JOIN STUDENTS\
               ON sc.SID = STUDENTS.SID WHERE sc.SID = '{}';".format(UID)
        result = self.__execute_sql(sql)
        return result

    def get_all_classes(self, UID):
        sql = "SELECT c.CID,c.COURSE_NAME,c.COURSE_CAP,c.COURSE_DUR,\
        c.COURSE_MAJOR,c.COURSE_TIME,c.CREDITS,c.SELECTED_NUMBER,\
        c.TEACHER,c.COURSE_LOC,c.COURSE_TERM FROM  COURSE as c where c.CID \
        not in(SELECT st.CID FROM STUDENT_COURSE as st WHERE st.SID = '{}');".format(
            UID)
        result = self.__execute_sql(sql)
        return result

    def get_schedule(self, UID):
        sql = "SELECT c.COURSE_NAME,c.COURSE_LOC,c.COURSE_TIME,c.TEACHER FROM COURSE \
        AS c JOIN STUDENT_COURSE AS sc on c.CID = sc.CID WHERE sc.SID = '{}';".format(UID)
        result = self.__execute_sql(sql)
        return result

    def get_grade(self, UID):
        sql = "SELECT c.CID,c.COURSE_NAME,c.CREDITS,sc.GRADE from STUDENT_COURSE as sc \
        join COURSE as c ON sc.CID = c.CID WHERE sc.SID = '{}';".format(UID)
        result = self.__execute_sql(sql)
        return result

    def change_user_password(self, UID, psw):
        sql = "UPDATE `OOADPro`.`STUDENTS` t SET t.`STUDENT_PASSWORD` = '{}' WHERE t.`SID` = '{}';".format(psw, UID)
        result = self.__execute_sql(sql)
        self.commit_change()
        return result

    def get_selected(self, UID):
        sql = "SELECT c.CID,c.COURSE_NAME,c.COURSE_CAP,c.COURSE_DUR,\
        c.COURSE_MAJOR,c.COURSE_TIME,c.CREDITS,c.SELECTED_NUMBER,\
        c.TEACHER,c.COURSE_LOC,c.COURSE_TERM FROM STUDENT_COURSE as st JOIN COURSE as c\
        on c.CID = st.CID WHERE st.SID = '{}';".format(UID)
        res = self.__execute_sql(sql)
        return res

    def check_pre(self, UID, CID, TERM="2018SPRING"):
        sql_comb = "SELECT cs.COMBID as COMBID,COURSEID,SUBCOMBID,OP from COMBINATION_COURSE \
        AS cs LEFT JOIN COMBINATION AS c on cs.COMBID = c.COMBID;"
        sql_selected = "SELECT c.CID FROM COURSE AS c JOIN STUDENT_COURSE AS sc \
        ON c.CID = sc.CID WHERE sc.SID = '{}';".format(UID)
        sql_courselimit = "SELECT c.COURSE_COMB FROM COURSE as c WHERE c.CID = '{}';".format(CID)
        # print(sql_comb+"\n"+sql_selected+"\n"+sql_courselimit)
        limit_comb = self.__execute_sql_single(sql_courselimit)
        # print(limit_comb)
        if limit_comb:
            all_comb = self.__execute_sql(sql_comb)
            selected_course = self.__execute_sql(sql_selected)
            # print(selected_course)
            # print(all_comb)
            con_set = []
            con_set = self.read_con(all_comb, limit_comb, con_set)
            # print(con_set)
            con_part = [[]]
            split = 0
            for i in range(len(con_set)):
                # print(split)
                if i % 2 == 1:
                    if str(con_set[i]) == "OR":
                        split += 1
                        con_part.append([])
                    # elif str(con_set[i]) == "AND":
                    #     print('wait')
                else:
                    con_part[split].append(con_set[i])
            print(con_part)
            print(selected_course)
            s_course = []
            for k in selected_course:
                s_course.append(str(k[0]))
            torf = True
            for item in con_part:
                for i in item:
                    if i not in s_course:
                        torf = False
                if torf == True:
                    return 1, "Fulfill the prerequisite."
                torf = True
            msg = "("
            for i in con_part:
                for j in i:
                    msg += str(j)
                    if j != i[len(i) - 1]:
                        msg += " and "
                msg += ")"
                if i != con_part[len(con_part) - 1]:
                    msg += " or ("
            return 0, "Fail, prerequisite: " + msg
        else:
            return 1, "Fulfill the prerequisite."

    def read_con(self, all_comb, limit_comb, con_set):
        for item in all_comb:
            # print(item)
            if item[0] == limit_comb:
                if item[2] == None:
                    con_set.append(item[1])
                    con_set.append(item[3])
                elif item[1] == None:
                    con_set = self.read_con(all_comb, item[2], con_set)
        return con_set

    def check_cap(self, CID):
        sql = "SELECT c.COURSE_CAP,c.SELECTED_NUMBER FROM COURSE as c WHERE CID = '{}'".format(CID)
        res = self.__execute_sql(sql)
        # print(res)
        max_cap = res[0][0]
        current_n = res[0][1]
        if current_n < max_cap:
            return True
        else:
            return False

    def r_choose_one_course(self, UID):
        try:
            sql = "SELECT sc.CID FROM STUDENT_COURSE as sc WHERE sc.SID = '{}';".format(UID)
            res = self.__execute_sql(sql)
            temp = int(random() * len(res))
            # print(str(res)+res[temp][0])
            result = res[temp][0]
        except:
            result = None
        return result

    def show_reco(self, UID):
        CID = str(self.r_choose_one_course(UID))
        sql1 = "SELECT sc1.CID,count(*) FROM STUDENT_COURSE as sc1 WHERE sc1.SID in (\
        SELECT sc2.SID FROM STUDENT_COURSE as sc2 WHERE sc2.CID = '{}')and \
        sc1.CID!= '{}' GROUP BY sc1.CID;".format(CID, CID)
        res = self.__execute_sql(sql1)
        # print(CID)
        sql2 = "SELECT c.SELECTED_NUMBER FROM COURSE as c WHERE c.CID = '{}';".format(CID)
        total_num = (self.__execute_sql(sql2)[0][0])
        # print(total_num)
        msg = "{}% of people who choose {} also choose {}!".format(str(100 * float(res[0][1]) / float(total_num)), CID,
                                                                   str(res[0][0]))
        # print(msg)
        return msg, str(res[0][0]), str(100 * float(res[0][1]) / float(total_num))

    def get_course_info(self, CID):
        sql = "SELECT c.CID,c.COURSE_NAME,c.TEACHER FROM COURSE as c WHERE CID = '{}';".format(CID)
        res = self.__execute_sql(sql)
        return res

    def select_course(self, UID, CID, TERM="2018SPRING"):
        code, msg = self.check_pre(UID, CID, TERM)
        if code == 1:
            if self.check_cap(CID):
                sql1 = "INSERT INTO OOADPro.STUDENT_COURSE (SID, CID, TERM) \
                VALUES ({}, '{}', '{}');".format(UID, CID, TERM)
                self.__execute_sql(sql1)
                sql2 = "UPDATE COURSE as c SET \
                c.SELECTED_NUMBER=c.SELECTED_NUMBER+1 WHERE CID = '{}';".format(CID)
                self.__execute_sql(sql2)
                self.commit_change()
                return "success"
            else:
                msg += "  ** The course is full **"
                return msg
        else:
            return msg

    def withdraw_course(self, UID, CID, TERM="2018SPRING"):
        sql1 = "DELETE FROM STUDENT_COURSE WHERE SID = '{}' and CID = '{}' and TERM = '{}'".format(UID, CID, TERM)
        self.__execute_sql(sql1)
        sql2 = "UPDATE COURSE as c SET \
        c.SELECTED_NUMBER=c.SELECTED_NUMBER-1 WHERE CID = '{}';".format(CID)
        self.__execute_sql(sql2)
        self.commit_change()

# if __name__ == '__main__':
#     a = conn()
#     print(a.r_choose_one_course(11510102))
#     # a.select_course(UID=11510102, CID="CS004")
#     # a.get_user_password(11510102)
#     # a.check_full(CID='CS004')
#     # print(a.get_all_classes(11510102))
#     # a.get_user_password(11510102)
#     a.close()
