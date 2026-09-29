import importlib.metadata

packages = ["chromadb", "langchain", "langchain-community", "langchain-chroma", "langchain-huggingface"]

with open("versions.txt", "w") as f:
    for pkg in packages:
        try:
            version = importlib.metadata.version(pkg)
            f.write(f"{pkg}=={version}\n")
        except importlib.metadata.PackageNotFoundError:
            f.write(f"{pkg} is not installed\n")
