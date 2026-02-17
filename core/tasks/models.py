from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from core.database import Base


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default='pending')
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"