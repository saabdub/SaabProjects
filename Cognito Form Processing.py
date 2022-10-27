
import time
import datetime
import os
import json
import shutil
from datetime import datetime
import pandas as pd
import mysql.connector
from Emailing import Email

user = os.environ.get("USERNAME")
class NewDbUpload():

    def __init__(self):
        self.study_id = None
        self.business_unit_id = None
        self.service_area_id = None
        self.client_id = None
        self.errormessage = ""


    def connectnewdb(self, statement: str, statementtype: str):
        mydb = mysql.connector.connect(host='iclproduction.mysql.database.azure.com',
                                    user= os.environ.get('DATABASE_LOGIN'),
                                    password=os.environ.get('DATABASE_PASSWORD'),
                                    database="production"
                                       )
        con = mydb.cursor()
        try:
            con.execute(statement)
            if statementtype == "select":
                return con.fetchall()
            elif statementtype == "insert":
                mydb.commit()
                return con.lastrowid
            else:
                mydb.commit()
        except mysql.connector.Error as err:
            self.addToErrormessage(str(err))

        mydb.close()

    def getClient(self, cient_name: str, sector: str, industry: str, location: str):
        print("Getting client id...")
        statement = f"SELECT id FROM dim_client WHERE name = '{cient_name}' AND sector = '{sector}' AND industry = '{industry}' AND country = '{location}'"
        result = self.connectnewdb(statement, "select")

        if result:
            self.client_id = result[0][0]
        else:
            statement = f"INSERT INTO dim_client (name,sector,industry,country) VALUES ('{cient_name}', '{sector}', " \
                        f"'{industry}', '{location}')"
            self.client_id = self.connectnewdb(statement, "insert")

    def getStudyId(self, study_name: str, start_date: str,
                    end_date: str, months_actuals: int, year_commenced: int = datetime.now().year):
        print("Getting study id...")
        statement = f"SELECT id FROM dim_study WHERE name = '{study_name}'"
        result = self.connectnewdb(statement, "select")
        if result:
            self.study_id = result[0][0]
        else:
            statement = f"INSERT INTO dim_study (name, client_id, start_date, end_date, months_actuals, " \
                        f"year_commenced) VALUES ('{study_name}', {self.client_id}, '{start_date}', '{end_date}'," \
                        f" {months_actuals}, {year_commenced})"
            self.study_id = self.connectnewdb(statement, "insert")

    def getCurrency(self, short_code: str):
        statement = f"select id from dim_currency where short_code = '{short_code}'"
        result = self.connectnewdb(statement, "select")
        if result:
            return result[0][0]
        else:
            statement = f"INSERT INTO dim_currency (short_code) VALUES ('{short_code}')"
            self.addToErrormessage (f"\n\nCurrency {short_code} was not found in the database and was added. " 
                            f"Please also fill up the missing information in the database.")

            return self.connectnewdb(statement, "insert")

    def getGeography(self, city: str, location: str, region: str):
        statement = f"SELECT id FROM dim_geography WHERE city = '{city}' AND country = '{location}' AND " \
                    f"region = '{region}'"
        result = self.connectnewdb(statement, "select")
        if result:
            return result[0][0]
        else:
            statement = f"INSERT INTO dim_geography (city, country, region) VALUES ('{city}', '{location}', '{region}')"
            self.addToErrormessage(f"\n\nGeography {city}, {location}, {region} was not found in the database and was added.Please also fill up the missing information in the database.")
            return self.connectnewdb(statement, "insert")

    def addToErrormessage(self, message: str):
        self.errormessage += message

    def getBusinessUnitid(self, sector, industry, short_code, city, location, region, line_of_business: str = "N/A", department:str = "N/A"):
        print("Getting business unit id...")
        statement = f"SELECT id FROM dim_business_unit WHERE client_id = '{self.client_id}' and sector = '{sector}' " \
                    f"AND industry = '{industry}' AND  line_of_business = '{line_of_business}' AND department = '{department}'" \
                    f" AND geography_id = {self.getGeography(city, location, region)} AND currency_id = {self.getCurrency(short_code)}"

        result = self.connectnewdb(statement, "select")
        if result:
            self.business_unit_id = result[0][0]
        else:
            statement = f"insert into dim_business_unit (client_id, sector, industry, line_of_business, department, " \
                        f"geography_id, currency_id) VALUES ({self.client_id}, '{sector}', '{industry}', '{line_of_business}', " \
                        f"'{department}', {self.getGeography(city, location, region)}, {self.getCurrency(short_code)})"

            self.business_unit_id = self.connectnewdb(statement, "insert")

    def getServiceAreaid(self, service_area: str, sub_service_area: str = "All"):
        statement = f"SELECT id FROM dim_service_area WHERE name = '{service_area}' and sub_service_area = '{sub_service_area}'"
        result = self.connectnewdb(statement, "select")
        if result:
            self.service_area_id = result[0][0]
        else:
            self.addToErrormessage(f"\n\nService Area {service_area} was not found in the database. "
                            f"Upload was not completed. Please check the form before upload.")
            raise Exception(self.errormessage)


class ProjectInfo(NewDbUpload):

    def __init__(self, test: bool, filename: str):
        super().__init__()
        self.import_path = "C:/Users/" + user + "/Dropbox (ImprovIT)/ICL DB Import Folder/ICL Form Converter/Import"
        self.export_path = "C:/Users/" + user + "/Dropbox (ImprovIT)/ICL DB Import Folder/ICL Form Converter/Export"
        self.project_name = filename
        self.filename = filename
        self.databaseTableName = None
        self.data = None
        self.isTest = test
        self.infomessage = ""
        self.service_area_name = None
        self.status = None

    def check_record(self):
        if self.study_id and self.business_unit_id:
            return True
        else:
            return False

    def InjecttionAttackCheck (self, item: str) -> str:
        if item is not None:
            if "select" in item.lower() or "delete" in item.lower() or "update" in item.lower() or \
                    "drop" in item.lower() or "insert" in item.lower():
                item = item.replace("select", "").replace("delete", "").replace("update", "")\
                    .replace("drop", "").replace("insert", "").replace(";", "")
            return item

    def getData(self):
        """
        This function will get the data from the import folder and will save the data in a dictionary
        :return: None
        """
        if self.filename is not None:
            with open(self.import_path + "/" + self.filename, "r") as f:
                self.data = json.load(f)
                #shutil.move(self.import_path + "/" + x, self.export_path + "/" + x)
                #os.rename(self.export_path + "/" + x, self.export_path + f"/{str(datetime.now()).replace('-', '').replace(':','').replace(' ','').replace('.','')}" + x)

    def getAttachement(self):
        try:
            self.numberOfAttachments = self.data["ProjectInformation"]["_999ATTATCHMENTSINCLUDED"]
            self.addToInfoMessage("\nThere are " + str(self.numberOfAttachments) + " attachments\n")
        except:
            self.numberOfAttachments = 0

    def getProjectInfo(self):
        if self.filename is not None:
            try:
                self.project_info = self.data["ProjectInformation"] | self.data["Geography"] | self.data["Currency"]
            except:
                self.addToErrormessage("\nProject Information is missing something worth checking\n")

    def cleanPojectInfo(self):
        self.getProjectInfo()
        tempdict = {}
        if self.filename is not None:
            for key, value in self.project_info.items():
                if not "_" in key:
                    if "date" in key.lower():
                        value = self.dateChange(value)
                    if str(value).strip() == "":
                        value = None
                    if "year" in key.lower():
                        value = str(value).replace(",", "")
                    if value is not None:
                        tempdict[key] = self.InjecttionAttackCheck(str(value))
            self.project_info = tempdict

    def dateChange(self, item: str) -> str:

        if item is not None:
            try:
                newdate = datetime.strptime(item, '%d/%m/%Y').strftime('%Y-%m-%d')
            except:
                newdate = item
            return newdate

    def addToInfoMessage(self, message: str):
        self.infomessage += message

    def prepareDb(self):
        self.getClient(self.project_info["Client"], self.project_info["Sector"], self.project_info["Industry"],
                       self.project_info["Country2"])
        self.getStudyId(self.project_info["TProjectName"], self.project_info["TStudyPeriodStartDate"],
                        self.project_info["TStudyPeriodEndDate"],self.project_info["TMonthsActuals"])
        self.getBusinessUnitid(self.project_info["Sector"], self.project_info["Industry"], self.project_info["OriginalCurrency"],
                                 self.project_info["City"], self.project_info["Country2"], self.project_info["Region"])
        print("Checking state of records")
        if not self.check_record():
            self.addToErrormessage("\n\nThe project information is not complete. Please check the data and try again\n")
            raise Exception(self.errormessage)
        else:
            return True

    def mainRun(self):
        self.getData()
        self.cleanPojectInfo()
        self.getAttachement()
        if self.prepareDb():
            print("Preparation done")


class allCognitoProcess(ProjectInfo):

    def __init__(self, test: bool, filename: str):
        super().__init__(test, filename)

    def mainRun(self):
        super().mainRun()
        print("Starting Cognito Process")
        self.extraStepsForDbBeforeLoad()

    def cleanPojectInfo(self):
        self.getProjectInfo()
        tempdict = {}
        if self.filename is not None:
            for key, value in self.project_info.items():
                if not "_" in key:
                    if "date" in key.lower():
                        value = self.dateChange(value)
                    if str(value).strip() == "":
                        value = None
                    if "year" in key.lower():
                        value = str(value).replace(",", "")
                    if value is not None:
                        tempdict[key] = self.InjecttionAttackCheck(str(value))

            self.project_info = tempdict

    def formCheck(self):

        def getFieldsNameFromDatabase():
            config = {
                'host': 'iclproduction.mysql.database.azure.com',
                'user': os.environ.get('DATABASE_LOGIN'),
                'password': os.environ.get('DATABASE_PASSWORD'),
                'database': 'iclprod'
            }

            try:
                conn = mysql.connector.connect(**config)
                cursor = conn.cursor()
                cursor.execute(
                "select column_name from information_schema.columns where table_name = '" + self.databaseTableName + "' \
                and table_schema = 'iclprod' and column_name not like '%---%' and column_name <> 'Study_id' and \
                ordinal_position between 3 and (select ordinal_position from information_schema.columns where table_schema \
                = 'iclprod' and table_name = '" + self.databaseTableName + "'  and column_name like '%OriginalCurrency%')-1;")
                fields =[]
                rows = [item[0] for item in cursor.fetchall()]
                # the reason for the NA here because BINARY fails me on mysql
                for k in rows:
                    if not k.endswith("NA"):
                        fields.append(k)

                cursor.close()
                conn.close()
                return fields

            except (mysql.connector.Error, mysql.connector.errors.ProgrammingError) as err:
                print(err)
                Email(err, self.data["cleint"]).Send()

        def send_email_with_the_field(NotinDB: list, NotonCognito: list, NumberofAttachement: int,
                                      UsedCognitoFormName: str, test: bool):
            if not NotinDB:
                MissingFields = '<p style="font-size: 16px;font-weight: bold; color: green;"> ' \
                        "All the fields on the form ('{}') are correct and are in use.</p>".format(UsedCognitoFormName)
            else:
                MissingFields = "These fields ({}) are not not in the Database.Please check. ".format(NotinDB)

            if not NotonCognito:
                MissingQuestions = ""
            else:
                MissingQuestions = '<H2 style= "font-weight: bold;font-size: 24px;"> FYI:</H2><br>' \
                                   "<p  style=font-size: 16px;> These fields {} are not on the Cognito form.</p>".format(NotonCognito)

            if NumberofAttachement > 0:
                ThereAreAttachements = '<H1 style=color:red;> There are {} Attachments  on Cognito </H1>'.format(
                    NumberofAttachement)
            else:
                ThereAreAttachements = ""

            message = "{}<br>{}<br>{}<br>".format(MissingFields, MissingQuestions, ThereAreAttachements)
            Email(message, UsedCognitoFormName, Test=test).Send()

        if self.data is not None:
            filds = getFieldsNameFromDatabase()
            fieldsOnFormNotInDB = list(filter(lambda a: a not in self.data.keys(), filds))
            fieldsinDBNotOnForm = list(filter(lambda b: b not in filds, self.data.keys()))
            send_email_with_the_field(fieldsinDBNotOnForm, fieldsOnFormNotInDB, self.numberOfAttachments,
                                      self.databaseTableName, self.isTest)

    def valueDataCheck(self):
        if self.data is not None:
            tempdata = {}
            self.databaseTableName = self.data["Form"]["Name"].replace(" ", "_") # or we can do by filename
            for key, value in self.data.items():
                if not "_" in key and not key.startswith("$") and not "Entry" in key and not "ZApplication" in key and\
                        not "ProjectInformation" in key and not "Form" in key:
                    tempdata[key] = value

            self.flatten_json(tempdata)
            tempdata.clear()
            for key, value in self.data.items():
                if not "_" in key and "id" != key.lower() and "number" != key.lower() and "password" != key.lower() \
                                                                        and "yesno" != key.lower():
                    if "date" in key.lower():
                        value = self.dateChange(value)
                    if value == "":
                        value = None
                    if type(value) == bool:
                        if value == True:
                            value = "Yes"
                        else:
                            value = "No"

                    key = key[key.rfind(".")+1:]
                    tempdata[key] = value
            self.data = tempdata
            self.data = {**self.data, **self.project_info}

    def flatten_json(self, nested_json: dict, exclude: list = [''], sep: str = '.') -> dict:
        out = dict()

        def flatten(x: (list, dict, str), name: str = '', exclude=exclude):
            if type(x) is dict:
                for a in x:
                    if any(a not in item for item in exclude):
                        flatten(x[a], f'{name}{a}{sep}')
            elif type(x) is list:
                i = 0
                for a in x:
                    if any(list == type(sl) or dict == type(sl) for sl in x):
                        flatten(a, f'{name}{i}{sep}')
                    else:
                        out[name[:-1]] = x
                    i += 1
            else:
                out[name[:-1]] = x
        flatten(nested_json)
        self.data = out

    def loadDataToDatabese(self):
        if self.data is not None:
            theClient = self.project_info["Client"]
            fieldnames = list(self.data.keys())
            values = list(self.data.values())
            config = {
                    'host': 'iclproduction.mysql.database.azure.com',
                    'user': os.environ.get('DATABASE_LOGIN'),
                    'password': os.environ.get('DATABASE_PASSWORD'),
                    'database': 'iclprod'
                }

            try:
                conn = mysql.connector.connect(**config)
                cursor = conn.cursor()

                cursor.execute("Select idClient from client where Client = '" + theClient + "'")
                idclient = cursor.fetchone()
                if idclient is not None:
                    cursor.execute(
                        "SELECT column_name FROM information_schema.columns where "
                        "ordinal_position = 1 and table_schema = 'iclprod' and table_name = '" + self.databaseTableName + "'")
                    tablePrimaryKeyColumn = cursor.fetchone()
                    cursor.execute("select max(" + tablePrimaryKeyColumn[0] + ")+1 from " + self.databaseTableName + " ;")
                    rowNumber = cursor.fetchone()
                    print(
                        "INSERT INTO " + self.databaseTableName + " (idClient," + str(tablePrimaryKeyColumn[0]) + "," +
                        ",".join(l for l in fieldnames) + ") VAlUES (" + str(idclient[0]) + "," + str(rowNumber[0])
                        + "," + ",".join(l for l in values) + ");")
                    cursor.execute(
                        "INSERT INTO " + self.databaseTableName + " (idClient," + str(tablePrimaryKeyColumn[0]) + "," +
                        ",".join(l for l in fieldnames) + ") VAlUES (" + str(idclient[0]) + "," + str(rowNumber[0])
                        + "," + ",".join(l for l in values) + ");")
                    cursor.execute("select LAST_INSERT_ID();")

                else:
                    print("Client not found")
            except (mysql.connector.Error, mysql.connector.errors.ProgrammingError) as err:
                print(err)

    def exporttoCSV(self):
        if self.data is not None:
            ada = pd.DataFrame(list(self.data.items()), columns=['Name', 'Value'])
            ada.to_csv(self.filename[:5] + ".csv", index=False)
            print("Filename: " + self.filename[:5] + " exported to csv")

    def getServiceareaname(self):
        try:
            self.service_area_name = self.data["Form"]["Name"]
            return True
        except:
            self.addToErrormessage("\nService Area Name is missing something worth checking\n")
            return False

    def extraStepsForDbBeforeLoad(self):
        if self.getServiceareaname():
            self.getServiceAreaid(self.service_area_name)


class servers(allCognitoProcess):

    def __init__(self, test: bool, filename: str):
        super().__init__(test, filename)
        self.typeOfServer = []

    def mainRun(self):
        self.getData()

        self.cleanPojectInfo()
        self.valueDataCheck()
        self.getTheTypeOfServers()
        self.serverSplitByType()
        # self.formCheck() # This is the function that will check the form fileds vs DB fields and send an email if it is not correct
        # self.loadDataToDatabese() #This is the main function that will load the data to the database

        #self.test()
        #self.exporttoCSV()

    def test(self):
        print(self.data["HPC"])
        if not "000".isdigit():
            print("000 is a number")

    def getTheTypeOfServers(self):
        if self.data is not None:
            self.typeOfServer = self.data["P900IServerTypesI"].split(",")
            for k in self.typeOfServer:
                if k.startswith(" "):
                    self.typeOfServer.remove(k)
                    self.typeOfServer.append(k.strip())
            self.typeOfServer.append("All")
            self.data.pop("P900IServerTypesI")

            self.serverTypesNumberRef = {"Wintel": "111", "Unix": "222", "Virtual Environment": "333",
                                     "AS/400 (i Series)": "444", "Novell": "555", "VMS": "666", "HPC": "777",
                                     "Other": "888", "All": "000"}
            self.project_info = {key: self.project_info[key] for key in self.project_info if not key.startswith("IServerTypeI") }

    def serverSplitByType(self):
        #print(self.typeOfServer)
        tempdict = {}
        out = {}
        for k in self.serverTypesNumberRef.keys():
            if k in self.typeOfServer:
                for key, value in self.data.items():
                    if key[-3:] == self.serverTypesNumberRef[k]:
                        tempdict[key] = value
                    if not key[-3:].isdigit():
                        tempdict[key] = value
                out[k] = tempdict
                tempdict = {} # reset the tempdict .clear() does not work
        self.data = out

    def loadDataToDatabese(self):
        if self.data is not None:
            temp = self.data
            for k in temp.keys():
                self.data = temp[k]
                super().loadDataToDatabese()

    #def formCheck(self):
    #    super().formCheck()


class dbs(allCognitoProcess):

    def __init__(self, test: bool, filename: str):
        super().__init__(test, filename)
        self.typeOfDatabase = []

    def mainRun(self):
        self.getData()
        self.cleanPojectInfo()
        self.valueDataCheck()
        self.getTheTypeOfDatabase()
        self.databaseSplitByType()
        # self.formCheck() # This is the function that will check the form fileds vs DB fields and send an email if it is not correct
        # self.loadDataToDatabese() #This is the main function that will load the data to the database

        #self.test()
        #self.exporttoCSV()

    def test(self):
        pass

    def getTheTypeOfDatabase(self):
        if self.data is not None:
            self.typeOfDatabase = self.data["900LDatabaseType"].split(",")
            self.typeOfDatabase = [k.replace(" ", "") for k in self.typeOfDatabase]

            self.typeOfDatabase.append("All")
            self.data.pop("900LDatabaseType")
            self.databaseTypesNumberRef = {"Oracle": "111", "SQL": "222", "DB2": "333", "Progress(OpenEdge)": "444",
                                    "Informix": "555", "Sybase": "666", "Foxpro": "777", "Other": "888", "All": "000"}

            self.project_info = {key: self.project_info[key] for key in self.project_info if not key.startswith("LDatabaseType")}

    def databaseSplitByType(self):
        #print(self.typeOfDatabase)
        tempdict = {}
        out = {}
        for k in self.databaseTypesNumberRef.keys():
            if k in self.typeOfDatabase:
                for key, value in self.data.items():
                    if key[-3:] == self.databaseTypesNumberRef[k]:
                        tempdict[key] = value
                    if not key[-3:].isdigit():
                        tempdict[key] = value
                out[k] = tempdict
                tempdict = {} # reset the tempdict .clear() does not work
        self.data = out

    def loadDataToDatabese(self):
        if self.data is not None:
            temp = self.data
            for k in temp.keys():
                self.data = temp[k]
                super().loadDataToDatabese()

    def formCheck(self):
        super().formCheck()


class datacentre(allCognitoProcess):

    def __init__(self, test: bool, filename: str):
        super().__init__(test, filename)
        self.numberOfDatacentre = 0

    def mainRun(self):
        self.getData()
        self.cleanPojectInfo()
        self.valueDataCheck()

    #-----------------------------------------------------------------------------------------------

    #  only datacentre left and test the others.
    #  application list ?? or cloud  ??? or Projects ??? ProjectInformation ???
    #
    #-----------------------------------------------------------------------------------------------



        # self.formCheck() # This is the function that will check the form fileds vs DB fields and send an email if it is not correct
        # self.loadDataToDatabese() #This is the main function that will load the data to the database

        # self.test()
        # self.exporttoCSV()

    def test(self):
        pass


    def loadDataToDatabese(self):
        if self.data is not None:
            temp = self.data
            for k in temp.keys():
                self.data = temp[k]
                super().loadDataToDatabese()

    def formCheck(self):
        super().formCheck()



def getinfo():
    import_path = "C:/Users/" + user + "/Dropbox (ImprovIT)/ICL DB Import Folder/ICL Form Converter/Import"
    for x in os.listdir(import_path):
        if x.endswith(".json"):
            return x


if __name__ == "__main__":
    test = True # In test Change this to "yes" to run the program

    while True:
        filename = getinfo()
        if filename is None:
            print(" \r{}".format("I`m Running...Ready for Cognito... Nothing in Import Folder "+str(datetime.today().time())), end=" ")
        else:
            print("Starting...")
            try:
                if "servers" in filename:
                    file = servers(test, filename).mainRun()
                elif "dbs" in filename:
                    file = dbs(test, filename).mainRun()
                elif "data_centre" in filename:
                    file = datacentre(test, filename).mainRun()
                elif "ProjectInfo" in filename:
                    file = allCognitoProcess(test, filename)
                    file.mainRun()
                else:
                    file = allCognitoProcess(test, filename)
                    file.mainRun()
                    file.exporttoCSV()

                if file.errormessage != "" or file.errormessage != "":
                    Email(file.errormessage + file.infomessage, file.client_id, Test=test).Send()
                print("Done...")
            except Exception as e:
                Email(str(e), "None", Test=test).Send()

        time.sleep(15)



"""
if __name__ == "__main__":
    while True: # just normal while and break  so it's need a main run  ?? excel will be the same script or separate run??

        the_file, fileprecheck = thenew.FilePreCheck()
        #print(the_file,fileprecheck)
        if not the_file:
            print(" \r{}".format("I`m Running...Ready for Cognito... Nothing in Import Folder "+str(datetime.datetime.today().time())),end=" ")
            #time.sleep(10)
            #break
        elif fileprecheck != "No":
            print("Start")
            dbname = the_file[:-5]
            if dbname == "data_centre":

                Howmany_dc, transposedata = thenew.number_of_rounds(the_file)
                DC1, DC2, DC3, DC4, Attached_answer, What_to_do, Number_of_Attachements = thenew.import_data_for_datacetre(transposedata)
                xx = 0

                field_names_original = thenew.connect_the_database_to_match(dbname)

                while xx < Howmany_dc:
                    if xx == 0:
                        passed_data = DC1
                        DBSname = "DC1"
                    elif xx == 1:
                        passed_data = DC2
                        DBSname = "DC2"
                    elif xx == 2:
                        passed_data = DC3
                        DBSname = "DC3"
                    elif xx == 3:
                        passed_data = DC4
                        DBSname = "DC4"
                    xx += 1
                    Cleandata, temp_original = thenew.datacentre_multiple_execution(passed_data)
                    thenew.Upload_the_data(Cleandata, dbname, What_to_do)
                    if What_to_do != "Complete":
                        thenew.Calculating_numbercheck(Cleandata, dbname)
                    list_of_different_items = list(filter(lambda a: a not in field_names_original, temp_original))
                    list_of_different_items2 = list(filter(lambda b: b not in temp_original, field_names_original))

                    thenew.send_email_with_the_field(list_of_different_items, list_of_different_items2, Number_of_Attachements, dbname)
            elif dbname == 'dbs':
                Howmany_round, transposedata = thenew.number_of_rounds(the_file)
                if len(Howmany_round) > 1:
                    Howmany_round.append('All')
                the_111, the_222, the_333, the_444, the_555, the_666, the_777, the_888, the_000, Attached_answer, What_to_do, Number_of_Attachements  = thenew.servers_dbs_import(transposedata)
                list_of_different_items3 = ""
                field_names_original = thenew.connect_the_database_to_match(dbname)
                while Howmany_round: # should replace s in list drop but change the name
                    if "Oracle" in Howmany_round:
                        Howmany_round.remove("Oracle")
                        passed_data = the_111
                        DBSname = "Oracle"
                    elif "SQL" in Howmany_round:
                        Howmany_round.remove("SQL")
                        passed_data = the_222
                        DBSname = "SQL"
                    elif "DB2" in Howmany_round:

                        Howmany_round.remove("DB2")
                        passed_data = the_333
                        DBSname = "DB2"
                    elif "Progress (OpenEdge)" in Howmany_round:
                        Howmany_round.remove("Progress (OpenEdge)")
                        passed_data = the_444
                        DBSname = "Progress (OpenEdge)"
                    elif "Informix" in Howmany_round:
                        Howmany_round.remove("Informix")
                        passed_data = the_555
                        DBSname = "Informix"
                    elif "Sybase" in Howmany_round:
                        Howmany_round.remove("Sybase")
                        passed_data = the_666
                        DBSname = "Sybase"
                    elif "Foxpro" in Howmany_round:
                        Howmany_round.remove("Foxpro")
                        passed_data = the_777
                        DBSname = "Foxpro"
                    elif "Other" in Howmany_round:
                        Howmany_round.remove("Other")
                        passed_data = the_888
                        DBSname = "Other"
                    elif "All" in Howmany_round:
                        Howmany_round.remove("All")
                        passed_data = the_000
                        DBSname = "All"
                    Cleandata, temp_original = thenew.datacentre_multiple_execution(passed_data)
                    list_of_different_items = list(filter(lambda a: a not in field_names_original, temp_original))
                    list_of_different_items2 = list(filter(lambda b: b not in temp_original, field_names_original))
                    thenew.Upload_the_data(Cleandata, dbname, What_to_do)
                    thenew.Calculating_numbercheck(Cleandata, dbname)

                    thenew.send_email_with_the_field(list_of_different_items, list_of_different_items2,
                                                     Number_of_Attachements, dbname)
            elif dbname == 'servers':

                Howmany_round, transposedata = thenew.number_of_rounds(the_file)
                if len(Howmany_round) > 1:
                    Howmany_round.append('Total')

                the_111, the_222, the_333, the_444, the_555, the_666, the_777, the_888, the_000, Attached_answer, Status_report, Number_of_Attachements = thenew.servers_dbs_import( transposedata)
                list_of_different_items3 = ""
                field_names_original = thenew.connect_the_database_to_match(dbname)

                while Howmany_round: # use dictionary if this grow
                    if "Wintel" in Howmany_round:
                        Howmany_round.remove("Wintel")
                        passed_data = the_111
                        DBSname = "Wintel"
                    elif "Unix/Linux" in Howmany_round:
                        Howmany_round.remove("Unix/Linux")
                        passed_data = the_222
                        DBSname = "Unix/Linux"
                    elif "Virtual Environment" in Howmany_round:
                        Howmany_round.remove("Virtual Environment")
                        passed_data = the_333
                        DBSname = "Virtual Environment"
                    elif "AS/400 (i Series)" in Howmany_round:
                        Howmany_round.remove("AS/400 (i Series)")
                        passed_data = the_444
                        DBSname = "AS/400 (i Series)"
                    elif "Novell" in Howmany_round:
                        Howmany_round.remove("Novell")
                        passed_data = the_555
                        DBSname = "Novell"
                    elif "VMS" in Howmany_round:
                        Howmany_round.remove("VMS")
                        passed_data = the_666
                        DBSname = "VMS"
                    elif "HPC" in Howmany_round:
                        Howmany_round.remove("HPC")
                        passed_data = the_777
                        DBSname = "HPC"
                    elif "Other" in Howmany_round:
                        Howmany_round.remove("Other")
                        passed_data = the_888
                        DBSname = "Other"
                    elif "Total" in Howmany_round:
                        Howmany_round.remove("Total")
                        passed_data = the_000
                        DBSname = "Total"

                    Cleandata, temp_original  = thenew.datacentre_multiple_execution(passed_data)

                    list_of_different_items = list(filter(lambda a: a not in field_names_original, temp_original))
                    list_of_different_items2 = list(filter(lambda b: b not in temp_original, field_names_original))

                    thenew.Upload_the_data(Cleandata, dbname, Status_report)
                    if Status_report != "Complete":
                        thenew.Calculating_numbercheck(Cleandata, dbname)


                    thenew.send_email_with_the_field(list_of_different_items, list_of_different_items2, Number_of_Attachements, dbname)
            elif dbname == 'Cloud':
                #data = thenew.import_the_data(the_file)
                thenew.Cloud_Tables_split()

            elif dbname == 'ProjectInfo':
                data = thenew.import_the_data(the_file)
                Cleandata, temp_original, Attached_answer, What_to_do, Number_of_Attachements = thenew.cleaning_dataframes(data)
                ProjectInfo.Client_Check_upload(Cleandata)
                # send email what happened
            elif dbname == 'ProjectSummary':
                thenew.ProjectSummary()
                thenew.Email_sys("Processed, ProjectSummary", "ProjectSummary")
                #message = "This is in design phase no upload or any data calculation. Need to review "
                #thenew.Email_sys(message)
            else:

                data = thenew.import_the_data(the_file)

                Cleandata, temp_original, Attached_answer, What_to_do, Number_of_Attachements = thenew.cleaning_dataframes(data)

                field_names_original = thenew.connect_the_database_to_match(dbname)
                # compare the list of DB fieldname to Cognito filed name
                thenew.Upload_the_data(Cleandata, dbname, What_to_do)
                list_of_different_items = list(filter(lambda a: a not in field_names_original, temp_original))
                list_of_different_items2 = list(filter(lambda b: b not in temp_original, field_names_original))

                thenew.send_email_with_the_field(list_of_different_items, list_of_different_items2, Number_of_Attachements, dbname)
                print("Done")
                if What_to_do != "Complete":
                    thenew.Calculating_numbercheck(Cleandata, dbname)




        time.sleep(20)


"""
