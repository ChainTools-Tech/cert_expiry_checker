from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='cert_exp_check',
    version='1.0.0',
    author='qf3l3k',
    author_email='qf3l3k@gmail.com',
    description='Certificate expiration checker.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/qf3l3k/pgbackup',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cert_exp_check=cert_exp_check:main'
        ],
    }
)