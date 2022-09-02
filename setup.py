from setuptools import find_packages, setup

setup(
    name='django_action_reservation',
    version='0.0.0',
    packages=find_packages(exclude=['demo*']),
    install_requires=[
        'django>=3.5',
        'django-appconf>=1.0.0',
    ]
)
