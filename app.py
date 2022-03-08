from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from sqlalchemy import *
from trigger import *
from secret_key import randomstring, check_password
import datetime

# 创建数据库连接
# import app

engine = create_engine("mysql+pymysql://root:335566@127.0.0.1:3306/test5?charset=utf8", max_overflow=0,
                       pool_size=5)
#  mysql+pymysql://{用户名，一般是root}:{密码}@{本地}:3306/{数据库名字，要自己先去mysql建好再使用这个}?charset=utf8


Session = scoped_session(sessionmaker(bind=engine))

session = Session()

Base = declarative_base()


class Room(Base):
    __tablename__ = "Room"

    Rno = Column(Integer, primary_key=True)
    Rstorey = Column(Integer)
    Rstatus = Column(Enum('空', '已住'))
    Rcode = Column(VARCHAR(length=10))

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class CodeInf(Base):
    __tablename__ = 'CodeInf'

    Rcode = Column(VARCHAR(length=10), primary_key=True)
    Rtype = Column(Enum('豪华', '标准'))
    Rscale = Column(Enum('单人', '双人'))
    Rprice = Column(Integer)
    Mno = Column(VARCHAR(length=10))

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class Customer(Base):
    __tablename__ = 'Customer'

    Cid = Column(BIGINT, primary_key=True)
    Cname = Column(String(length=40))
    Csex = Column(Enum('男', '女'))
    Cnumber = Column(VARCHAR(length=40))
    Carid = Column(String(length=60), nullable=True)

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class Receptionist(Base):
    __tablename__ = 'Receptionist'

    RECPno = Column(VARCHAR(length=10), primary_key=True)
    RECPname = Column(String(length=40))
    RECPsalary = Column(Integer)
    Mno = Column(VARCHAR(length=10))
    RECPpass = Column(String(length=80))

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class Waiter(Base):
    __tablename__ = 'Waiter'

    Wno = Column(VARCHAR(length=10), primary_key=True)
    Wname = Column(String(length=40))
    Wsalary = Column(Integer)
    Mno = Column(VARCHAR(length=10))

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class WorkHistory(Base):
    __tablename__ = 'WorkHistory'

    Ename = Column(String(length=40))
    Eno = Column(VARCHAR(length=10), primary_key=True)
    Etype = Column(Enum('R', 'W'))  # R means receptionist; W means waiter
    Etime = Column(VARCHAR(length=20))
    Qtime = Column(VARCHAR(length=20), nullable=True)

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class Car(Base):
    __tablename__ = 'Car'

    CARid = Column(String(length=60), primary_key=True)
    CARcolor = Column(String(length=40), nullable=True)

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class Manager(Base):
    __tablename__ = 'Manager'

    Mno = Column(VARCHAR(length=10), primary_key=True)
    Mname = Column(String(length=40))
    Mpass = Column(String(length=80))

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class CustomerCheck(Base):
    __tablename__ = 'CustomerCheck'

    Cid = Column(BIGINT, primary_key=True)
    Rno = Column(Integer, primary_key=True)
    RECPno = Column(VARCHAR(length=10))
    Atime = Column(VARCHAR(length=40))
    Ltime = Column(VARCHAR(length=40), nullable=True)

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class ParkingLot(Base):
    __tablename__ = 'ParkingLot'

    Pposition = Column(Integer, primary_key=True)
    Pstatus = Column(Enum('空', '已停'))

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class ParkingManagement(Base):
    __tablename__ = 'ParkingManagement'

    CARid = Column(String(length=60), primary_key=True)
    CARposition = Column(Integer)
    Itime = Column(VARCHAR(length=40))
    Cnumber = Column(VARCHAR(length=40))

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class EmployeeRoom(Base):
    __tablename__ = 'EmployeeRoom'

    Rno = Column(Integer, primary_key=True)
    Wno = Column(VARCHAR(length=10))
    RECPno = Column(VARCHAR(length=10))

    def save(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def move_away(self):
        session.delete(self)
        session.commit()


app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = randomstring(8)
bootstrap = Bootstrap(app)

MAno = None
REno = None


@app.route('/', methods=['GET', 'POST'])
def home():
    # initialization
    if not session.query(CodeInf).filter(CodeInf.Rcode == 'A1').first():
        code_inf = CodeInf(Rcode='A1', Rtype='豪华', Rscale='单人', Rprice=100, Mno='M1')
        code_inf.save()
    if not session.query(CodeInf).filter(CodeInf.Rcode == 'A2').first():
        code_inf = CodeInf(Rcode='A2', Rtype='豪华', Rscale='双人', Rprice=200, Mno='M2')
        code_inf.save()
    if not session.query(CodeInf).filter(CodeInf.Rcode == 'B1').first():
        code_inf = CodeInf(Rcode='B1', Rtype='标准', Rscale='单人', Rprice=50, Mno='M1')
        code_inf.save()
    if not session.query(CodeInf).filter(CodeInf.Rcode == 'B2').first():
        code_inf = CodeInf(Rcode='B2', Rtype='标准', Rscale='双人', Rprice=90, Mno='M2')
        code_inf.save()
    if not session.query(ParkingLot).filter(ParkingLot.Pposition == 1).first():
        lot = ParkingLot(Pposition=1, Pstatus='空')
        lot.save()
    if not session.query(ParkingLot).filter(ParkingLot.Pposition == 2).first():
        lot = ParkingLot(Pposition=2, Pstatus='空')
        lot.save()
    if not session.query(ParkingLot).filter(ParkingLot.Pposition == 3).first():
        lot = ParkingLot(Pposition=3, Pstatus='空')
        lot.save()
    if not session.query(ParkingLot).filter(ParkingLot.Pposition == 4).first():
        lot = ParkingLot(Pposition=4, Pstatus='空')
        lot.save()
    if not session.query(ParkingLot).filter(ParkingLot.Pposition == 5).first():
        lot = ParkingLot(Pposition=5, Pstatus='空')
        lot.save()
    if not session.query(ParkingLot).filter(ParkingLot.Pposition == 6).first():
        lot = ParkingLot(Pposition=6, Pstatus='空')
        lot.save()
    if not session.query(Manager).filter(Manager.Mno == 'M001').first():
        str = randomstring(10)
        temp_password = str[0:2] + '654321' + str[2:10]
        manager = Manager(Mno='M001', Mname='Czl', Mpass=temp_password)
        manager.save()
    if not session.query(Manager).filter(Manager.Mno == 'M002').first():
        str = randomstring(10)
        temp_password = str[0:2] + '0987' + str[2:10]
        manager = Manager(Mno='M002', Mname='Hbh', Mpass=temp_password)
        manager.save()
    if not session.query(Manager).filter(Manager.Mno == 'M003').first():
        str = randomstring(10)
        temp_password = str[0:2] + '97531' + str[2:10]
        manager = Manager(Mno='M003', Mname='Zhw', Mpass=temp_password)
        manager.save()
    if not session.query(Room).filter(Room.Rno == 101).first():
        room = Room(Rno=101, Rstorey=1, Rstatus='空', Rcode='B1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 102).first():
        room = Room(Rno=102, Rstorey=1, Rstatus='空', Rcode='B1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 103).first():
        room = Room(Rno=103, Rstorey=1, Rstatus='空', Rcode='B1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 104).first():
        room = Room(Rno=104, Rstorey=1, Rstatus='空', Rcode='B1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 105).first():
        room = Room(Rno=105, Rstorey=1, Rstatus='空', Rcode='B2')
        room.save()
    if not session.query(Room).filter(Room.Rno == 106).first():
        room = Room(Rno=106, Rstorey=1, Rstatus='空', Rcode='B2')
        room.save()
    if not session.query(Room).filter(Room.Rno == 107).first():
        room = Room(Rno=107, Rstorey=1, Rstatus='空', Rcode='B2')
        room.save()
    if not session.query(Room).filter(Room.Rno == 108).first():
        room = Room(Rno=108, Rstorey=1, Rstatus='空', Rcode='B2')
        room.save()
    if not session.query(Room).filter(Room.Rno == 201).first():
        room = Room(Rno=201, Rstorey=2, Rstatus='空', Rcode='B1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 202).first():
        room = Room(Rno=202, Rstorey=2, Rstatus='空', Rcode='B1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 203).first():
        room = Room(Rno=203, Rstorey=2, Rstatus='空', Rcode='B1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 204).first():
        room = Room(Rno=204, Rstorey=2, Rstatus='空', Rcode='B1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 205).first():
        room = Room(Rno=205, Rstorey=2, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 206).first():
        room = Room(Rno=206, Rstorey=2, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 207).first():
        room = Room(Rno=207, Rstorey=2, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 208).first():
        room = Room(Rno=208, Rstorey=2, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 301).first():
        room = Room(Rno=301, Rstorey=3, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 302).first():
        room = Room(Rno=302, Rstorey=3, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 303).first():
        room = Room(Rno=303, Rstorey=3, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 304).first():
        room = Room(Rno=304, Rstorey=3, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 305).first():
        room = Room(Rno=305, Rstorey=3, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 306).first():
        room = Room(Rno=306, Rstorey=3, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 307).first():
        room = Room(Rno=307, Rstorey=3, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 308).first():
        room = Room(Rno=308, Rstorey=3, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 401).first():
        room = Room(Rno=401, Rstorey=4, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 402).first():
        room = Room(Rno=402, Rstorey=4, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 403).first():
        room = Room(Rno=403, Rstorey=4, Rstatus='空', Rcode='A1')
        room.save()
    if not session.query(Room).filter(Room.Rno == 404).first():
        room = Room(Rno=404, Rstorey=4, Rstatus='空', Rcode='A1')
        room.save()
    return render_template("homePage.html")


def currentTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global MAno, REno
    MAno = None
    REno = None
    return render_template('homePage.html')


@app.route('/waiter_passwordChange', methods=['GET', 'POST'])
def waiter_passwordChange():
    if request.method == 'GET':
        return render_template("waiter_passwordChange.html")
    else:
        if 'Oldpass' in request.form and 'Newpass' in request.form \
                and not request.form['Oldpass'] == '' and not request.form['Newpass'] == '':
            old = request.form['Oldpass']
            correct = session.query(Receptionist).filter(Receptionist.RECPno == REno).first()
            passWord = correct.RECPpass
            if not check_password(old, passWord):
                return render_template("login_error.html")
            newpass = request.form['Newpass']
            str_temp = randomstring(10)
            temp_password = str_temp[0:2] + newpass[::-1] + str_temp[2:10]
            correct.RECPpass = temp_password
            correct.update()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/manager_passwordChange', methods=['GET', 'POST'])
def manager_passwordChange():
    if request.method == 'GET':
        return render_template("manager_passwordChange.html")
    else:
        if 'Oldpass' in request.form and 'Newpass' in request.form \
                and not request.form['Oldpass'] == '' and not request.form['Newpass'] == '':
            old = request.form['Oldpass']
            correct = session.query(Manager).filter(Manager.Mno == MAno).first()
            passWord = correct.Mpass
            if not check_password(old, passWord):
                return render_template("login_error.html")
            newpass = request.form['Newpass']
            str_temp = randomstring(10)
            temp_password = str_temp[0:2] + newpass[::-1] + str_temp[2:10]
            correct.Mpass = temp_password
            correct.update()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/waiter_login', methods=['GET', 'POST'])
def waiter_login():
    global REno
    if request.method == 'GET' and REno is None:
        return render_template("waiter_login.html")
    elif REno is not None:
        return render_template("waiter_homePage.html")
    else:
        if 'RECPno' in request.form and 'RECPpass' in request.form:
            RECPno = request.form['RECPno']
            RECPpass = request.form['RECPpass']
        else:
            return render_template("login_error.html")
        if not session.query(Receptionist).filter(Receptionist.RECPno == RECPno).first():
            return render_template("login_error.html")
        pass_temp = session.query(Receptionist.RECPpass).filter(Receptionist.RECPno == RECPno).first()
        right_pass = pass_temp[0]
        if not check_password(RECPpass, right_pass):
            return render_template("login_error.html")
        REno = RECPno
        global MAno
        MAno = None
        # print(REno)
        return render_template("waiter_homePage.html")


@app.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
    global MAno
    if request.method == 'GET' and MAno is None:
        return render_template("manager_login.html")
    elif MAno is not None:
        return render_template("manager_homePage.html")
    else:
        if 'Mno' in request.form and 'Mpass' in request.form:
            Mno = request.form['Mno']
            Mpass = request.form['Mpass']
            if session.query(Manager).filter(Manager.Mno == Mno).first():
                pass_temp = session.query(Manager.Mpass).filter(Manager.Mno == Mno).first()
                right_pass = pass_temp[0]
                if not check_password(Mpass, right_pass):
                    return render_template("login_error.html")
                MAno = Mno
                # print('after: ' + MAno)
                global RECPno
                RECPno = None
                # session['Mno'] = Mpass
                return render_template("manager_homePage.html")
        return render_template("login_error.html")


@app.route('/guest_homePage', methods=['GET', 'POST'])
def guest_home():
    return render_template("guest_homePage.html")


@app.route('/waiter_homePage', methods=['GET', 'POST'])
def waiter_home():
    return render_template("waiter_homePage.html")


@app.route('/manager_homePage', methods=['GET', 'POST'])
def manager_home():
    return render_template("manager_homePage.html")


@app.route('/guest_managerInformation_query', methods=['GET', 'POST'])
def guest_manager_query():
    if request.method == 'GET':
        return render_template("guest_managerInformation_query.html")
    else:
        if 'Mno' in request.form and not request.form['Mno'] == '':
            mno = request.form['Mno']
            ans = session.query(Manager.Mno, Manager.Mname).filter(Manager.Mno == mno).first()
            return render_template("guest_managerInformation_result.html", u=ans)
        return render_template("guest_emptyError.html")


@app.route('/guest_managerInformation_show', methods=['GET', 'POST'])
def guest_manager_show():
    ans = session.query(Manager.Mno, Manager.Mname).all()
    return render_template("guest_managerInformation_show.html", u=ans)


@app.route('/guest_parkingManage_query', methods=['GET', 'POST'])
def guest_car_query():
    if request.method == 'GET':
        return render_template("guest_parkingManage_query.html")
    else:
        if 'Cid' in request.form and not request.form['Cid'] == '':
            carId = request.form['Cid']
            ans = session.query(ParkingManagement.CARposition, ParkingManagement.Itime) \
                .filter(ParkingManagement.CARid == carId).all()
            return render_template("guest_parkingManage_result.html", u=ans)
        return render_template("guest_emptyError.html")


@app.route('/guest_parkingStatus_show', methods=['GET', 'POST'])
def guest_park_show():
    ans = session.query(ParkingLot.Pposition, ParkingLot.Pstatus).all()
    return render_template("guest_parkingStatus_show.html", u=ans)


@app.route('/waiter_room_show', methods=['GET', 'POST'])
def waiter_room_show():
    ans = session.query(Room.Rno, Room.Rstorey, Room.Rstatus, Room.Rcode).all()
    return render_template("waiter_room_show.html", u=ans)


@app.route('/waiter_room_query', methods=['GET', 'POST'])
def waiter_room_query():
    if request.method == 'GET':
        return render_template("waiter_room_query.html")
    else:
        if 'Rno' in request.form and not request.form['Rno'] == '':
            Rno = request.form['Rno']
            ans = session.query(Room.Rno, Room.Rstorey, Room.Rstatus, Room.Rcode).filter(
                Room.Rno == Rno or CodeInf.Rcode == Room.Rcode).all()
            return render_template("waiter_room_result.html", u=ans)
        return render_template("waiter_emptyError.html")


@app.route('/waiter_carInformation_delete', methods=['GET', 'POST'])
def waiter_car_delete():
    if request.method == 'GET':
        return render_template("waiter_carInformation_delete.html")
    else:
        if 'Cid' in request.form and not request.form['Cid'] == '':
            Carid = request.form['Cid']
            if not session.query(Car).filter(Car.CARid == Carid).first():
                return render_template("waiter_deleteError.html")
            session.query(Car).filter(Car.CARid == Carid).delete()
            session.commit()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_carInformation_insert', methods=['GET', 'POST'])
def waiter_car_insert():
    if request.method == 'GET':
        return render_template("waiter_carInformation_insert.html")
    else:
        if 'Gid' in request.form and 'Rno' in request.form and \
                not request.form['Gid'] == '' and not request.form['Rno'] == '':
            Carid = request.form['Gid']
            if session.query(Car).filter(Car.CARid == Carid).first():
                return render_template("waiter_insertError.html")
            flag_1 = 1 if (len(Carid) == 8 and Carid[2] == '_') else 0
            flag_3 = 1 if Carid[0:2].isalpha() else 0
            flag_2 = 1 if Carid[3:8].isalnum() else 0
            if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
                return render_template('waiter_error.html', u='车牌号格式不正确！')
            Carcolor = request.form['Rno']
            car = Car(CARid=Carid, CARcolor=Carcolor)
            car.save()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_carInformation_query', methods=['GET', 'POST'])
def waiter_car_query():
    if request.method == 'GET':
        return render_template("waiter_carInformation_query.html")
    else:
        if 'Cid' in request.form and not request.form['Cid'] == '':
            Carid = request.form['Cid']
            ans = session.query(Car.CARid, Car.CARcolor).filter(Car.CARid == Carid).all()
            return render_template("waiter_carInformation_result.html", u=ans)
        return render_template("waiter_emptyError.html")


@app.route('/waiter_carInformation_show', methods=['GET', 'POST'])
def waiter_car_show():
    ans = session.query(Car.CARid, Car.CARcolor).all()
    return render_template("waiter_carInformation_show.html", u=ans)


@app.route('/waiter_carInformation_update', methods=['GET', 'POST'])
def waiter_car_update():
    if request.method == 'GET':
        return render_template("waiter_carInformation_update.html")
    else:
        if 'Gid' in request.form and not request.form['Gid'] == '':
            Carid = request.form['Gid']
            Carcolor = request.form['Rno'] if 'Rno' in request.form else None
            if not session.query(Car).filter(Car.CARid == Carid).first():
                return render_template("waiter_updateError.html")
            toUpdate = session.query(Car).filter(Car.CARid == Carid).first()
            if Carcolor != '':
                toUpdate.CARcolor = Carcolor
            toUpdate.update()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_guestCheckin_delete', methods=['GET', 'POST'])
def waiter_checkin_delete():
    if request.method == 'GET':
        return render_template("waiter_guestCheckin_delete.html")
    else:
        if 'Gid' in request.form and not request.form['Gid'] == '':
            Cid = request.form['Gid']
            if not session.query(CustomerCheck).filter(CustomerCheck.Cid == Cid).first():
                return render_template("waiter_deleteError.html")
            if session.query(Customer).filter(Customer.Cid == Cid).first():
                return render_template("waiter_error.html", u='应该先删除顾客基本信息哦！')
            session.query(CustomerCheck).filter(CustomerCheck.Cid == Cid).delete()
            session.commit()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_guestCheckin_insert', methods=['GET', 'POST'])
def waiter_checkin_insert():
    if request.method == 'GET':
        return render_template("waiter_guestCheckin_insert.html")
    else:
        if 'Gid' in request.form and 'Rno' in request.form \
                and not request.form['Gid'] == '' and not request.form['Rno'] == '': #and not request.form['Atime'] == ''
            Cid = request.form['Gid']
            if not (len(Cid) == 18 and Cid.isalnum()):
                return render_template('waiter_error.html', u='请输入有效的身份证号码！')
            Rno = request.form['Rno']
            if not session.query(Room).filter(Room.Rno == Rno).first():
                return render_template('waiter_error.html', u='办理入住房间号不存在！')
            RECPno = REno
            Atime = currentTime()
            # Atime = request.form['Atime']
            # flag_3 = 1 if len(Atime) == 10 else 0
            # flag_2 = 1 if (Atime[0:4].isdigit() and Atime[5:7].isdigit() and Atime[8:10].isdigit()
            #                and 1 <= int(Atime[5:7]) <= 12 and 1 <= int(Atime[8:10]) <= 31) else 0
            # flag_1 = 1 if (Atime[4] == '.' and Atime[7] == '.') else 0
            # if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
            #     return render_template("waiter_error.html", u='请输入规范的入住日期！')

            if session.query(CustomerCheck).filter(and_(CustomerCheck.Cid == Cid, CustomerCheck.Rno == Rno)).first():
                return render_template("waiter_insertError.html")
            checkIn = CustomerCheck(Cid=Cid, Rno=Rno, RECPno=RECPno, Atime=Atime, Ltime="未离店")
            if not session.query(Room).filter(Room.Rno == Rno).first():
                return render_template("waiter_insertError.html")
            checkIn.save()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_guestCheckin_apart', methods=['GET', 'POST'])
def waiter_checkin_apart():
    if request.method == 'GET':
        return render_template("waiter_guestCheckin_apart.html")
    else:
        if 'Cid' in request.form and 'Rno' in request.form\
                and not request.form['Cid'] == '' and not request.form['Rno'] == '':# and not request.form['Ltime'] == '':
            Cid = request.form['Cid']
            Rno = request.form['Rno']
            Ltime = currentTime() #request.form['Ltime']
            if not (len(Cid) == 18 and Cid.isalnum()):
                return render_template('waiter_error.html', u='请输入有效的身份证号码！')

            if not (Rno.isdigit() and 101 <= int(Rno) <= 908):
                return render_template("waiter_error.html", u='房间号格式有误！')

            # flag_3 = 1 if len(Ltime) == 10 else 0
            # flag_2 = 1 if (Ltime[0:4].isdigit() and Ltime[5:7].isdigit() and Ltime[8:10].isdigit()
            #                and 1 <= int(Ltime[5:7]) <= 12 and 1 <= int(Ltime[8:10]) <= 31) else 0
            # flag_1 = 1 if (Ltime[4] == '.' and Ltime[7] == '.') else 0
            # if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
            #     return render_template("waiter_error.html", u='请输入规范的离店日期！')

            # instruction = "UPDATE CustomerCheck SET Ltime='" + Ltime + "' WHERE Cid='" + Cid + "' AND Rno='" + Rno + "';"
            # session.execute(instruction)
            # session.query(CustomerCheck).from_statement(text(instruction))
            toUpdate = session.query(CustomerCheck).filter(and_(CustomerCheck.Rno == Rno, CustomerCheck.Cid == Cid)) \
                .first()
            toUpdate.Ltime = Ltime
            toUpdate.update()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_guestCheckin_query', methods=['GET', 'POST'])
def waiter_checkin_query():
    if request.method == 'GET':
        return render_template("waiter_guestCheckin_query.html")
    else:
        if 'Gid' in request.form and not request.form['Gid'] == '':
            Cid = request.form['Gid']
            ans = session \
                .query(CustomerCheck.Cid, CustomerCheck.Rno, CustomerCheck.RECPno, CustomerCheck.Atime,
                       CustomerCheck.Ltime) \
                .filter(CustomerCheck.Cid == Cid).all()
            return render_template("waiter_guestCheckin_result.html", u=ans)
        return render_template("waiter_emptyError.html")


@app.route('/waiter_guestCheckin_show', methods=['GET', 'POST'])
def waiter_checkin_show():
    ans = session \
        .query(CustomerCheck.Cid, CustomerCheck.Rno, CustomerCheck.RECPno, CustomerCheck.Atime, CustomerCheck.Ltime) \
        .all()
    return render_template("waiter_guestCheckin_show.html", u=ans)


@app.route('/waiter_guestCheckin_update', methods=['GET', 'POST'])
def waiter_checkin_update():
    if request.method == 'GET':
        return render_template("waiter_guestCheckin_update.html")
    else:
        if 'Gid' in request.form and not request.form['Gid'] == '':
            Cid = request.form['Gid']
            Rno = request.form['Rno'] if 'Rno' in request.form else None
            RECPno = REno
            Ltime = currentTime() #request.form['Ltime'] if 'Ltime' in request.form else None
            if not session \
                    .query(CustomerCheck) \
                    .filter(and_(CustomerCheck.Cid == Cid, CustomerCheck.Rno == Rno)).first():
                return render_template("waiter_updateError.html")
            toUpdate = session \
                .query(CustomerCheck) \
                .filter(and_(CustomerCheck.Cid == Cid, CustomerCheck.Rno == Rno)).first()
            toUpdate.RECPno = RECPno
            # if Ltime != '':
            #     flag_3 = 1 if len(Ltime) == 10 else 0
            #     flag_2 = 1 if (Ltime[0:4].isdigit() and Ltime[5:7].isdigit() and Ltime[8:10].isdigit()
            #                    and 1 <= int(Ltime[5:7]) <= 12 and 1 <= int(Ltime[8:10]) <= 31) else 0
            #     flag_1 = 1 if (Ltime[4] == '.' and Ltime[7] == '.') else 0
            #     if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
            #         return render_template("waiter_error.html", u='请输入正确的离店时间！')
            toUpdate.Ltime = Ltime
            toUpdate.update()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_guestInformation_delete', methods=['GET', 'POST'])
def waiter_customer_delete():
    if request.method == 'GET':
        return render_template("waiter_guestInformation_delete.html")
    else:
        if 'Gid' in request.form and not request.form['Gid'] == '':
            Cid = request.form['Gid']
            if not session.query(Customer).filter(Customer.Cid == Cid).first():
                return render_template("waiter_deleteError.html")
            session.query(Customer).filter(Customer.Cid == Cid).delete()  # customer delete
            session.commit()
            '''
            toUpdate = session.query(CustomerCheck).filter(CustomerCheck.Cid == Cid).first()
            upRno = toUpdate.Rno
            toUpdate2 = session.query(Room).filter(Room.Rno == upRno).first()
            toUpdate2.Rstatus = '空'
            toUpdate2.update()  # room status changed when guest inf get deleted
            '''
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_guestInformation_insert', methods=['GET', 'POST'])
def waiter_customer_insert():
    if request.method == 'GET':
        return render_template("waiter_guestInformation_insert.html")
    else:
        if 'Gid' in request.form and 'Gname' in request.form and 'Gsex' in request.form and 'Gnum' in request.form \
                and not request.form['Gid'] == '' and not request.form['Gname'] == '' and not request.form['Gnum'] == '' \
                and not request.form['Gsex'] == '':
            Cid = request.form['Gid']
            if session.query(Customer).filter(Customer.Cid == Cid).first():
                return render_template("waiter_insertError.html")
            if not session.query(CustomerCheck).filter(CustomerCheck.Cid == Cid).first():
                return render_template('waiter_error.html', u='请先插入对应的入住信息！')
            if not (len(Cid) == 18 and Cid.isalnum()):
                return render_template('waiter_error.html', u='请输入有效的身份证号码！')
            Cname = request.form['Gname']
            Csex = request.form['Gsex']
            if not (Csex == '男' or Csex == '女'):
                return render_template('waiter_error.html', u='请输入有效性别')
            Cnumber = request.form['Gnum']
            if not (Cnumber.isdigit() and len(Cnumber) == 11):
                return render_template('waiter_error.html', u='请输入有效的电话号码！')
            Carid = request.form['Cid'] if request.form['Cid'] != '' else None
            if Carid:
                flag_1 = 1 if (len(Carid) == 8 and Carid[2] == '_') else 0
                flag_3 = 1 if Carid[0:2].isalpha() else 0
                flag_2 = 1 if Carid[3:8].isalnum() else 0
                if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
                    return render_template('waiter_error.html', u='车牌号格式不正确！')
            cus = Customer(Cid=Cid, Cname=Cname, Csex=Csex, Cnumber=Cnumber, Carid=Carid)
            cus.save()
            if not session.query(CustomerCheck).filter(CustomerCheck.Cid == Cid).first():
                return render_template("waiter_error.html", u='请先输入该顾客的对应入住信息')
            '''
            toUpdate = session.query(CustomerCheck).filter(CustomerCheck.Cid == Cid).first()
            upRno = toUpdate.Rno
            toUpdate2 = session.query(Room).filter(Room.Rno == upRno).first()
            toUpdate2.Rstatus = '已住'
            toUpdate2.update()  # room status changed when guest inf go in
            '''
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_guestInformation_query', methods=['GET', 'POST'])
def waiter_customer_query():
    if request.method == 'GET':
        return render_template("waiter_guestInformation_query.html")
    else:
        if 'Gid' in request.form and not request.form['Gid'] == '':
            Cid = request.form['Gid']
            ans = session.query(Customer.Cname, Customer.Csex, Customer.Cnumber, Customer.Carid).filter(
                Customer.Cid == Cid) \
                .all()
            return render_template("waiter_guestInformation_result.html", u=ans)
        return render_template("waiter_emptyError.html")


@app.route('/waiter_guestInformation_show', methods=['GET', 'POST'])
def waiter_customer_show():
    ans = session.query(Customer.Cid, Customer.Cname, Customer.Csex, Customer.Cnumber, Customer.Carid) \
        .all()
    return render_template("waiter_guestInformation_show.html", u=ans)


@app.route('/waiter_guestInformation_update', methods=['GET', 'POST'])
def waiter_customer_update():
    if request.method == 'GET':
        return render_template("waiter_guestInformation_update.html")
    else:
        if 'Gid' in request.form and not request.form['Gid'] == '':
            Cid = request.form['Gid']
            if not session.query(Customer).filter(Customer.Cid == Cid).first():
                return render_template("waiter_updateError.html")
            Cname = request.form['Gname'] if 'Gname' in request.form else None
            Csex = request.form['Gsex'] if 'Gsex' in request.form else None
            Cnumber = request.form['Gnum'] if 'Gnum' in request.form else None
            Carid = request.form['Cid'] if 'Cid' in request.form else None
            toUpdate = session.query(Customer).filter(Customer.Cid == Cid).first()
            if Cname != '':
                toUpdate.Cname = Cname
            if Csex != '':
                if not (Csex == '男' or Csex == '女'):
                    return render_template('waiter_error.html', u='请输入有效性别')
                toUpdate.Csex = Csex
            if Cnumber != '':
                if not (Cnumber.isdigit() and len(Cnumber) == 11):
                    return render_template('waiter_error.html', u='请输入有效的电话号码！')
                toUpdate.Cnumber = Cnumber
            if Carid != '':
                flag_1 = 1 if (len(Carid) == 8 and Carid[2] == '_') else 0
                flag_3 = 1 if Carid[0:2].isalpha() else 0
                flag_2 = 1 if Carid[3:8].isalnum() else 0
                if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
                    return render_template('waiter_error.html', u='车牌号格式不正确！')
                toUpdate.Carid = Carid
            toUpdate.update()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_parkingManage_delete', methods=['GET', 'POST'])
def waiter_park_delete():
    if request.method == 'GET':
        return render_template("waiter_parkingManage_delete.html")
    else:
        if 'Cid' in request.form and not request.form['Cid'] == '':
            Carid = request.form['Cid']
            if not session.query(ParkingManagement).filter(ParkingManagement.CARid == Carid).first():
                return render_template("waiter_deleteError.html")
            session.query(Car).filter(Car.CARid == Carid).delete()
            session.commit()  # Car delete
            carInPosition = session.query(ParkingManagement.CARposition).filter(ParkingManagement.CARid == Carid)
            carpos = carInPosition[0][0]
            session.query(ParkingLot).filter(ParkingLot.Pposition == carpos) \
                .update({ParkingLot.Pstatus: "空"}, synchronize_session=False)  # update parkinglot status
            session.query(ParkingManagement).filter(ParkingManagement.CARid == Carid).delete()
            session.commit()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_parkingManage_insert', methods=['GET', 'POST'])
def waiter_park_insert():
    if request.method == 'GET':
        return render_template("waiter_parkingManage_insert.html")
    else:
        if 'Cid' in request.form and 'Cpos' in request.form and 'Gnum' in request.form and 'Carcolor' in request.form \
                and not request.form['Cid'] == '' and not request.form['Cpos'] == ''\
                and not request.form['Gnum'] == '' and not request.form['Carcolor'] == '':
            Carid = request.form['Cid']
            if session.query(ParkingManagement).filter(ParkingManagement.CARid == Carid).first():
                return render_template("waiter_insertError.html")
            flag_1 = 1 if (len(Carid) == 8 and Carid[2] == '_') else 0
            flag_3 = 1 if Carid[0:2].isalpha() else 0
            flag_2 = 1 if Carid[3:8].isalnum() else 0
            if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
                return render_template('waiter_error.html', u='车牌号格式不正确！')
            Cpos = request.form['Cpos']
            if not session.query(ParkingLot).filter(ParkingLot.Pposition == Cpos).first():
                return render_template('waiter_error.html', u='请输入有效车位！')
            ans = session.query(ParkingLot).filter(ParkingLot.Pposition == Cpos).first()
            if ans.Pstatus == '已停':
                return render_template('waiter_error.html', u='此车位已停有车了！')
            Itime = currentTime() #request.form['Itime']
            # flag_3 = 1 if len(Itime) == 10 else 0
            # flag_2 = 1 if (Itime[0:4].isdigit() and Itime[5:7].isdigit() and Itime[8:10].isdigit()
            #                and 1 <= int(Itime[5:7]) <= 12 and 1 <= int(Itime[8:10]) <= 31) else 0
            # flag_1 = 1 if (Itime[4] == '.' and Itime[7] == '.') else 0
            # if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
            #     return render_template("waiter_error.html", u='请输入正确的停车时间！')
            Cnum = request.form['Gnum']
            if not (Cnum.isdigit() and len(Cnum) == 11):
                return render_template('waiter_error.html', u='请输入有效的电话号码！')
            Carcolor = request.form['Carcolor']
            parkManage = ParkingManagement(CARid=Carid, CARposition=Cpos, Itime=Itime, Cnumber=Cnum)
            parkManage.save()
            if not session.query(Car).filter(Car.CARid == Carid).first():
                car = Car(CARid=Carid, CARcolor=Carcolor)
                car.save()  # Car upload
            toUpdate = session.query(ParkingLot).filter(ParkingLot.Pposition == Cpos).first()
            toUpdate.Pstatus = '已停'
            toUpdate.update()  # parking lot inf
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_parkingManage_query', methods=['GET', 'POST'])
def waiter_park_query():
    if request.method == 'GET':
        return render_template("waiter_parkingManage_query.html")
    else:
        if 'Cid' in request.form and not request.form['Cid'] == '':
            Carid = request.form['Cid']
            ans = session \
                .query(ParkingManagement.CARid, ParkingManagement.CARposition, ParkingManagement.Itime,
                       ParkingManagement.Cnumber) \
                .filter(ParkingManagement.CARid == Carid).all()
            return render_template("waiter_parkingManage_result.html", u=ans)
        return render_template("waiter_emptyError.html")


@app.route('/waiter_parkingManage_show', methods=['GET', 'POST'])
def waiter_park_show():
    ans = session \
        .query(ParkingManagement.CARid, ParkingManagement.CARposition, ParkingManagement.Itime,
               ParkingManagement.Cnumber) \
        .all()
    return render_template("waiter_parkingManage_show.html", u=ans)


@app.route('/waiter_parkingManage_update', methods=['GET', 'POST'])
def waiter_park_update():
    if request.method == 'GET':
        return render_template("waiter_parkingManage_update.html")
    else:
        if 'Cid' in request.form and not request.form['Cid'] == '':
            Carid = request.form['Cid']
            if not session.query(ParkingManagement).filter(ParkingManagement.CARid == Carid).first():
                return render_template("waiter_updateError.html")
            Cpos = request.form['Cpos'] if 'Cpos' in request.form else None
            Itime = currentTime() #request.form['Itime'] if 'Itime' in request.form else None
            Cnum = request.form['Gnum'] if 'Gnum' in request.form else None
            toUpdate = session.query(ParkingManagement).filter(ParkingManagement.CARid == Carid).first()
            if Cpos != '':
                if not session.query(ParkingLot).filter(ParkingLot.Pposition == Cpos).first():
                    return render_template('waiter_error.html', u='请输入有效车位！')
                toUpdate.CARposition = Cpos
            # if Itime != '':
            #     flag_3 = 1 if len(Itime) == 10 else 0
            #     flag_2 = 1 if (Itime[0:4].isdigit() and Itime[5:7].isdigit() and Itime[8:10].isdigit()
            #                    and 1 <= int(Itime[5:7]) <= 12 and 1 <= int(Itime[8:10]) <= 31) else 0
            #     flag_1 = 1 if (Itime[4] == '.' and Itime[7] == '.') else 0
            #     if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
            #         return render_template("waiter_error.html", u='请输入正确的停车时间！')
            toUpdate.Itime = Itime
            if Cnum != '':
                if not (Cnum.isdigit() and len(Cnum) == 11):
                    return render_template('waiter_error.html', u='请输入有效的电话号码！')
                toUpdate.Cnumber = Cnum
            toUpdate.update()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_parkingStatus_delete', methods=['GET', 'POST'])
def waiter_lot_delete():
    if request.method == 'GET':
        return render_template("waiter_parkingStatus_delete.html")
    else:
        if 'Gid' in request.form and not request.form['Gid'] == '':
            Cpos = request.form['Gid']
            if not session.query(ParkingLot).filter(ParkingLot.Pposition == Cpos).frist():
                return render_template("waiter_deleteError.html")
            session.query(ParkingLot).filter(ParkingLot.Pposition == Cpos).delete()
            session.commit()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_parkingStatus_insert', methods=['GET', 'POST'])
def waiter_lot_insert():
    if request.method == 'GET':
        return render_template("waiter_parkingStatus_insert.html")
    else:
        if 'Cpos' in request.form and 'Cstat' in request.form \
                and not request.form['Cpos'] == '' and not request.form['Cstat'] == '':
            Cpos = request.form['Cpos']
            if session.query(ParkingLot).filter(ParkingLot.Pposition == Cpos).first():
                return render_template("waiter_insertError.html")
            if not Cpos.isdigit():
                return render_template('waiter_error.html', u='车位号为数字！')
            Cstatus = request.form['Cstat']
            if not (Cstatus == '空' or Cstatus == '已停'):
                return render_template('waiter_error.html', u='请输入规范的车位状态！')
            lot = ParkingLot(Pposition=Cpos, Pstatus=Cstatus)
            lot.save()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_parkingStatus_update', methods=['GET', 'POST'])
def waiter_lot_update():
    if request.method == 'GET':
        return render_template("waiter_parkingStatus_update.html")
    else:
        if 'Cpos' in request.form and not request.form['Cpos'] == '':
            Cpos = request.form['Cpos']
            if not session.query(ParkingLot).filter(ParkingLot.Pposition == Cpos).first():
                return render_template("waiter_updateError.html")
            Cstatus = request.form['Cstat'] if 'Cstat' in request.form else None
            toUpdate = session.query(ParkingLot).filter(ParkingLot.Pposition == Cpos).first()
            if Cstatus != '':
                if not (Cstatus == '空' or Cstatus == '已停'):
                    return render_template('waiter_error.html', u='请输入规范的车位状态！')
                toUpdate.Pstatus = Cstatus
            toUpdate.update()
            return render_template("waiter_index.html")
        return render_template("waiter_emptyError.html")


@app.route('/waiter_parkingStatus_show', methods=['GET', 'POST'])
def waiter_lot_show():
    ans = session.query(ParkingLot.Pposition, ParkingLot.Pstatus).all()
    return render_template("waiter_parkingStatus_show.html", u=ans)


@app.route('/manager_room_show', methods=['GET', 'POST'])
def manager_room_show():
    ans = session.query(Room.Rno, Room.Rstorey, Room.Rstatus, Room.Rcode).all()
    return render_template("manager_room_show.html", u=ans)


@app.route('/manager_room_insert', methods=['GET', 'POST'])
def manager_room_insert():
    if request.method == 'GET':
        return render_template("manager_room_insert.html")
    else:
        if 'Rno' in request.form and 'Rstorey' in request.form and 'Rstatus' in request.form and 'Rcode' in request.form \
                and not request.form['Rno'] == '' and not request.form['Rstorey'] == '' and not request.form[
                                                                                                    'Rstatus'] == '' \
                and not request.form['Rcode'] == '':
            Rno = request.form['Rno']
            if session.query(Room).filter(Room.Rno == Rno).first():
                return render_template("manager_insertError.html")
            if not (Rno.isdigit() and 101 <= int(Rno) <= 908):
                return render_template("manager_error.html", u='房间号格式有误！')
            storey_accord = int(int(Rno) / 100)
            # print(storey_accord)
            Rstorey = request.form['Rstorey']
            Rstatus = request.form['Rstatus']
            Rcode = request.form['Rcode']
            if not (Rstorey.isdigit() and int(Rstorey) == storey_accord):
                return render_template("manager_error.html", u='输入楼层应与房间号首数字对应！')
            if not (Rstatus == '空' or Rstatus == '已住'):
                return render_template("manager_error.html", u='房间状态输入不规范！')
            if not (Rcode == 'A1' or Rcode == 'A2' or Rcode == 'B1' or Rcode == 'B2'):
                return render_template("manager_error.html", u='没有这样的房间代号！')
            new_room = Room(Rno=Rno, Rcode=Rcode, Rstatus=Rstatus, Rstorey=Rstorey)
            new_room.save()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_room_delete', methods=['GET', 'POST'])
def manager_room_delete():
    if request.method == 'GET':
        return render_template("manager_room_delete.html")
    else:
        if 'Rno' in request.form and not request.form['Rno'] == '':
            Rno = request.form['Rno']
            if not session.query(Room).filter(Room.Rno == Rno).first():
                return render_template("manager_deleteError.html")
            session.query(Room).filter(Room.Rno == Rno).delete()
            session.commit()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_codeInf_show', methods=['GET', 'POST'])
def manager_codeInf_show():
    ans = session.query(CodeInf.Rcode, CodeInf.Rtype, CodeInf.Rscale, CodeInf.Rprice, CodeInf.Mno).all()
    return render_template("manager_codeInf_show.html", u=ans)


@app.route('/manager_codeInf_update', methods=['GET', 'POST'])
def manager_codeInf_update():
    if request.method == 'GET':
        return render_template("manager_codeInf_update.html")
    else:
        if 'Rcode' in request.form and not request.form['Rcode'] == '':
            Rcode = request.form['Rcode']
            if not session.query(CodeInf).filter(CodeInf.Rcode == Rcode).first():
                return render_template("manager_updateError.html")
            Rprice = request.form['Rprice'] if 'Rprice' in request.form else None
            if not (Rprice.isdigit() and int(Rprice) >= 0):
                return render_template('manager_error.html', u='请输入正确的房价!!')
            # Mno = request.form['Mno']
            toUpdate = session.query(CodeInf).filter(CodeInf.Rcode == Rcode).first()
            if Rprice != '':
                toUpdate.Rprice = Rprice
            toUpdate.Mno = MAno
            toUpdate.update()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_customer_show', methods=['GET', 'POST'])
def manager_customer_show():
    ans = session.query(Customer.Cid, Customer.Cname, Customer.Csex, Customer.Cnumber, Customer.Carid).all()
    return render_template("manager_customer_show.html", u=ans)


@app.route('/manager_receptionist_show', methods=['GET', 'POST'])
def manager_receptionist_show():
    ans = session.query(Receptionist.RECPno, Receptionist.RECPname, Receptionist.RECPsalary, Receptionist.Mno).all()
    return render_template('manager_receptionist_show.html', u=ans)


@app.route('/manager_receptionist_update', methods=['GET', 'POST'])
def manager_receptionist_update():
    if request.method == 'GET':
        return render_template("manager_receptionist_update.html")
    else:
        if 'RECPno' in request.form and not request.form['RECPno'] == '':
            RECPno = request.form['RECPno']
            if not session.query(Receptionist).filter(Receptionist.RECPno == RECPno).first():
                return render_template("manager_updateError.html")
            RECPsalary = request.form['RECPsalary'] if 'RECPsalary' in request.form else None
            if not (RECPsalary.isdigit() and int(RECPsalary) >= 2000):
                return render_template('manager_error.html', u='请输入正确且合理的工资!!')
            toUpdate = session.query(Receptionist).filter(Receptionist.RECPno == RECPno).first()
            if RECPsalary != '':
                toUpdate.RECPsalary = RECPsalary
            toUpdate.Mno = MAno
            toUpdate.update()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_receptionist_insert', methods=['GET', 'POST'])
def manager_receptionist_insert():
    if request.method == 'GET':
        return render_template("manager_receptionist_insert.html")
    else:
        if 'RECPno' in request.form and 'RECPname' in request.form and 'RECPsalary' in request.form and \
                'RECPpass' in request.form and not request.form['RECPno'] == '' \
                and not request.form['RECPname'] == '' and not request.form['RECPsalary'] == '' \
                and not request.form['RECPpass'] == '':
            RECPno = request.form['RECPno']
            if session.query(Receptionist).filter(Receptionist.RECPno == RECPno).first():
                return render_template("manager_insertError.html")
            if session.query(WorkHistory).filter(WorkHistory.Eno == RECPno).first():
                return render_template("manager_error.html", u='与历史职员的工号也不应重复！')
            flag_1 = 1 if len(RECPno) == 4 else 0
            flag_2 = 1 if RECPno[0] == 'R' else 0
            flag_3 = 1 if RECPno[1:4].isdigit() else 0
            if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
                return render_template("manager_error.html", u='请输入正确的前台工号！')
            RECPname = request.form['RECPname']
            RECPsalary = request.form['RECPsalary']
            if not (RECPsalary.isdigit() and int(RECPsalary) >= 2000):
                return render_template('manager_error.html', u='请输入正确且合理的工资!!')
            Mno = MAno
            Etype = 'R'
            Etime = currentTime() #request.form['Etime']
            # flag_3 = 1 if len(Etime) == 10 else 0
            # flag_2 = 1 if (Etime[0:4].isdigit() and Etime[5:7].isdigit() and Etime[8:10].isdigit()
            #                and 1 <= int(Etime[5:7]) <= 12 and 1 <= int(Etime[8:10]) <= 31) else 0
            # flag_1 = 1 if (Etime[4] == '.' and Etime[7] == '.') else 0
            # if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
            #     return render_template("manager_error.html", u='请输入正确的入职时间！')
            RECPpass = request.form['RECPpass']
            recp = Receptionist(RECPno=RECPno, RECPname=RECPname, RECPsalary=RECPsalary, Mno=Mno, RECPpass=RECPpass)
            recp.save()
            workhistory = WorkHistory(Ename=RECPname, Eno=RECPno, Etype=Etype, Etime=Etime, Qtime='仍在职')
            workhistory.save()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_receptionist_delete', methods=['GET', 'POST'])
def manager_receptionist_delete():
    if request.method == 'GET':
        return render_template("manager_receptionist_delete.html")
    else:
        if 'RECPno' in request.form and not request.form['RECPno'] == '' :
                #and not request.form['Qtime'] == '':
            RECPno = request.form['RECPno']
            if not session.query(Receptionist).filter(Receptionist.RECPno == RECPno).first():
                return render_template("manager_deleteError.html")
            Qtime = currentTime()#request.form['Qtime']
            # flag_3 = 1 if len(Qtime) == 10 else 0
            # flag_2 = 1 if (Qtime[0:4].isdigit() and Qtime[5:7].isdigit() and Qtime[8:10].isdigit()
            #                and 1 <= int(Qtime[5:7]) <= 12 and 1 <= int(Qtime[8:10]) <= 31) else 0
            # flag_1 = 1 if (Qtime[4] == '.' and Qtime[7] == '.') else 0
            # if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
            #     return render_template("manager_error.html", u='请输入正确的离职时间！')
            session.query(Receptionist).filter(Receptionist.RECPno == RECPno).delete()
            session.commit()
            toUpdate = session.query(WorkHistory).filter(WorkHistory.Eno == RECPno).first()
            toUpdate.Qtime = Qtime
            toUpdate.update()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_waiter_show', methods=['GET', 'POST'])
def manager_waiter_show():
    ans = session.query(Waiter.Wno, Waiter.Wname, Waiter.Wsalary, Waiter.Mno).all()
    return render_template('manager_waiter_show.html', u=ans)


@app.route('/manager_waiter_update', methods=['GET', 'POST'])
def manager_waiter_update():
    if request.method == 'GET':
        return render_template("manager_waiter_update.html")
    else:
        if 'Wno' in request.form and not request.form['Wno'] == '':
            Wno = request.form['Wno']
            if not session.query(Waiter).filter(Waiter.Wno == Wno).first():
                return render_template("manager_updateError.html")
            Wsalary = request.form['Wsalary'] if 'Wsalary' in request.form else None
            if not (Wsalary.isdigit() and int(Wsalary) >= 2000):
                return render_template('manager_error.html', u='请输入正确且合理的工资!!')
            toUpdate = session.query(Waiter).filter(Waiter.Wno == Wno).first()
            if Wsalary != '':
                toUpdate.Wsalary = Wsalary
            toUpdate.Mno = MAno
            toUpdate.update()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_waiter_insert', methods=['GET', 'POST'])
def manager_waiter_insert():
    if request.method == 'GET':
        return render_template("manager_waiter_insert.html")
    else:
        if 'Wno' in request.form and 'Wname' in request.form and 'Wsalary' in request.form \
                and not request.form['Wno'] == '' and not request.form['Wname'] == '' \
                and not request.form['Wsalary'] == '':
            Wno = request.form['Wno']
            if session.query(Waiter).filter(Waiter.Wno == Wno).first():
                return render_template("manager_insertError.html")
            if session.query(WorkHistory).filter(WorkHistory.Eno == Wno).first():
                return render_template("manager_error.html", u='与历史职员的工号也不应重复！')
            flag_1 = 1 if len(Wno) == 4 else 0
            flag_2 = 1 if Wno[0] == 'W' else 0
            flag_3 = 1 if Wno[1:4].isdigit() else 0
            if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
                return render_template("manager_error.html", u='请输入正确的服务人员工号！')
            Wname = request.form['Wname']
            Wsalary = request.form['Wsalary']
            if not (Wsalary.isdigit() and int(Wsalary) >= 2000):
                return render_template('manager_error.html', u='请输入正确且合理的工资!!')
            Etype = 'W'
            Etime = currentTime()#request.form['Etime']
            # flag_3 = 1 if len(Etime) == 10 else 0
            # flag_2 = 1 if (Etime[0:4].isdigit() and Etime[5:7].isdigit() and Etime[8:10].isdigit()
            #                and 1 <= int(Etime[5:7]) <= 12 and 1 <= int(Etime[8:10]) <= 31) else 0
            # flag_1 = 1 if (Etime[4] == '.' and Etime[7] == '.') else 0
            # if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
            #     return render_template("manager_error.html", u='请输入正确的入职时间！')
            waiter = Waiter(Wno=Wno, Wname=Wname, Wsalary=Wsalary, Mno=MAno)
            waiter.save()
            workhistory = WorkHistory(Ename=Wname, Eno=Wno, Etype=Etype, Etime=Etime, Qtime='仍在职')
            workhistory.save()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_waiter_delete', methods=['GET', 'POST'])
def manager_waiter_delete():
    if request.method == 'GET':
        return render_template("manager_waiter_delete.html")
    else:
        if 'Wno' in request.form and not request.form['Wno'] == '':# and not request.form['Qtime'] == '':
            Wno = request.form['Wno']
            if not session.query(Waiter).filter(Waiter.Wno == Wno).first():
                return render_template("manager_deleteError.html")
            Qtime = currentTime()#request.form['Qtime']
            # flag_3 = 1 if len(Qtime) == 10 else 0
            # flag_2 = 1 if (Qtime[0:4].isdigit() and Qtime[5:7].isdigit() and Qtime[8:10].isdigit()
            #                and 1 <= int(Qtime[5:7]) <= 12 and 1 <= int(Qtime[8:10]) <= 31) else 0
            # flag_1 = 1 if (Qtime[4] == '.' and Qtime[7] == '.') else 0
            # if flag_3 == 0 or flag_2 == 0 or flag_1 == 0:
            #     return render_template("manager_error.html", u='请输入正确的离职时间！')
            session.query(Waiter).filter(Waiter.Wno == Wno).delete()
            session.commit()
            toUpdate = session.query(WorkHistory).filter(WorkHistory.Eno == Wno).first()
            toUpdate.Qtime = Qtime
            toUpdate.update()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_employeeRoom_insert', methods=['GET', 'POST'])
def manager_er_insert():
    if request.method == 'GET':
        return render_template("manager_employeeRoom_insert.html")
    else:
        if 'Rno' in request.form and 'Wno' in request.form and 'RECPno' in request.form \
                and not request.form['Rno'] == '' and not request.form['Wno'] == '' \
                and not request.form['RECPno'] == '':
            Rno = request.form['Rno']
            if not session.query(Room).filter(Room.Rno == Rno).first():
                return render_template("manager_error.html", u='此房号不存在！')
            if session.query(EmployeeRoom).filter(EmployeeRoom.Rno == Rno).first():
                return render_template("manager_error.html", u='此房已有安排！')
            Wno = request.form['Wno']
            if not session.query(Waiter).filter(Waiter.Wno == Wno).first():
                return render_template("manager_error.html", u='此服务人员不存在')
            RECPno = request.form['RECPno']
            if not session.query(Receptionist).filter(Receptionist.RECPno == RECPno).first():
                return render_template("manager_error.html", u='此前台人员不存在')
            er = EmployeeRoom(Rno=Rno, Wno=Wno, RECPno=RECPno)
            er.save()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_employeeRoom_delete', methods=['GET', 'POST'])
def manager_er_delete():
    if request.method == 'GET':
        return render_template("manager_employeeRoom_delete.html")
    else:
        if 'Rno' in request.form and not request.form['Rno'] == '':
            Rno = request.form['Rno']
            if not session.query(EmployeeRoom).filter(EmployeeRoom.Rno == Rno).first():
                return render_template("manager_deleteError.html")
            session.query(EmployeeRoom).filter(EmployeeRoom.Rno == Rno).delete()
            session.commit()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_employeeRoom_update', methods=['GET', 'POST'])
def manager_er_update():
    if request.method == 'GET':
        return render_template("manager_employeeRoom_update.html")
    else:
        if 'Rno' in request.form and not request.form['Rno'] == '':
            Rno = request.form['Rno']
            if not session.query(EmployeeRoom).filter(EmployeeRoom.Rno == Rno).first():
                return render_template("manager_updateError.html")
            Wno = request.form['Wno'] if 'Wno' in request.form else None
            RECPno = request.form['RECPno'] if 'RECPno' in request.form else None
            toUpdate = session.query(EmployeeRoom).filter(EmployeeRoom.Rno == Rno).first()
            if Wno != '':
                if not session.query(Waiter).filter(Waiter.Wno == Wno).first():
                    return render_template("manager_error.html", u='此服务人员不存在')
                toUpdate.Wno = Wno
            if RECPno != '':
                if not session.query(Receptionist).filter(Receptionist.RECPno == RECPno).first():
                    return render_template("manager_error.html", u='此前台人员不存在')
                toUpdate.RECPno = RECPno
            toUpdate.update()
            return render_template("manager_index.html")
        return render_template("manager_emptyError.html")


@app.route('/manager_employeeRoom_show', methods=['GET', 'POST'])
def manager_er_show():
    ans = session.query(EmployeeRoom.Rno, EmployeeRoom.Wno, EmployeeRoom.RECPno).all()
    # session.commit()
    return render_template("manager_employeeRoom_show.html", u=ans)


@app.route('/manager_workHistory_show', methods=['GET', 'POST'])
def manager_wh_show():
    ans = session.query(WorkHistory.Ename, WorkHistory.Eno, WorkHistory.Etype, WorkHistory.Etime,
                        WorkHistory.Qtime).all()
    return render_template("manager_workHistory_show.html", u=ans)


if __name__ == '__main__':
    # 创建数据表
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    runTriggers()
    app.run(debug=True)
