Any .py or .so file in this folder can be called from the climate analyser backend

__init__.py enables the climate analyser to use import operators to reference
all included py files. 

To properally support intergration with the backend all operations must be called
with a function as follows

def run(inputFiles, outputFIles):

The exception is cdoOps.py which is called to handle any cdo operation.
