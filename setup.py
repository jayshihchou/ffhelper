from importlib.metadata import entry_points
import runpy

from setuptools import setup

__version__ = runpy.run_path('ffhelper/__init__.py')['__version__']


setup(
    name='ffhelper',
    version=__version__,
    author='Chou, Shih-Chieh',
    author_email='jayshihchou@gmail.com',
    url='https://github.com/jayshihchou/ffmpeg_helper',
    description='ffhelper is a ffmpeg helper',
    packages=['ffhelper'],
    license='MIT',
    python_requires='>=3.6',
    keywords=['ffmpeg', 'ffmpeg_helper', 'ffhelper'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS'
    ],
    entry_points={
        'console_scripts': [
            'ffhelper=ffhelper.__main__:run'
        ]
    }
)
