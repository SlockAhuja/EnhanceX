#!/usr/bin/env bash
# EnhanceX CLI Shell Batch Script Example
# Created by Slock Ahuja (https://github.com/SlockAhuja/EnhanceX)

echo "Running EnhanceX System Diagnostics..."
enhancex doctor

echo "Listing Registered AI Models..."
enhancex models list

echo "Enhancing Input Image in Auto Mode..."
enhancex enhance input.jpg output_enhanced.jpg --mode auto
