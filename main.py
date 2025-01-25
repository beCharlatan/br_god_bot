from services import Preprocessor, Postprocessor, RequirementsAnalyzer

def main():
    preprocessor = Preprocessor()
    analyzer = RequirementsAnalyzer()
    postprocessor = Postprocessor()
    
    args = preprocessor.parse_arguments()
    content = preprocessor.read_requirements_file(args.input_file)
    
    test_suite = analyzer.analyze_requirements(content)
    
    output_path = postprocessor.generate_output_path(args.input_file)
    postprocessor.save_test_cases(test_suite, output_path)

if __name__ == "__main__":
    main()
