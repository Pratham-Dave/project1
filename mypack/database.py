import os 
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

if os.getenv("DATABASE_URL") == None:
    dbConnection = "postgres://neirzwjdfklgwv:06ddc2eb1be9201f1324c6779bb86b764d2fb843df91d38af3c9d1da4df25459@ec2-54-81-37-115.compute-1.amazonaws.com:5432/d4gljnrpedu0op"
else:
    dbConnection = os.getenv("DATABASE_URL")

engine = create_engine(dbConnection)
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("books.csv")
    reader = csv.reader(f)

    for isbn,title,author,year in reader:
        db.execute("INSERT INTO books(isbn,title,author,year) VALUES(:isbn,:title,:author,:year)",{"isbn": isbn,"title":title,"author":author,"year":year})
        print(f"Adding book with isbn number{isbn}")
    db.commit()


if __name__ == "__main__":
    main()