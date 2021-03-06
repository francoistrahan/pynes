# Pynetrees Decision Tree Librairy

The Pynetrees decision tree librairy is still very young. I wrote it in a moment
of inspiration while studying with Prof. Angelos Georghiou. We had a bit of fun
and I hope I can put my head to it someday soon.

I put it online after someone asked to give it a spin. If you are familiar with
Jupyter, I suggest that you start by looking at the examples in the pynetrees
folder. If you are not familiar with Jupyter, I suggest you go learn about this
amazing tool as soon as you can.

I do commit to making this repository better and adding a bit more
documentation, but it might take a while until it actually happens. Until then,
don't hesitate to send me an email for questions, suggestions or anything else:
francois.trahan@gmail.com

Have fun!

# How to use pynetrees as part of a larger project

Given dependencies on a few projects that evolve very fast and have a track
record of introducing breaking changes, I strongly advise to work within a
virtual environment.

Pynetrees is available on PyPI. To install pynetrees within your environment
(virtual or not), simply use the following command:

`pip install pynetrees`

# How to get going if you want to develop on Pynetrees (or just play with it)

For developers who would like to explore the pynetrees library with the ambition
of thinkering with it, or if you want to bootstrap an environment to play with
it, here are suggested steps:

- Checkout or download the code on your computer
- Create and activate a virtual environment (python >=3.6)
- Within this environment, go to the "pynetrees" folder
- Run the command `poetry install`
  - This will install all the dependencies to use Pynetrees
  - It will also install dependencies for development and testing
- If you want, you may run the command `pytest -v` to execute the unittests

If you intend to use pynetrees within a Jupyter notebook or look at the examples that
are in the repository, running the following commands will get you going:

- Run the command `poetry install --extras examples`
  - This will install jupyter-notebook and dependencies into your virtual environment
- From there on, you may run `jupyter-notebook` to work with jupyter
  - You may run the command `jupyter-notebook "Drill Example.ipynb"` for an example of how to use pynetrees



# Todo

- Upgrade to pandas >= 0.24 (breaking changes)
- Remove explicit tornado version (version 6.0.0 clashes with jupyter notebook; that should be fixed at some point)
- Explicitly control whether tests should pop resulting graphs
