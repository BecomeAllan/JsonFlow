from setuptools import setup, find_packages

# Lendo as dependências do arquivo requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Lendo o conteúdo do README.md para a descrição longa
with open('src/README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='JsonFlow',
    version='0.1.1.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    author='BecomeAllan',
    author_email='becomeallan@gmail.com',
    install_requires=requirements,
    extras_require={
        'parse': ['pandoc', 'beautifulsoup4']
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='json, dictionary, manipulation, traversal, nested, extraction, configuration, API, data storage, python, JsonFlow',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
