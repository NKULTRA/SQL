from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__= 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nothing to do!')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

menu = (
    "1) Today's tasks\n"
    "2) Week's tasks\n"
    "3) All tasks\n"
    "4) Missed tasks\n"
    "5) Add task\n"
    "6) Delete task\n"
    "0) Exit"
)

week = {
    0 : "Monday",
    1 : "Tuesday",
    2 : "Wednesday",
    3 : "Thursday",
    4 : "Friday",
    5 : "Saturday",
    6 : "Sunday"
}


def today():
    today = datetime.today().date()
    row = session.query(Table).filter(Table.deadline == today).all()
    if len(row) == 0:
        print("Today", today.day, today.strftime('%b'))
        print("Nothing to do!")
        print()
    else:
        for element in row:
            print(element.task)
    print()


def weeklong():
    today = datetime.today().date()
    for i in range(7):
        row = session.query(Table).filter(Table.deadline == (today + timedelta(days=i))).all()
        print(
            week[(today + timedelta(days=i)).weekday()],
            (today + timedelta(days=i)).day,
            (today + timedelta(days=i)).strftime('%b')
        )
        if len(row) == 0:
            print("Nothing to do!")
        else:
            for i in range(len(row)):
                print(f"{i + 1}. " + row[i].task)
        print()


def alltask():
    row = session.query(Table).all()
    if len(row) == 0:
        print("Nothing to do!")
    else:
        for i in range(len(row)):
            print(f"{i + 1}. " + row[i].task)
    print()


def addtask():
    new_act = input("Enter activity")
    new_dead = input("Enter deadline")
    print("The task has been added!")
    print()
    new_row = Table(
        task=new_act,
        deadline=datetime.strptime(new_dead, '%Y-%m-%d').date()
    )
    session.add(new_row)
    session.commit()


def missed():
    today = datetime.today().date()
    row = session.query(Table).filter(Table.deadline < today).all()
    if len(row) == 0:
        print("Nothing is missed!")
    else:
        for i in range(len(row)):
            print(f"{i + 1}. " + row[i].task)
    print()


def delete():
    row = session.query(Table).order_by(Table.deadline).all()
    print("Choose the number of the task you want to delete:")
    if len(row) == 0:
        print("Nothing to delete!")
    else:
        for i in range(len(row)):
            print(f"{i + 1}. " + row[i].task)
    inp = int(input())
    session.delete(row[inp - 1])
    session.commit()
    print("The task has been deleted!")
    print()

# start menu
while True:
    print(menu)
    inp = input()
    print()

    if inp == "1":
        today()
    elif inp == "2":
        weeklong()
    elif inp == "3":
        alltask()
    elif inp == "4":
        missed()
    elif inp == "5":
        addtask()
    elif inp == "6":
        delete()
    elif inp == "0":
        print("Bye!")
        break
