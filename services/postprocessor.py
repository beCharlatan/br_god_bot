import json
from pathlib import Path
from datetime import datetime
from domain.models import TestSuite

class Postprocessor:
    def generate_output_path(self, input_file: str) -> str:
        """Generate output filename based on input filename."""
        input_path = Path(input_file)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return str(input_path.parent / f"test_cases_{timestamp}.json")

    def save_test_cases(self, test_suite: TestSuite, output_path: str):
        """Save test cases to a JSON file."""
        output = test_suite.dict()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
