#!/bin/sh
kinit jgross
aklog
echo $@
ssh -A jgross@linerva.mit.edu $@
