import io
from setuptools import setup, find_packages


setup(
    name='stream-redirect',
    description='Collect and redirect stdout and stderr from a python program',
    long_description_content_type="text/markdown",
    long_description=io.open('README.md', encoding='utf-8').read(),
    author='Greg Hellings',
    author_email='greg.hellings@gmail.com',
    url='https://github.com/greg-hellings/stream_redirect',
    license='GPLv3',
    version='0.1.2',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=['six'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing'
    ]
)
