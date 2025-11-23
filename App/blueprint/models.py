from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List
from datetime import date
from flask_sqlalchemy import SQLAlchemy


#create a base class for our models
class Base(DeclarativeBase): #all sql method will inherit from the base
    pass

#Instantiate your sqlalchemy database
db = SQLAlchemy(model_class = Base)

class Member(Base):
    __tablename__ = 'members' #will most likely be initialized as a member table in the database

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    DOB: Mapped[date] = mapped_column(db.Date, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    #loan:Mapped['Loan'] = db.relationship(back_populates='member')
    member_loans: Mapped[List['Loan']] = db.relationship(back_populates='member') #relationship between member and loan

#this is a many to many relationship
loan_book = db.Table(
    'loan_book',
    Base.metadata,
    db.Column('loan_id', db.ForeignKey('loans.id')),
    db.Column('book_id', db.ForeignKey('books.id'))
)

class Loan(Base):
    __tablename__ = 'loans' #will most likely be initialized as a "loans" table in the database

    id: Mapped[int] = mapped_column(primary_key=True)
    loan_date: Mapped[date] = mapped_column(db.Date)
    member_id: Mapped[int] = mapped_column(db.ForeignKey('members.id'))
    member: Mapped['Member'] = db.relationship(back_populates='member_loans') #relationship between member and loan
    books: Mapped[List['Book']] = db.relationship(secondary=loan_book, back_populates='book_loans')

class Book(Base):
    __tablename__ = "books" #will most likely be initialized as a "books" table in the database

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(db.String(255), nullable=False)
    genre: Mapped[str] = mapped_column(db.String(255), nullable=False)
    desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    book_loans: Mapped[List['Loan']] = db.relationship(secondary=loan_book, back_populates='books')
