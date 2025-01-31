from langchain.tools import tool
from services.document_store import DocumentStore
from typing import List


@tool
def get_all_brs() -> List[str]:
    """
    Retrieves all business requirements (BRs) from document storage for AI agent operations

    Interface:
        Inputs: None
        Outputs: List of BR document filenames

    Key Features:
        - Direct integration with DocumentStore service
        - Returns original filenames for traceability
        - Compatible with LangChain tool ecosystem

    Usage:
        When an AI agent needs to:
        1. Validate requirements coverage
        2. Cross-reference features with BRs
        3. Generate requirement-based content

    Example Agent Usage:
        br_list = get_all_brs()
        for br in br_list:
            analyze_requirement(br)

    Returns:
        List[str]: BR filenames in format 'BR_<feature>_<version>.<ext>'

    Note:
        Requires DocumentStore service initialization
    """
    # Log agent tool activation
    print(f'[BR Agent] Fetching all business requirements')

    # Access document storage service
    document_embedder = DocumentStore()
    return [doc.original_filename for doc in document_embedder.get_all_documents()]