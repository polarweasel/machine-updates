# What to use for persistent data storage?
# The display client queries the server at set intervals,
# and wants to know what's changed between runs. If there's
# a state change for any flags, it should update the display,
# but if the change is anything else, it should just store the
# updated data without changing the display.
#
# NOTE: Also need to handle the "no data" case. The server will
# not persist any data, so if the display client queries it and
# gets a "no data" response, it should just leave the display
# as-is. OR, it could mark that machine as MIA.
#
# General logic for the frequent polling:
#   FOR each machine
#     - retrieve existing flag states (load avgs and disk space)
#     - compare each flag state to what just came from the server
#     - IF anything has changed, we need to update the display
#     - store the new data in place of the old
#   END
#
# General logic for the periodic scheduled refreshes:
#   - get data for all machines and store in place of the old
#   - update the display
#   END

import shelve

d = shelve.open(filename)  # open -- file may get suffix added by low-level
                           # library

d[key] = data              # store data at key (overwrites old data if
                           # using an existing key)
data = d[key]              # retrieve a COPY of data at key (raise KeyError
                           # if no such key)
del d[key]                 # delete data stored at key (raises KeyError
                           # if no such key)

flag = key in d            # true if the key exists
klist = list(d.keys())     # a list of all existing keys (slow!)

# as d was opened WITHOUT writeback=True, beware:
d['xx'] = [0, 1, 2]        # this works as expected, but...
d['xx'].append(3)          # *this doesn't!* -- d['xx'] is STILL [0, 1, 2]!

# having opened d without writeback=True, you need to code carefully:
temp = d['xx']             # extracts the copy
temp.append(5)             # mutates the copy
d['xx'] = temp             # stores the copy right back, to persist it

# or, d=shelve.open(filename,writeback=True) would let you just code
# d['xx'].append(5) and have it work as expected, BUT it would also
# consume more memory and make the d.close() operation slower.

d.close()                  # close it