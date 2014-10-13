#! /usr/bin/python

class BaseTest(object):
    """ Base class for the unit tests in each module. """
    def __init__(self, modname, tests):
        """ Initialize tester object. Takes a human readable module name and a
        list of tests to perform on the module.  This method is designed to be
        called via super().
        """
        self.modname = modname
        self.tests = tests

    def run_tests(self):
        """ Run the unit tests. """
        print "Testing module {!s}".format(self.modname)
        for i, test in enumerate(self.tests):
            fname = test.func_name
            test_doc = test.__doc__
            print "Test{!s}: {!s}".format((i+1), test_doc) # print out the test id
            test_result = test()
            if not test_result: # test failure
                print "fail. Name of the test function: %s"%fname
                print "Failure in module test %s"%self.modname
                return 
            else: # test pass, write out the results
                print test_result
        return True
