import pymysql as pms
import sys

connection = pms.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = 'dltjsals0804',
    charset = 'utf8',
    db = 'test'
)

def CreateTable():
    #관리자 Table
        sql0 = '''CREATE TABLE 관리자(
                관리자번호 INT NOT NULL,
                담당부서 VARCHAR(20) NOT NULL,
                소속은행지점 VARCHAR(20) NOT NULL,
            PRIMARY KEY (관리자번호)
        );'''
        cursor.execute(sql0)
        connection.commit()
        #사용자 Table
        sql1 = '''CREATE TABLE 사용자(
                성 VARCHAR(2) NOT NULL,
                이름 VARCHAR(3) NOT NULL,
                주민등록번호 VARCHAR(30) NOT NULL,
                담보 VARCHAR(50),
                신용등급 INT,
            PRIMARY KEY (주민등록번호)
        );'''
        cursor.execute(sql1)
        connection.commit()
        #사용자_전화번호 Table
        sql2 = '''CREATE TABLE 사용자_전화번호(
                전화번호 VARCHAR(30) NOT NULL,
                주민등록번호 VARCHAR(30) NOT NULL,
            PRIMARY KEY (전화번호, 주민등록번호),
            FOREIGN KEY (주민등록번호) REFERENCES 사용자(주민등록번호) ON UPDATE CASCADE
        );'''
        cursor.execute(sql2)
        connection.commit()
        #사용자_계좌번호 Table
        sql3 = '''CREATE TABLE 사용자_계좌번호(
                계좌번호 VARCHAR(50) NOT NULL,
                주민등록번호 VARCHAR(30) NOT NULL,
            PRIMARY KEY (계좌번호, 주민등록번호),
            FOREIGN KEY (주민등록번호) REFERENCES 사용자(주민등록번호) ON UPDATE CASCADE
        );'''
        cursor.execute(sql3)
        connection.commit()
        #예금 Table
        sql6 = '''CREATE TABLE 예금(
                금융상품ID INT NOT NULL,
                연금리 DECIMAL(10,2) NOT NULL,
                운영책임자 INT NOT NULL,
            PRIMARY KEY (금융상품ID)
        );'''
        cursor.execute(sql6)
        connection.commit()
        #적금 Table
        sql7 = '''CREATE TABLE 적금(
                금융상품ID INT NOT NULL,
                연금리 DECIMAL(10,2) NOT NULL,
                월별저축금액 BIGINT NOT NULL,
                만기일 DATE NOT NULL,
                운영책임자 INT NOT NULL,
            PRIMARY KEY (금융상품ID)
        );'''
        cursor.execute(sql7)
        connection.commit()
        #대출 Table
        sql8 = '''CREATE TABLE 대출(
                금융상품ID INT NOT NULL,
                담보종류 VARCHAR(50) NOT NULL,
                적용금리 DECIMAL(10,2) NOT NULL,
                만기일 DATE NOT NULL,
                대출한도 BIGINT NOT NULL,
                운영책임자 INT NOT NULL,
            PRIMARY KEY (금융상품ID)
        );'''
        cursor.execute(sql8)
        connection.commit()
        #펀드 Table
        sql9 = '''CREATE TABLE 펀드(
                금융상품ID INT NOT NULL,
                주식비율 FLOAT NOT NULL DEFAULT 0,
                채권비율 FLOAT NOT NULL DEFAULT 1,
                위험성 CHAR(1) NOT NULL,
                기대수익률 DECIMAL(10,3) NOT NULL,
                운영책임자 INT NOT NULL,
            PRIMARY KEY (금융상품ID)
        );'''
        cursor.execute(sql9)
        connection.commit()
        #계좌 Table
        sql4 = '''CREATE TABLE 계좌(
                계좌번호 VARCHAR(50) NOT NULL,
                비밀번호 CHAR(4) NOT NULL,
                계좌종류 CHAR(2) NOT NULL,
                이체한도 BIGINT NOT NULL,
                발급은행지점 VARCHAR(20) NOT NULL,
                계좌개설날짜 DATE NOT NULL,
                예금금융상품ID INT,
                적금금융상품ID INT, 
                대출금융상품ID INT,
                펀드금융상품ID INT, 
                관리자번호 INT NOT NULL,
                주민등록번호 VARCHAR(30) NOT NULL,
            PRIMARY KEY (계좌번호),
            FOREIGN KEY (예금금융상품ID) REFERENCES 예금(금융상품ID),
            FOREIGN KEY (적금금융상품ID) REFERENCES 적금(금융상품ID),
            FOREIGN KEY (대출금융상품ID) REFERENCES 대출(금융상품ID),
            FOREIGN KEY (펀드금융상품ID) REFERENCES 펀드(금융상품ID),
            FOREIGN KEY (관리자번호) REFERENCES 관리자(관리자번호),
            FOREIGN KEY (주민등록번호) REFERENCES 사용자(주민등록번호) ON UPDATE CASCADE
        );'''
        cursor.execute(sql4)
        connection.commit()
        #계좌_입출금내역 Table
        sql5 = '''CREATE TABLE 계좌_입출금내역(
                입금내역 BIGINT DEFAULT 0,
                출금내역 BIGINT DEFAULT 0,
                계좌번호 VARCHAR(50) NOT NULL,
                순서 BIGINT NOT NULL DEFAULT 0,
            PRIMARY KEY (순서, 계좌번호)
        );'''
        cursor.execute(sql5)
        connection.commit()

#Manager Authorized
def Register_Manager(): #관리자 정보 추가하기
    print('''
-----------------------Register Manager----------------------------''')
    input1 = int(input("관리자 번호: "))
    input2 = input("담당 부서: ")
    input3 = input("소속 은행 지점: ")
    sql ='''INSERT INTO 관리자 VALUES({}, "{}", "{}");'''.format(input1, input2, input3)
    cursor.execute(sql)
    connection.commit()

def Delete_Manager(manager_number): #관리자 정보 삭제하기
    print('''
-----------------------Delete Manager----------------------------''')
    sql = '''DELETE FROM 관리자 WHERE 관리자번호={};'''.format(manager_number)
    cursor.execute(sql)
    connection.commit()

def Update_Manager_Information(manager_number): #자신의 소속 부서를 업데이트
    print('''
----------------Update Manager Information----------------''')
    input1 = input("New department: ")
    input2 = input("New bank branch: ")
    sql = '''UPDATE 관리자 SET 담당부서 = '{}', 소속은행지점 = '{}' WHERE 관리자번호 = {};'''.format(input1, input2, manager_number)
    cursor.execute(sql)
    connection.commit()

def Account_Management():
    Select = input('''
--------------------Account Management------------------------
1. Check the Balance of customers' account
2. Modify the customers' deposit and withdrawal details
---------------------------------------------------------------
input: ''')
    if (Select == '1'): #해당 금액 이상의 잔액을 가지고 있는계좌 잔액을 확인하기
        input1 = input("확인할 계좌의 최소 금액을 입력하세요: ")
        sql = '''SELECT  계좌번호, SUM(입금내역)-SUM(출금내역) AS 잔액  
        FROM 계좌_입출금내역 GROUP BY 계좌번호 HAVING 잔액 >= {};'''.format(input1)
        cursor.execute(sql)
        resultset = cursor.fetchall()
        for row in resultset:
            print('계좌번호: "{}" 잔액:{}'.format(row[0], row[1]))
    elif (Select == '2'): #선택한 입출금 내역 정보 수정하기
        input1 = input("수정하려는 계좌번호: ")
        input2 = int(input("수정하려는 입출금내역 순서: "))
        input3 = int(input("바뀐 입금 내역: "))
        input4 = int(input("바뀐 출금 내역: "))
        sql ='''UPDATE 계좌_입출금내역 SET 입금내역={}, 출금내역={} 
        WHERE 계좌번호="{}" AND 순서={}'''.format(input3, input4, input1, input2)
        cursor.execute(sql)
        connection.commit()
    else:
        return

def View_Customers():
    Select = input('''
---------------------View customers------------------------
1. View All Customers Information
2. View Some Selected Customers 
-----------------------------------------------------------
input: ''')
    if(Select == '1'): #모든 사용자의 정보를 확인하기
        print('''-------------------View All Customers Information-----------------------''')
        sql = '''SELECT * FROM 사용자 ORDER BY 성 ASC, 이름 ASC;'''
        cursor.execute(sql)
        resultset = cursor.fetchall()
        for row in resultset:
            print('이름:{0} {1} | 주민등록번호:{2} | 담보:{3} | 신용등급:{4}'.format(row[0], row[1], row[2], row[3], row[4]))
        print('''------------------------------------------------------------------------\n''')
    elif(Select == '2'): #일부 조건에 맞는 사용자의 정보를 확인하기
        Select2 = input('''
------------------View Some Selected Customers-------------------
1. Select Customers' First Name
2. Select Customers' Birth Year
-----------------------------------------------------------------
input: ''')
        if (Select2=='1'): #입력한 성을 가진 사용자의 정보 확인하기
            input1 = input("확인하고 싶은 사용자의 성: ")
            sql = '''SELECT * FROM 사용자 WHERE 성 = "{}" ORDER BY 성 ASC, 이름 ASC;'''.format(input1)
            cursor.execute(sql)
            resultset = cursor.fetchall()
            for row in resultset:
                print('이름:{0} {1} | 주민등록번호:{2} | 담보:{3} | 신용등급:{4}'.format(row[0], row[1], row[2], row[3], row[4]))
        elif (Select2=='2'): #입력한 년도에 태어난 사용자의 정보 확인하기
            input2 = input("확인하고 싶은 사용자의 태어난 년도: ")
            sql = '''SELECT * FROM 사용자 WHERE 주민등록번호 LIKE '{}%' ORDER BY 성 ASC, 이름 ASC;'''.format(input2)
            cursor.execute(sql)
            resultset = cursor.fetchall()
            for row in resultset:
                print('이름:{0} {1} | 주민등록번호:{2} | 담보:{3} | 신용등급:{4}'.format(row[0], row[1], row[2], row[3], row[4]))
        else:
            return
    else:
        return

def Add_Financial_Products(manager_number): #금융상품 추가
    Product = input('''
----Add Financial Products----
1. Deposit
2. Installment Saving
3. Loans
4. Funds
-------------------------------
input: ''')
    print()

    if(Product == '1'): #예금
        input1 = int(input("금융상품ID (1로 시작하는 네자리수): "))
        input2 = float(input("연금리: "))
        sql='''INSERT INTO 예금(금융상품id, 연금리, 운영책임자) 
        VALUES ({}, {}, {});'''.format(input1, input2, manager_number)
        cursor.execute(sql)
        connection.commit()
    
    elif(Product == '2'): #적금
        input1 = int(input("금융상품ID (2로 시작하는 네자리수): "))
        input2 = float(input("연금리: "))
        input3 = int(input("월별저축금액: "))
        input4 = input("만기일 (EX:2022-01-01): ")
        sql='''INSERT INTO 적금(금융상품id, 연금리, 월별저축금액, 만기일, 운영책임자) 
        VALUES ({}, {}, {}, "{}", {});'''.format(input1, input2, input3, input4, manager_number)
        cursor.execute(sql)
        connection.commit()

    elif(Product == '3'): #대출
        input1 = int(input("금융상품ID (3로 시작하는 네자리수): "))
        input2 = input("담보 종류: ")
        input3 = float(input("적용 금리: "))
        input4 = input("만기일 (EX:2022-01-01): ")
        input5 = int(input("대출한도: "))
        sql='''INSERT INTO 대출(금융상품id, 담보종류, 적용금리, 만기일, 대출한도, 운영책임자) 
        VALUES ({}, "{}", {}, "{}", {}, {});'''.format(input1, input2, input3, input4, input5, manager_number)
        cursor.execute(sql)
        connection.commit()
    
    elif(Product == '4'): #펀드
        input1 = int(input("금융상품ID (4로 시작하는 네자리수): "))
        input2 = float(input("주식 비율: "))
        input3 = float(1-input2) #채권비율
        if (input2 > 0.7):
            input4 = "상"
        elif (input2 > 0.4):
            input4 = "중"
        else:
            input4 = "하"
        input5 = float(input("기대 수익률: "))
        sql='''INSERT INTO 펀드(금융상품id, 주식비율, 채권비율, 위험성, 기대수익률, 운영책임자) 
        VALUES ({}, {}, {}, "{}", {}, {});'''.format(input1, input2, input3, input4, input5, manager_number)
        cursor.execute(sql)
        connection.commit()
    
    else:
        return

def Delete_Financial_Products(manager_number):
    #본인이 책임지고 있는 금융상품을 보여줌
    Show_Part(manager_number)
    print('''
--------------------Delete Financial Product--------------------''')
    Select = input("Types of financial products to be deleted: ")
    number = int(input("Enter the number of financial product: "))
    if(Select == '예금'):
        sql = '''SELECT * FROM 계좌 WHERE 예금금융상품ID = {};'''.format(number)
        if(cursor.execute(sql) != 0): #만일 해당 금융상품을 사용하는 계좌가 있는 경우, 삭제를 진행할 수 없음
            print("There's an account that uses the product")
            return
        else:
            sql = '''DELETE FROM 예금 WHERE 금융상품ID = {} and 운영책임자 = {};'''.format(number, manager_number)
            if(cursor.execute(sql) == 0):
                print("You don't have an authority to delete this product")
            else:
                connection.commit()
    elif(Select == '적금'):
        sql = '''SELECT * FROM 계좌 WHERE 적금금융상품ID = {};'''.format(number)
        if(cursor.execute(sql) != 0): #만일 해당 금융상품을 사용하는 계좌가 있는 경우, 삭제를 진행할 수 없음
            print("There's an account that uses the product")
            return
        else:
            sql = '''DELETE FROM 적금 WHERE 금융상품ID = {} and 운영책임자 = {};'''.format(number, manager_number)
            if(cursor.execute(sql) == 0):
                print("You don't have an authority to delete this product")
            else:
                connection.commit()
    elif(Select == '대출'):
        sql = '''SELECT * FROM 계좌 WHERE 대출금융상품ID = {};'''.format(number)
        if(cursor.execute(sql) != 0): #만일 해당 금융상품을 사용하는 계좌가 있는 경우, 삭제를 진행할 수 없음
            print("There's an account that uses the product")
            return
        else:
            sql = '''DELETE FROM 대출 WHERE 금융상품ID = {} and 운영책임자 = {};'''.format(number, manager_number)
            if(cursor.execute(sql) == 0):
                print("You don't have an authority to delete this product")
            else:
                connection.commit()
    elif(Select == '펀드'):
        sql = '''SELECT * FROM 계좌 WHERE 펀드금융상품ID = {};'''.format(number)
        if(cursor.execute(sql) != 0): #만일 해당 금융상품을 사용하는 계좌가 있는 경우, 삭제를 진행할 수 없음
            print("There's an account that uses the product")
            return
        else:
            sql = '''DELETE FROM 펀드 WHERE 금융상품ID = {} and 운영책임자 = {};'''.format(number, manager_number)
            if(cursor.execute(sql) == 0):
                print("You don't have an authority to delete this product")
            else:
                connection.commit()
    else:
        pass

def Show_Financial_Products(manager_number):
    Select = input('''
-----------------Show Financial Products-----------------
1. All Financial Products
2. Financial Products that you are responsibility for
----------------------------------------------------------
input: ''')
    print()
    if (Select == '1'): #모든 금융 자산을 보여주는 경우
        Show_All()
    elif (Select == '2'): #자신이 책임지고 있는 금융상품을 보여주는 경우
        Show_Part(manager_number)
    else:
        return

def Show_All(): #모든 금융자산을 보여주는 경우
    print('''
--------------------------All Financial Products-----------------------------
§ 1. Deposit §''')
    sql = '''SELECT * FROM 예금;'''
    cursor.execute(sql)
    resultset = cursor.fetchall()
    for row in resultset:
        sql0 = '''SELECT COUNt(*) FROM 계좌 WHERE 예금금융상품ID = {}'''.format(row[0])
        cursor.execute(sql0)
        result = cursor.fetchone()[0]
        print('금융상품ID: {0} | 연금리: {1}% | 운영책임자: {2} | 해당 금융상품을 이용하는 계좌의 수: {3}'.format(row[0], row[1]*100, row[2], result))
    print("\n§ 2. Installment Savings §")
    sql1 = '''SELECT * FROM 적금'''
    cursor.execute(sql1)
    resultset = cursor.fetchall()
    for row in resultset:
        sql0 = '''SELECT COUNt(*) FROM 계좌 WHERE 적금금융상품ID = {}'''.format(row[0])
        cursor.execute(sql0)
        result = cursor.fetchone()[0]
        print('금융상품ID: {0} | 연금리: {1}% | 월별 저축금액: {2} | 만기일: {3} | 운영책임자: {4} | 해당 금융상품을 이용하는 계좌의 수: {5}'.format(row[0], row[1]*100, row[2], row[3], row[4], result))
    print("\n§ 3. Loans §")
    sql2 = '''SELECT * FROM 대출'''
    cursor.execute(sql2)
    resultset = cursor.fetchall()
    for row in resultset:
        sql0 = '''SELECT COUNt(*) FROM 계좌 WHERE 대출금융상품ID = {}'''.format(row[0])
        cursor.execute(sql0)
        result = cursor.fetchone()[0]
        print('금융상품ID: {0} | 담보 종류: {1} | 적용 금리: {2}% | 만기일: {3} | 대출 한도: {4} | 운영책임자: {5} | 해당 금융상품을 이용하는 계좌의 수: {6}'.format(row[0], row[1], row[2]*100, row[3], row[4], row[5], result))
    print("\n§ 4. Funds §")
    sql3 = '''SELECT * FROM 펀드'''
    cursor.execute(sql3)
    resultset = cursor.fetchall()
    for row in resultset:
        sql0 = '''SELECT COUNt(*) FROM 계좌 WHERE 펀드금융상품ID = {}'''.format(row[0])
        cursor.execute(sql0)
        result = cursor.fetchone()[0]
        print('금융상품ID: {0} | 주식:채권비율: {1}:{2} | 위험성: {3} | 기대수익률: {4}% | 운영책임자: {5} | 해당 금융상품을 이용하는 계좌의 수: {6}'.format(row[0], row[1], row[2], row[3], row[4]*100, row[5], result))
    print('''------------------------------------------------------------------------------------------------------------------------''')

def Show_Part(manager_number): #자신이 책임지고 있는 금융상품을 보여주는 경우
    print('''
-----------------------------Financial Products that you are responsibility for--------------------------------
§ 1. Deposit §''')
    sql = '''SELECT * FROM 예금 WHERE 운영책임자 = {};'''.format(manager_number)
    number = cursor.execute(sql)
    if (number == 0):
        print("No Deposit")
    else:
        resultset = cursor.fetchall()
        for row in resultset:
            print('금융상품ID: {0} | 연금리: {1}% | 운영책임자: {2}'.format(row[0], row[1]*100, row[2]))
    print("\n§ 2. Installment Savings §")
    sql1 = '''SELECT * FROM 적금 WHERE 운영책임자 = {};'''.format(manager_number)
    number = cursor.execute(sql1)
    if (number == 0):
        print("No Installment Saving")
    else:
        resultset = cursor.fetchall()
        for row in resultset:
            print('금융상품ID: {0} | 연금리: {1}% | 월별 저축금액: {2} | 만기일: {3} | 운영책임자: {4}'.format(row[0], row[1]*100, row[2], row[3], row[4]))
    print("\n§ 3. Loans §")
    sql2 = '''SELECT * FROM 대출 WHERE 운영책임자 = {};'''.format(manager_number)
    number = cursor.execute(sql2)
    if (number == 0):
        print("No Loan")
    else:
        resultset = cursor.fetchall()
        for row in resultset:
            print('금융상품ID: {0} | 담보 종류: {1} | 적용 금리: {2}% | 만기일: {3} | 대출 한도: {4} | 운영책임자: {5}'.format(row[0], row[1], row[2]*100, row[3], row[4], row[5]))
    print("\n§ 4. Funds §")
    sql3 = '''SELECT * FROM 펀드 WHERE 운영책임자 = {};'''.format(manager_number)
    number = cursor.execute(sql3)
    if (number == 0):
        print("No Fund")
    else:
        resultset = cursor.fetchall()
        for row in resultset:
            print('금융상품ID: {0} | 주식:채권비율: {1}:{2} | 위험성: {3} | 기대수익률: {4}% | 운영책임자: {5}'.format(row[0], row[1], row[2], row[3], row[4]*100, row[5]))
    print('''-----------------------------------------------------------------------------------------------------------------''')

def Update_Financial_Product(manager_number): #자신이 관리하고 있는 금융상품 정보를 업데이트
    #자신이 책임지고 있는 금융상품 정보를 보여줌
    Show_Part(manager_number)
    print('''
----------------------Update Financial Product------------------------''')
    Select = input("Types of financial products to be updated: ")
    number = int(input("Enter the number of financial product: "))
    if(Select == "예금"): #예금
        input1 = float(input("새로운 연금리: "))
        sql ='''UPDATE 예금 SET 연금리 = {} WHERE 금융상품ID = {} and 운영책임자 = {};'''.format(input1, number, manager_number)
        cursor.execute(sql)
        connection.commit()
    elif(Select == "적금"): #적금
        input1 = float(input("새로운 연금리: "))
        input2 = int(input("새로운 월별저축금액: "))
        input3 = input("새로운 만기일 (EX:2022-01-01): ")
        sql = '''UPDATE 적금 SET 연금리 = {}, 월별저축금액 = {}, 만기일 = "{}" 
        WHERE 금융상품ID = {} and 운영책임자 = {};'''.format(input1, input2, input3, number, manager_number)
        cursor.execute(sql)
        connection.commit()
    elif(Select == "대출"): #대출
        input1 = input("담보 종류: ")
        input2 = float(input("적용 금리: "))
        input3 = input("만기일 (EX:2022-01-01): ")
        input4 = int(input("대출한도: "))
        sql = '''UPDATE 대출 SET 담보종류 = "{}", 적용금리 = {}, 만기일 = "{}", 대출한도 = {}
        WHERE 금융상품ID = {} and 운영책임자 = {};'''.format(input1, input2, input3, input4, number, manager_number)
        cursor.execute(sql)
        connection.commit() 
    elif(Select == "펀드"): #펀드
        input1 = float(input("새로운 주식 비율: "))
        input2 = float(1-input1) #채권비율
        if (input1 > 0.7):
            input3 = "상"
        elif (input1 > 0.4):
            input3 = "중"
        else:
            input3 = "하"
        input4 = float(input("새로운 기대 수익률: "))
        sql = '''UPDATE 펀드 SET 주식비율 = {}, 채권비율 = {}, 위험성 = "{}", 기대수익률 = {}
        WHERE 금융상품ID = {} and 운영책임자 = {};'''.format(input1, input2, input3, input4, number, manager_number)
        cursor.execute(sql)
        connection.commit()
    else:
        return

#Customer Authorized
def Add_New_Customers():
    print('''
--------Add New Customer---------''')
    input1 = input("성: ")
    input2 = input("이름: ")
    input3 = input("주민등록번호: ")
    input4 = input("담보: ")
    input5 = int(input("신용등급: "))
    input6 = input("전화번호: ")
    sql1 ='''INSERT INTO 사용자(성,이름, 주민등록번호, 담보, 신용등급) 
    VALUES ("{}","{}", "{}", "{}", {});'''.format(input1, input2, input3, input4, input5)
    cursor.execute(sql1)
    connection.commit()
    sql2='''INSERT INTO 사용자_전화번호(전화번호, 주민등록번호)
    VALUES ("{}","{}");'''.format(input6, input3)
    cursor.execute(sql2)
    connection.commit()
    while(1):
        Select = input("전화번호를 더 추가하시겠습니까? [y or n]: ")
        if(Select == 'y'):
            input7 = input("전화번호: ")
            sql2='''INSERT INTO 사용자_전화번호(전화번호, 주민등록번호)
            VALUES ("{}","{}");'''.format(input7, input3)
            cursor.execute(sql2)
            connection.commit()
        else: 
            return

def Check(password, account): #계좌번호가 있는지, 비밀번호가 맞는지 확인하는 작업, 맞으면 1, 없으면 0 반환
    sql = '''SELECT 비밀번호 FROM 계좌 WHERE 계좌번호 = '{}';'''.format(account)
    if(cursor.execute(sql) == 0):
        print("Wrong account number!")
        return 0 
    real = cursor.fetchone()
    real = str(real[0])
    if(real != password):
        print("Wrong password")
        return 0
    else:
        return 1

def Deposit_Withdrawal(account):
    Select = input('''
------------------[Choose Deposit or Withdraw]---------------------   
1. Deposit
2. Withdraw
input: ''')
    time = '''SELECT * FROM 계좌_입출금내역 WHERE 계좌번호 = '{}';'''.format(account)
    time = cursor.execute(time)

    if(Select == '1'):
        money = input("How much? ")
        sql = '''INSERT INTO 계좌_입출금내역(입금내역, 계좌번호, 순서) VALUES({},'{}',{});'''.format(money, account, time)
        cursor.execute(sql)
        connection.commit()
    elif(Select =='2'):
        money = int(input("How much? "))
        ssql = "SELECT 이체한도 FROM 계좌 WHERE 계좌번호 = '{}';".format(account)
        cursor.execute(ssql)
        limit = cursor.fetchone()
        limit = int(limit[0])
        if(money >= limit):
            print("It exceeded the transfer limit")
            return 
        else:
            sql = '''INSERT INTO 계좌_입출금내역(출금내역, 계좌번호, 순서) VALUES({},'{}',{});'''.format(money, account, time)
            cursor.execute(sql)
            connection.commit()
    else:
        return

def Check_Balance(account):
    print('''
----------------Check your account balance----------------''')
    Deposit_sum = '''SELECT SUM(입금내역) FROM 계좌_입출금내역 WHERE 계좌번호 = '{}';'''.format(account)
    cursor.execute(Deposit_sum)
    Deposit_sum = cursor.fetchone()
    Deposit_sum = Deposit_sum[0]
    Withdraw_sum = '''SELECT SUM(출금내역) FROM 계좌_입출금내역 WHERE 계좌번호 = '{}';'''.format(account)
    cursor.execute(Withdraw_sum)
    Withdraw_sum = cursor.fetchone()
    Withdraw_sum = Withdraw_sum[0]
    print("The balance of current account: {} won".format(Deposit_sum-Withdraw_sum))

def Check_Account_Info(ID):
    print('''
----------------Check registered financial product information----------------''')
    sql = '''SELECT * FROM 사용자_계좌번호 WHERE 주민등록번호 = {};'''.format(ID)
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print("보유하고 있는 계좌번호: {}".format(row[0]))
    print("--------------------------------------------")
    num = input("확인하고 싶은 계좌번호: ")
    print("---------------------------------------------")
    type ='''SELECT 계좌종류 FROM 계좌 WHERE 계좌번호 = '{}';'''.format(num)
    cursor.execute(type)
    type = cursor.fetchone()
    type = type[0]
    if(type == "예금"):
        sql = '''SELECT 금융상품ID, 연금리, 운영책임자 
        FROM 예금, 계좌 WHERE 금융상품ID = 예금금융상품ID and 계좌번호 ='{}';'''.format(num)
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print("금융상품ID: {}, 연금리: {}%, 운영책임자: {}".format(row[0], row[1]*100, row[2]))
    elif(type == "적금"):
        sql = '''SELECT 금융상품ID, 연금리, 월별저축금액, 만기일, 운영책임자 
        FROM 적금, 계좌 WHERE 금융상품ID = 적금금융상품ID and 계좌번호 ='{}';'''.format(num)
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print("금융상품ID: {}, 연금리: {}%, 월별저축금액: {}, 만기일: {}, 운영책임자: {}".format(row[0], row[1]*100, row[2], row[3], row[4]))
    elif(type == "대출"):
        sql = '''SELECT 금융상품ID, 담보종류, 적용금리, 만기일, 대출한도, 운영책임자
        FROM 대출, 계좌 WHERE 금융상품ID = 대출금융상품ID and 계좌번호 ='{}';'''.format(num)
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print("금융상품ID: {}, 담보종류: {}, 적용금리: {}%, 만기일: {}, 대출한도: {}, 운영책임자: {}".format(row[0], row[1], row[2]*100, row[3], row[4], row[5]))
    elif(type == "펀드"):
        sql = '''SELECT 금융상품ID, 주식비율, 채권비율, 위험성, 기대수익률, 운영책임자
        FROM 펀드, 계좌 WHERE 금융상품ID = 펀드금융상품ID and 계좌번호 ='{}';'''.format(num)
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print("금융상품ID: {}, 비율: {}:{}, 위험성: {}, 기대수익률: {}%, 운영책임자: {}".format(row[0], row[1], row[2], row[3], row[4]*100, row[5]))
    else:
        return

def Open_Account(input7): 
    print('''
----------Open Account-----------''')
    input1 = input("계좌 번호: ")
    input2 = input("비밀번호 (4자리수): ")
    input3 = input("계좌 종류: ")
    input4 = int(input("이체 한도: "))
    input5 = input("발급된 은행 지점: ")
    input6 = input("계좌 개설 날짜 (EX: 2021-11-27): ")

    #예금 상품을 주문한 경우
    if(input3 == "예금"):
        #예금 상품들을 먼저 보여준다.
        sql = '''SELECT * FROM 예금'''
        cursor.execute(sql)
        resultset = cursor.fetchall()
        for row in resultset:
            print('금융상품ID: {0} | 연금리: {1}% | 운영책임자: {2}'.format(row[0], row[1]*100, row[2]))
        input8 = int(input("선택한 금융상품ID: "))
        sql1 = "SELECT 운영책임자 FROM 예금 WHERE 금융상품ID = {}".format(input8)
        cursor.execute(sql1)
        resultset = cursor.fetchone()
        input9 = resultset[0]  
        sql3 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_5;''' #관리자번호
        cursor.execute(sql3)
        connection.commit
        sql5 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_6;''' #주민등록번호
        cursor.execute(sql5)
        connection.commit
        sql6 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_1;''' #예금금융상품ID
        cursor.execute(sql6)
        connection.commit
        sql2 ='''INSERT INTO 계좌(계좌번호, 비밀번호, 계좌종류, 이체한도, 발급은행지점, 계좌개설날짜, 예금금융상품ID, 관리자번호, 주민등록번호) 
VALUES ("{}", "{}", "{}", {}, "{}", "{}", {}, {}, "{}");'''.format(input1, input2, input3, input4, input5, input6, input8, input9, input7)
        cursor.execute(sql2)
        connection.commit()
        sql4 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_5 FOREIGN KEY (관리자번호) REFERENCES 관리자(관리자번호);'''
        cursor.execute(sql4)
        connection.commit()
        sql5 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_6 FOREIGN KEY (주민등록번호) REFERENCES 사용자(주민등록번호);'''
        cursor.execute(sql5)
        connection.commit()
        sql6 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_1 FOREIGN KEY (예금금융상품ID) REFERENCES 예금(금융상품ID);'''
        cursor.execute(sql6)
        connection.commit

    #적금 상품을 주문한 경우
    elif(input3 == "적금"):
        #적금 상품들을 먼저 보여준다.
        sql1 = '''SELECT * FROM 적금;'''
        cursor.execute(sql1)
        resultset = cursor.fetchall()
        for row in resultset:
            print('금융상품ID: {0} | 연금리: {1}% | 월별 저축금액: {2} | 만기일: {3} | 운영책임자: {4}'.format(row[0], row[1]*100, row[2], row[3], row[4]))
        input8 = int(input("선택한 금융상품ID: "))
        sql2 = "SELECT 운영책임자 FROM 적금 WHERE 금융상품ID = {}".format(input8)
        cursor.execute(sql2)
        resultset = cursor.fetchone()
        input9 = resultset[0]   
        sql3 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_5;''' #관리자번호
        cursor.execute(sql3)
        connection.commit
        sql5 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_6;''' #주민등록번호
        cursor.execute(sql5)
        connection.commit
        sql6 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_2;''' #적금금융상품ID
        cursor.execute(sql6)
        connection.commit
        sql2 ='''INSERT INTO 계좌(계좌번호, 비밀번호, 계좌종류, 이체한도, 발급은행지점, 계좌개설날짜, 적금금융상품ID, 관리자번호, 주민등록번호) 
VALUES ("{}", "{}", "{}", {}, "{}", "{}", {}, {}, "{}");'''.format(input1, input2, input3, input4, input5, input6, input8, input9, input7)
        cursor.execute(sql2)
        connection.commit()
        sql4 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_5 FOREIGN KEY (관리자번호) REFERENCES 관리자(관리자번호);'''
        cursor.execute(sql4)
        connection.commit()
        sql5 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_6 FOREIGN KEY (주민등록번호) REFERENCES 사용자(주민등록번호);'''
        cursor.execute(sql5)
        connection.commit()
        sql6 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_2 FOREIGN KEY (적금금융상품ID) REFERENCES 적금(금융상품ID);'''
        cursor.execute(sql6)
        connection.commit

    #대출 상품을 주문한 경우
    elif(input3 == "대출"):
        #대출 상품들을 먼저 보여준다.
        sql2 = '''SELECT * FROM 대출;'''
        cursor.execute(sql2)
        resultset = cursor.fetchall()
        for row in resultset:
            print('금융상품ID: {0} | 담보 종류: {1} | 적용 금리: {2}% | 만기일: {3} | 대출 한도: {4} | 운영책임자: {5}'.format(row[0], row[1], row[2]*100, row[3], row[4], row[5]))
        input8 = int(input("선택한 금융상품ID: "))
        sql2 = "SELECT 운영책임자 FROM 대출 WHERE 금융상품ID = {};".format(input8)
        cursor.execute(sql2)
        resultset = cursor.fetchone()
        input9 = resultset[0]
        sql3 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_5;''' #관리자번호
        cursor.execute(sql3)
        connection.commit
        sql5 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_6;''' #주민등록번호
        cursor.execute(sql5)
        connection.commit
        sql6 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_3;''' #대출금융상품ID
        cursor.execute(sql6)
        connection.commit
        sql2 ='''INSERT INTO 계좌(계좌번호, 비밀번호, 계좌종류, 이체한도, 발급은행지점, 계좌개설날짜, 대출금융상품ID, 관리자번호, 주민등록번호) 
VALUES ("{}", "{}", "{}", {}, "{}", "{}", {}, {}, "{}");'''.format(input1, input2, input3, input4, input5, input6, input8, input9, input7)
        cursor.execute(sql2)
        connection.commit()
        sql4 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_5 FOREIGN KEY (관리자번호) REFERENCES 관리자(관리자번호);'''
        cursor.execute(sql4)
        connection.commit()
        sql5 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_6 FOREIGN KEY (주민등록번호) REFERENCES 사용자(주민등록번호);'''
        cursor.execute(sql5)
        connection.commit()
        sql6 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_3 FOREIGN KEY (대출금융상품ID) REFERENCES 대출(금융상품ID);'''
        cursor.execute(sql6)
        connection.commit

    #펀드 상품을 주문한 경우
    elif(input3 == "펀드"):
        #펀드 상품들을 먼저 보여준다.
        sql3 = '''SELECT * FROM 펀드;'''
        cursor.execute(sql3)
        resultset = cursor.fetchall()
        for row in resultset:
            print('금융상품ID: {0} | 주식:채권비율: {1}:{2} | 위험성: {3} | 기대수익률: {4}% | 운영책임자: {5}'.format(row[0], row[1], row[2], row[3], row[4]*100, row[5]))
        input8 = int(input("선택한 금융상품ID: "))
        sql2 = "SELECT 운영책임자 FROM 펀드 WHERE 금융상품ID = {};".format(input8)
        cursor.execute(sql2)
        resultset = cursor.fetchone()
        input9 = resultset[0]
        sql3 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_5;''' #관리자번호
        cursor.execute(sql3)
        connection.commit
        sql5 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_6;''' #주민등록번호
        cursor.execute(sql5)
        connection.commit
        sql6 = '''ALTER TABLE 계좌 DROP FOREIGN KEY 계좌_ibfk_4;''' #펀드금융상품ID
        cursor.execute(sql6)
        connection.commit
        sql2 ='''INSERT INTO 계좌(계좌번호, 비밀번호, 계좌종류, 이체한도, 발급은행지점, 계좌개설날짜, 펀드금융상품ID, 관리자번호, 주민등록번호) 
VALUES ("{}", "{}", "{}", {}, "{}", "{}", {}, {}, "{}");'''.format(input1, input2, input3, input4, input5, input6, input8, input9, input7)
        cursor.execute(sql2)
        connection.commit()
        sql4 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_5 FOREIGN KEY (관리자번호) REFERENCES 관리자(관리자번호);'''
        cursor.execute(sql4)
        connection.commit()
        sql5 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_6 FOREIGN KEY (주민등록번호) REFERENCES 사용자(주민등록번호);'''
        cursor.execute(sql5)
        connection.commit()
        sql6 = '''ALTER TABLE 계좌 ADD CONSTRAINT 계좌_ibfk_4 FOREIGN KEY (펀드금융상품ID) REFERENCES 펀드(금융상품ID);'''
        cursor.execute(sql6)
        connection.commit
    #없는 금융상품을 입력한 경우
    else:
        print("Wrong financial product!")
        return
    #이렇게 만든 계좌와 사용자 주민등록번호 입력하기
    sql = '''INSERT INTO 사용자_계좌번호 VALUES("{}","{}");'''.format(input1,input7)
    cursor.execute(sql)
    connection.commit()
    sql = '''INSERT INTO 계좌_입출금내역(계좌번호) VALUES("{}");'''.format(input1)
    cursor.execute(sql)
    connection.commit()

def Delete_Account(account):
    print('''
----------------Delete Account----------------''')
    sql = '''DELETE FROM 사용자_계좌번호 WHERE 계좌번호 = '{}';'''.format(account) #사용자_계좌번호 Table에 해당 instance 삭제
    cursor.execute(sql)
    connection.commit()
    sql = '''DELETE FROM 계좌_입출금내역 WHERE 계좌번호 = '{}';'''.format(account) #계좌_입출금내역 Table에 해당 instance 삭제
    cursor.execute(sql)
    connection.commit()
    sql = '''DELETE FROM 계좌 WHERE 계좌번호 = '{}';'''.format(account) #계좌 Table에서 해당 instance 삭제
    cursor.execute(sql)
    connection.commit()

def Update_Customers(ID):
    print('''
--------Update Customer Information---------''')
    input1 = input("새로운 성: ")
    input2 = input("새로운 이름: ")
    input3 = input("새로운 담보: ")
    input4 = int(input("새로운 신용등급: "))
    input5 = input("새로운 전화번호: ")
    input6 = input("삭제할 전화번호: ")
    sql1 = '''UPDATE 사용자 SET 성='{}', 이름='{}', 담보='{}', 신용등급={} 
    WHERE 주민등록번호='{}';'''.format(input1, input2, input3, input4, ID)
    cursor.execute(sql1)
    connection.commit()
    sql2 = '''UPDATE 사용자_전화번호 SET 전화번호='{}' WHERE 주민등록번호 = '{}' and 전화번호 = '{}';'''.format(input5, ID, input6)
    cursor.execute(sql2)
    connection.commit()
    
#Menu
#1.Manager Menu
def Manager_Menu():
    while (1):
        Select = input('''
------------[Manager Menu]------------
0. Return to previous menu
1. Register Manager
2. Delete Manager
3. Update Manager Information
4. Account Management
5. View Customer Information
6. Add Financial Product
7. Delete Financial Product
8. Show Financial Products
9. Update Financial Product
10. Exit the program
--------------------------------------
input: ''')
        if(Select == '0'):
            return
        elif(Select == '1'): #Register Manager
            Register_Manager()
        elif(Select == '2'): #Delete Manager
            manager_number = int(input("Enter manager number: "))
            Delete_Manager(manager_number)
        elif(Select == '3'): #Update Manager Information
            manager_number = int(input("Enter manager number: "))
            Update_Manager_Information(manager_number)
        elif(Select == '4'): #Account Management
            Account_Management()
        elif(Select == '5'): #View Customer Information
            View_Customers()
        elif(Select == '6'): #Add Financial Product
            manager_number = int(input("Enter manager number: "))
            Add_Financial_Products(manager_number)
        elif(Select == '7'): #Delete Financial Product
            manager_number = int(input("Enter manager number: "))
            Delete_Financial_Products(manager_number)
        elif(Select == '8'): #Show Financial Products
            manager_number = int(input("Enter manager number: "))
            Show_Financial_Products(manager_number)
        elif(Select == '9'): #Update Financial Product
            manager_number = int(input("Enter manager number: "))
            Update_Financial_Product(manager_number)
        elif(Select == '10'): #Exit the program
            sys.exit()

#2.Customer Menu
def Customer_Menu():
    while (1):
        Select = input('''
---------------[Customer Menu]------------------
0. Return to previous menu
1. Deposit and Withdraw money
2. Check your account balance
3. Check registered financial product information
4. Register your information
5. Open your account (Order financial products)
6. Delete your account
7. Update Customer Information
8. Exit the program
------------------------------------------------
input: ''')
        if(Select == '0'):
            return
        elif(Select == '1'):
            account = input("Please enter your account: ")
            password = input("Please enter your account password: ")
            if (Check(password, account) == 0):
                pass
            else:
                print()
                Deposit_Withdrawal(account)
        elif(Select == '2'):
            account = input("Please enter your account: ")
            password = input("Please enter your account password: ")
            if (Check(password, account) == 0):
                pass
            else:
                print()
                Check_Balance(account)
        elif(Select == '3'):
            ID = input("Please enter your personal ID: ")
            Check_Account_Info(ID)
        elif(Select == '4'):
            Add_New_Customers()
        elif(Select == '5'):
            ID = input("Please enter your personal ID: ")
            sql ='''SELECT 주민등록번호 FROM 사용자 WHERE 주민등록번호="{}";'''.format(ID)
            num = cursor.execute(sql)
            connection.commit()
            if (num == 0):
                print("You are not registered. Please register your personal information first\n")
            else:
                Open_Account(ID)
        elif(Select == '6'):
            account = input("Please enter your account: ")
            password = input("Please enter your account password: ")
            if (Check(password, account) == 0): #비밀번호가 틀렸거나 해당 계좌번호가 틀린 경우
                pass
            else:
                print()
                Delete_Account(account)
        elif(Select == '7'):
            ID = input("Please enter your personal ID: ")
            sql ='''SELECT 주민등록번호 FROM 사용자 WHERE 주민등록번호="{}";'''.format(ID)
            num = cursor.execute(sql)
            connection.commit()
            if (num == 0):
                print("You are not registered. Please register your personal information first\n")
            else:
                Update_Customers(ID)
        elif(Select == '8'):
            sys.exit()

try:
    with connection.cursor() as cursor:
        #Create Table
        Count = '''SELECT 1 FROM Information_schema.tables WHERE table_schema = "test";'''
        Count1 = cursor.execute(Count)
        connection.commit()        
        #만일 table이 존재하는 경우, CreateTable과정 없이 진행
        if (Count1 > 0):
            print("Table is already exist, Use table that already exists")
        else:
            print("Create Table")
            CreateTable()

        while (1):
            Select = input('''
--------Menu--------
1. Manager Menu
2. Customer Menu
3. Exit the program
--------------------
Input: ''')
            print()

            #1.Manager Menu
            if(Select =='1'):
                Manager_Menu()

            #2.Customer Menu
            elif(Select == '2'):
                Customer_Menu()

            #3.Exit
            elif(Select == '3'):
                sys.exit()

            else:
                print("Please enter the correct number")

finally:
    connection.close()
