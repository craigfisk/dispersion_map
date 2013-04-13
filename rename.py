#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys, os, re

DEBUG = True

def rename_files(path, pattern, repl):
    """ Note:  only does a substitution on the "performance" part of the file name
    """
    oldfilenames = []
    newfilenames = []

    try:
        for root, dirs, files in os.walk(path):
            for f in files:
                p = re.sub(pattern, repl, f)

                oldfilename = os.path.join(root, f)
                oldfilenames.append(oldfilename)

                newfilename = os.path.join(root, p)
                if newfilename != oldfilename:
                    newfilenames.append(newfilename)
                    if DEBUG:
                        print "changed: %s" % newfilename
                        print "oldfilename: %s \nnewfilename: %s" % (oldfilename, newfilename)
                    if not DEBUG:
                        try:
                            os.rename(oldfilename, newfilename)
                        except OSError as err:
                            print ('OSError: ' + str(err) + ' for oldfilename: ' + 
                                    oldfilename + ' with newfilename: ' + newfilename)
                
                
    except IOError, err:
        print err

    filenames = sorted(newfilenames)

    for filename in filenames:
        print "filename: %s" % filename

    print "Checked %d files and renamed %d files" % (len(oldfilenames), len(newfilenames))
    if DEBUG: 
        print "Didn't actually change any file names because DEBUG is on"

if __name__ == '__main__':
#    if len(sys.argv) == 3:
#        rename_files(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 4:
        rename_files(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print "Supplied %d arguments" % len(sys.argv) 
#        print 'Usage:  ./rename.py /music-archive/directory what_to_insert_before_title'
#        print '        or'
        print 'Usage:'
        print '    ./rename.py /music-archive/directory old_text new_text'
        print 'If DEBUG: True, changes are not actually made; otherwise they are.'
        if DEBUG: print 'True'
        else: print 'False'

"""
    import argparse
    parser = argparse.ArgumentParser(description='Convert music file tree to database table.')
    parser.add_argument('-u', '--upload', help='<database>.<table> to which to upload', required=True)
    parser.add_argument('-s', '--source', help="directory tree from which to convert music file information", required=True)
    
    args = parser.parse_args()
    # argsdict dictionary will have argsdict['source'], argsdict['upload']
    argsdict = vars(args)
    if DEBUG:
        print "Command line:"
        for k in argsdict.keys(): 
            print "\t%s: %s" % (k, argsdict[k])
 
"""
#    if argsdict['upload'] and argsdict['source']:
 
