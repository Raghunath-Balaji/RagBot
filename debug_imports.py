import sys
import langchain

print(f"Python version: {sys.version}")
print(f"Langchain version: {langchain.__version__}")

try:
    from langchain.retrievers import ContextualCompressionRetriever
    print("SUCCESS: from langchain.retrievers import ContextualCompressionRetriever")
except ImportError as e:
    print(f"FAIL: from langchain.retrievers - {e}")

try:
    from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
    print("SUCCESS: from langchain.retrievers.contextual_compression import ContextualCompressionRetriever")
except ImportError as e:
    print(f"FAIL: from langchain.retrievers.contextual_compression - {e}")

try:
    from langchain_core.retrievers import ContextualCompressionRetriever
    print("SUCCESS: from langchain_core.retrievers import ContextualCompressionRetriever")
except ImportError as e:
    print(f"FAIL: from langchain_core.retrievers - {e}")

# List all attributes in langchain.retrievers if it exists
try:
    import langchain.retrievers
    print("\nAttributes in langchain.retrievers:")
    print([attr for attr in dir(langchain.retrievers) if not attr.startswith('_')])
except ImportError:
    print("\nlangchain.retrievers module not found at all.")
