import inventory.CloudDB2 as DB
import pandas as pd


class Vendor:
    def __init__(self):
        self.Id = ""
        self.Name = ""
        self.Shop_Name = ""
        self.GST = ""
        self.Address = ""
        self.Mobile = ""
        self.Email = ""
        self.Password = ""
        query = "select count(ID) from vendors"
        nos = DB.check(query)
        print(nos)
        if nos == 0:
            query = "create table vendors(ID INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 1 " \
                    "INCREMENT BY 1), Name VARCHAR(75) NOT NULL, " \
                    "Shop_Name VARCHAR(75) NOT NULL, GST VARCHAR(30) NOT NULL, Address VARCHAR(255), " \
                    "Mobile VARCHAR(15) NOT NULL, Email VARCHAR(50), Password VARCHAR(50) )"
            DB.run(query)

    def save(self):
        print(self.Name)

        if self.Id != "":
            query = "update vendors set Name='{self.Name}'" \
                    ",Shop_Name='{self.Shop_Name}'" \
                    ",GST='{self.GST}'" \
                    ",Address='{self.Address}'" \
                    ",Mobile='{self.Mobile}'" \
                    ",Email='{self.Email}'" \
                    ",Password='{self.Password}'" \
                    " WHERE ID = '{self.Id}'"
        else:
            query = "insert into vendors(Name, Shop_Name, GST, Address, Mobile, Email, Password) " \
                    "VALUES('{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}')" \
                .format(self.Name, self.Shop_Name, self.GST, self.Address, self.Mobile, self.Email, self.Password)

        DB.run(query)

    def login(self):
        query = "select * from vendors WHERE Email='{}' and Password='{}'".format(self.Email, self.Password)
        return DB.view(query)

    def get(self, id):
        return DB.view("select * from vendors where ID = '" + str(id) + "'")

    def display(self):
        return DB.view("select * from vendors")
