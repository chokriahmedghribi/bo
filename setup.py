from setuptools import setup, find_packages

setup(
    name="bureau-ordre",
    version="1.0.0",
    description="نظام إدارة مكتب الظبط",
    author="Chokri Ahmed Ghribi",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "sqlalchemy>=2.0.23",
        "streamlit-option-menu>=0.3.6",
        "python-docx>=1.1.0",
        "pandas>=2.1.3",
        "openpyxl>=3.1.2",
        "python-dateutil>=2.8.2",
    ],
)