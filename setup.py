from setuptools import setup, find_packages

setup(
    name="data_ingestion_supabase",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "supabase",
        "pytest",
        "python-dotenv"
    ],
)