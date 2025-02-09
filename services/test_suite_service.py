from typing import Dict, List
from domain.test_suite import TestSuite
from domain.models.test_suite import TestSuite as DBTestSuite, UserCase as DBUserCase, TestCase as DBTestCase, TestStep as DBTestStep
from config.database import db


class TestSuiteService:
    @staticmethod
    def save_test_suite(test_data: TestSuite) -> tuple[DBTestSuite, Dict[str, int]]:
        """
        Сохраняет тестовый набор в базу данных.
        
        Args:
            test_data: Словарь с данными тестового набора
            
        Returns:
            Tuple[DBTestSuite, Dict[str, int]]: Созданный тестовый набор и статистика
        """
        with next(db.get_db()) as session:
            # Create TestSuite
            db_test_suite = DBTestSuite()
            session.add(db_test_suite)
            session.flush()
            
            # Create UserCases
            for uc in test_data['user_cases']:
                db_user_case = DBUserCase(
                    case_id=uc['id'],
                    title=uc['title'],
                    description=uc['description'],
                    test_suite_id=db_test_suite.id
                )
                session.add(db_user_case)
                session.flush()
                
                # Create TestCases
                for tc in uc['test_cases']:
                    db_test_case = DBTestCase(
                        case_id=tc['id'],
                        title=tc['title'],
                        description=tc['description'],
                        expected_outcome=tc['expected_outcome'],
                        user_case_id=db_user_case.id
                    )
                    session.add(db_test_case)
                    session.flush()
                    
                    # Create TestSteps
                    for step in tc['steps']:
                        db_test_step = DBTestStep(
                            step_number=step['step_number'],
                            description=step['description'],
                            expected_result=step['expected_result'],
                            test_case_id=db_test_case.id
                        )
                        session.add(db_test_step)
            
            session.commit()
            
            stats = {
                'user_cases_count': len(test_data['user_cases']),
                'test_cases_count': sum(len(uc['test_cases']) for uc in test_data['user_cases'])
            }
            
            return db_test_suite, stats
