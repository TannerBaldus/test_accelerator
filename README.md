# Test Accelerator


##Intro
Test Acclerator is a tool for use with [ElectricAccelerator](http://electric-cloud.com/products/electricaccelerator/) to accelerate unittests tests. 
How this works is test acclerator parses the unittest source files to deduce the full names
of tests an

##Installation
**Requires >=Python 2.7** 

**Windows**: Make sure Python27/Scripts in your PATH variable.

With the proper permissions run:
```bash
pip install test_accelerator
```

Alternativly you can download and extract the source and then
```bash
python setup.py install
```

 
##Usage
To create the MakeFile run the command  ```ecconvert``` with the following
required arguments:
```
  --framework FRAMEWORK				
  		Name of Framework to Parse
  --testrunner TEST_RUNNER			 
  				Path to the testrunner
  --files FILES, -f FILES			  
  				A comma separated list of files and/or directories to parse unittests
  --test_target TEST_TARGET, -t TEST_TARGET  	
  				The compiled test file. ex. tests.dll
```
These optional arguments can also be used
```
 --pattern PATTERN, -p PATTERN
 			glob pattern for files to search
             default = '*'
  --recursive, -r       
  			Whether to recursively search directory
  			default = False
  --makefile-m MAKEFILE_PATH
  			Path to write makefile to.
              default = MakeFile
  --agent AGENTS, -a AGENTS
  			How many agents are you using.
              default = 1

```
An example call:
```bash   
    ecconvert --framework NUnit --testrunner nunit-console.exe -t foo_tests.dll 
    -f Foo/tests,bartests.cs -r -p *.cs --agents 8
```

By default NUnit is the only testing framework defined. However other frameworks can easily be added.

##Defining Frameworks
The settings of a testing framework are defined with a dictonary in settings.py  containg four components:


#####nodes
A list of dictonaries defining how to find the full names of a a test suite or test. (How granular we want to go is up to how many nodes we put in the list)

Consider this example of NUnit code.
```cs
namespace Foo{
	[TestFixture]
	public class CalcTests{
    
    	[Test]
        public void addTest() {
        	Assert.areEqual(4,2+2};
            }
}

```
To run the test fixture CalcTests we would need to call:
```
nunit-console /run=Foo.CalcTests tests.dll 
``` 


