from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from config.database import Base


class TestStep(Base):
    __tablename__ = 'test_steps'
    
    id = Column(Integer, primary_key=True)
    step_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    expected_result = Column(Text, nullable=False)
    test_case_id = Column(Integer, ForeignKey('test_cases.id'), nullable=False)
    
    test_case = relationship("TestCase", back_populates="steps")


class TestCase(Base):
    __tablename__ = 'test_cases'
    
    id = Column(Integer, primary_key=True)
    case_id = Column(String(10), nullable=False, unique=True)  # TC###
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    expected_outcome = Column(Text, nullable=False)
    user_case_id = Column(Integer, ForeignKey('user_cases.id'), nullable=False)
    file_embeddings_id = Column(Integer, ForeignKey('file_embeddings.id'), nullable=True)
    
    steps = relationship("TestStep", back_populates="test_case", cascade="all, delete-orphan")
    user_case = relationship("UserCase", back_populates="test_cases")
    file_embeddings = relationship("FileEmbeddings")


class UserCase(Base):
    __tablename__ = 'user_cases'
    
    id = Column(Integer, primary_key=True)
    case_id = Column(String(10), nullable=False, unique=True)  # UC###
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    test_suite_id = Column(Integer, ForeignKey('test_suites.id'), nullable=False)
    file_embeddings_id = Column(Integer, ForeignKey('file_embeddings.id'), nullable=True)
    
    test_cases = relationship("TestCase", back_populates="user_case", cascade="all, delete-orphan")
    test_suite = relationship("TestSuite", back_populates="user_cases")
    file_embeddings = relationship("FileEmbeddings")


class TestSuite(Base):
    __tablename__ = 'test_suites'
    
    id = Column(Integer, primary_key=True)
    file_embeddings_id = Column(Integer, ForeignKey('file_embeddings.id'), nullable=True)
    
    user_cases = relationship("UserCase", back_populates="test_suite", cascade="all, delete-orphan")
    file_embeddings = relationship("FileEmbeddings")
