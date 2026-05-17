from setuptools import setup, find_packages

setup(
    name='vibescan',
    version='1.0.0',
    description='Security scanner for AI-generated (vibe-coded) code',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourusername/vibescan',
    packages=find_packages(),
    install_requires=[
        'click>=8.0',
        'rich>=13.0',
        'jinja2>=3.0',
        'colorama>=0.4',
        'pyyaml>=6.0',
        'requests>=2.31',
    ],
    entry_points={
        'console_scripts': [
            'vibescan=vibescan.cli:main',
        ],
    },
    python_requires='>=3.9',
    classifiers=[
        'Topic :: Security',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
    ],
)
