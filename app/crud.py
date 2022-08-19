from sqlalchemy.orm import Session

from . import models

def get_salary(db: Session):
    return db.query(models.salary.player, models.salary.positions, models.salary.team, models.salary.salary).all()

def get_Project(db: Session):
    return db.query(models.Project.state, models.Project.total, models.Project.hom, models.Project.sui, models.Project.ranks).all()
