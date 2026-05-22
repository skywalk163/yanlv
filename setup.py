"""
言律语言 - Python包配置

一个中文编程语言的词法分析器和编译器
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') if (this_directory / "README.md").exists() else ""

# 读取requirements
requirements = []
if (this_directory / "requirements.txt").exists():
    with open(this_directory / "requirements.txt", encoding='utf-8') as f:
        requirements = [
            line.strip() for line in f
            if line.strip() and not line.startswith('#') and not line.startswith('pytest') and not line.startswith('flake8') and not line.startswith('black') and not line.startswith('mypy') and not line.startswith('sphinx') and not line.startswith('memory-profiler') and not line.startswith('line-profiler')
        ]

setup(
    name='yanlv',
    version='2.0.0',
    author='言律语言项目组',
    author_email='yanlv@example.com',
    description='言律语言 - 中文编程语言的词法分析器和编译器',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yanlv/yanlv',
    project_urls={
        'Bug Tracker': 'https://github.com/yanlv/yanlv/issues',
        'Documentation': 'https://yanlv.readthedocs.io',
        'Source Code': 'https://github.com/yanlv/yanlv',
    },
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
    ],
    python_requires='>=3.8',
    install_requires=[
        'jieba>=0.42.1',
        'typing-extensions>=4.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'flake8>=6.0.0',
            'black>=23.0.0',
            'mypy>=1.0.0',
        ],
        'docs': [
            'sphinx>=5.0.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
        'thulac': [
            'thulac>=0.2.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'yanlv=yanlv.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        'chinese-programming-language',
        'compiler',
        'lexer',
        'parser',
        'semantic-analysis',
        'natural-language-processing',
        'nlp',
    ],
)