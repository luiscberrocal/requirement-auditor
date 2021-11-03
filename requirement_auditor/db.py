from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

from requirement_auditor.settings import DB_FILE

Base = declarative_base()

engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)


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


def main():
    Base.metadata.create_all(engine)
    LocalSession = sessionmaker(bind=engine)
    db: Session = LocalSession()

    project = Project(name='cool-project')
    requirement_list = list()
    requirement_list.append(Requirement(name='Django', specs='==', version='3.2.9'))
    requirement_list.append(Requirement(name='django-test-tools', specs='==', version='2.0.0'))
    project.requirements = requirement_list
    db.add(project)
    db.commit()


if __name__ == '__main__':
    main()