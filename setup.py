from setuptools import setup
import json

with open("metadata.json", encoding="utf-8") as fp:
    metadata = json.load(fp)

setup(
    name='lexibank_phond2',
    py_modules=['lexibank_phond2'],
    include_package_data=True,
    url=metadata.get("url",""),
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'phond2=lexibank_phond2:Dataset',
        ]
    },
    install_requires=[
        "pylexibank>=3.0.0"
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
