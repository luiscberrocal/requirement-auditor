from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

Base = declarative_base()

engine = create_engine("sqlite://", echo=True)


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
    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="requirements")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    LocalSession = sessionmaker(bind=engine)
    db: Session = LocalSession()

    project = Project(name='cool-project')
    db.add(project)
    db.commit()
