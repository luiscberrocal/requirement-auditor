from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

from requirement_auditor.settings import DB_FILE

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    requirements = relationship(
        "Requirement", back_populates="project", cascade="all, delete, delete-orphan"
    )


class Requirement(Base):
    __tablename__ = "requirements"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specs = Column(String, nullable=False)
    version = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="requirements")


def get_database(db_filename=None):
    if db_filename is None:
        db_filename = DB_FILE
    engine = create_engine(f"sqlite:///{db_filename}", echo=True)
    Base.metadata.create_all(engine)
    LocalSession = sessionmaker(bind=engine)
    db: Session = LocalSession()
    return db


