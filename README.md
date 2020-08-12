# contour_python
A python script to plot contour with scattered data for my wife. Note: format of input data is limited to specific features; i.e. two lines with label and zone are required before real data.

Simple interface for user use: ask user to input path and filename to load file; ask user to input zone number and label number to plot contour.

Skip rows that is not useful, until find lines with labels and zones.

Extract labels from line started with 'variables'.

Extract zone number from line started with 'zone'.

Build figure according to requirement of science paper format.
