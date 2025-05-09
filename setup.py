from setuptools import setup, find_packages
import os

def get_version():
    init_path = os.path.join(os.path.dirname(__file__), 'browlite', '__init__.py')
    with open(init_path, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"\'')

setup(
    name='browlite',
    version=get_version(),
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.4',
        'PyQtWebEngine>=5.15.5',
    ],
    entry_points={
        'console_scripts': [
            'browlite=browlite.main:main',
        ],
    },
    package_data={
        'browlite': [
            'resources/styles/*.css',
            'resources/icons/*.png',
            '*.ini'
        ],
    },
    include_package_data=True,
    author='PineRootLabs',
    author_email='DevDark249@gmail.com',
    description='Navegador minimalista leve e rápido com foco em privacidade',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='browser navegador minimalista python pyqt',
    url='https://github.com/PineRootLabs/Browlite',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Environment :: X11 Applications :: Qt',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
    ],
)