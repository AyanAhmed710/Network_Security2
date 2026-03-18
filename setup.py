from setuptools import setup, find_packages
from typing import List


def get_requirements() -> List[str]:

    try : 
        requirements_lst=[]
        with open('requirements.txt' , 'r') as f :

            for line in f.readlines() :
                line.strip()
                if line and line != '-e .':
                    requirements_lst.append(line)

    except FileNotFoundError :
        print("Requirements file not found. Please ensure 'requirements.txt' exists.")


    return requirements_lst

setup(
    name='network_security2',
    version='0.0.1',
    author='ayan',
    author_email="sheikhayanahmad710@gmail.com",
    description='A package for network security',
    packages=find_packages(),
    install_requires=get_requirements()
)


