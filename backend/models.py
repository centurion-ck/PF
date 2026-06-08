from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String

class Base(DeclarativeBase):
    pass


class Request(Base):

    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)

    request_id = Column(String)

    resource_type = Column(String)

    resource_name = Column(String)

    status = Column(String)

    iac_tool = Column(String)

    environment = Column(String)

