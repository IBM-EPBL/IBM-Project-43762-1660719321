import inventory.CloudDB2 as DB
import pandas as pd


class Inventory:
    def __init__(self):
        self.Id = ""
        self.Category = ""
        self.ItemName = ""
        self.VendorId = 0
        self.Wholesaleprice = 0
        self.Retailprice = 0
        self.Qty = 0
        self.Low_Stock_Limit = 0
        self.LotNo = ""
        self.Note = ""

        query = "select count(ID) from inventory"
        nos = DB.check(query)
        print(nos)
        if nos == 0:
            query = "create table inventory(ID INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 1 " \
                    "INCREMENT BY 1), VendorId INT NOT NULL, Category VARCHAR(75) NOT NULL, " \
                    "ItemName VARCHAR(75) NOT NULL, Wholesaleprice INT NOT NULL, Retailprice INT NOT NULL, " \
                    "Qty INT NOT NULL, Low_Stock_Limit INT NOT NULL, LotNo VARCHAR(50), Note VARCHAR(50) )"
            DB.run(query)

    def save(self):

        if self.Id != "":
            query = "update inventory set VendorId='{}', Category='{}'" \
                    ",ItemName='{}'" \
                    ",Wholesaleprice='{}'" \
                    ",Retailprice='{}'" \
                    ",Qty='{}'" \
                    ",Low_Stock_Limit='{}'" \
                    ",LotNo='{}'" \
                    ",Note='{}'" \
                    " WHERE ID = '{}'".format(self.VendorId, self.Category, self.ItemName, self.Wholesaleprice,
                                              self.Retailprice,
                                              self.Qty, self.Low_Stock_Limit, self.LotNo, self.Note, self.Id)
        else:
            query = "insert into inventory(VendorId, Category, ItemName, Wholesaleprice, Retailprice, Qty, " \
                    "Low_Stock_Limit, LotNo, Note) VALUES('{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}')" \
                .format(self.VendorId, self.Category, self.ItemName, self.Wholesaleprice, self.Retailprice, self.Qty,
                        self.Low_Stock_Limit, self.LotNo, self.Note)
        DB.run(query)

    def get(self, id):
        return DB.view("select * from inventory where VendorId = " + str(self.VendorId) + " and ID=" + str(id))

    def get_low_stock(self):
        return DB.view("select * from inventory where VendorId = " + str(self.VendorId) + " and "
                                                                                          "Qty <= Low_Stock_Limit")

    def display(self):
        return DB.view("select * from inventory where VendorId = " + str(self.VendorId))
