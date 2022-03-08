from app import session


def runTriggers():
    afterGuestCheckin()
    afterGuestApart()
    updatePstatus()
    updateCaridInCustomer()


def afterGuestCheckin():
    session.execute("DROP TRIGGER IF EXISTS afterGuestCheckin")
    session.commit()
    inst = "CREATE TRIGGER afterGuestCheckin " \
           "AFTER INSERT ON CustomerCheck " \
           "FOR EACH ROW " \
           "UPDATE Room SET Rstatus = '已住' WHERE Rno = new.Rno;"
    session.execute(inst)
    session.commit()


def afterGuestApart():
    session.execute("DROP TRIGGER IF EXISTS afterGuestApart")
    session.commit()
    inst = "CREATE TRIGGER afterGuestApart " \
           "AFTER UPDATE ON CustomerCheck " \
           "FOR EACH ROW " \
           "UPDATE Room SET Rstatus = '空' WHERE Rno = new.Rno;"
    session.execute(inst)
    session.commit()


#更新停车场管理表后，自动改变相关的车位信息
def updatePstatus():
    session.execute("DROP TRIGGER IF EXISTS updatePstatus")
    session.commit()
    inst = "CREATE TRIGGER updatePstatus " \
           "AFTER UPDATE ON ParkingManagement " \
           "FOR EACH ROW " \
           "BEGIN "\
           "UPDATE ParkingLot SET Pstatus = '空' WHERE Pposition = old.CARposition;"\
           "UPDATE ParkingLot SET Pstatus = '已停' WHERE Pposition = new.CARposition;"\
           "END;"
    session.execute(inst)
    session.commit()


#录入顾客信息时，自动根据停车信息中的联系方式填写车牌
def updateCaridInCustomer():
    session.execute("DROP TRIGGER IF EXISTS updateCaridInCustomer")
    session.commit()
    inst = "CREATE TRIGGER updateCaridInCustomer " \
           "BEFORE INSERT ON Customer " \
           "FOR EACH ROW " \
           "BEGIN "\
           "SELECT Carid INTO @id FROM ParkingManagement WHERE Cnumber = new.Cnumber;"\
           "SET new.Carid=@id;"\
           "END;"
           # "UPDATE Customer c,ParkingManagement p "\
           # "SET c.Carid = p.Carid "\
           # "WHERE c.Cnumber=p.Cnumber;"
    session.execute(inst)
    session.commit()


def updateCarid():
    session.execute("DROP TRIGGER IF EXISTS updateCarids")
    session.commit()
    inst = "CREATE TRIGGER updateCarids " \
           "AFTER DELETE ON ParkingManagement " \
           "FOR EACH ROW " \
           "DELETE FROM Car WHERE CARid = old.CARid;"
    session.execute(inst)
    session.commit()