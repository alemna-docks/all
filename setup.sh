#!/bin/bash

# ===============================================
#   Install extra Python libraries
# ===============================================
pip install -r requirements.txt

# ===============================================
#     Add this directory and the ./_helpers/ 
#    directory to PATH and make all the shell 
#               scripts executable
# ===============================================

# from https://codefather.tech/blog/bash-get-script-directory/
this_dir=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

_helpers_dir=$this_dir/_helpers
echo "Adding $this_dir and $helpers_dir to PATH..."
PATH=$this_dir:$helpers_dir:$PATH
export PATH

for file in $helpers_dir/*; do
    if [[ "$file" == *.sh ]]; then
        echo "Ensuring $file is executable..."
        chmod +x $file
    fi
done

# ===============================================
#   Check bigtree root indicator file
# ===============================================
# To allow some of the scripts in the ./_bigtree directory to be called
# without specifying a bigtree root directory, we will put an indicator
# file in the same directory as this file. If the _bigtree scripts are 
# called without specifying a bigtree root directory, they will search
# for the directory containing the indicator file. 

indicator_file="$this_dir/bigtree"
# Make sure 'indicator_file' is world-readable and executable
chmod a+r "$indicator_file"
chmod +x "$indicator_file"
