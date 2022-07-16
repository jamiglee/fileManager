#!/usr/bin/python
# -*- coding: UTF-8 -*-
# coding=utf-8
import sys

import scan_directories as scan

def show_main_desc():
    print("Welcome to use duplicate files scanner!\n"
          "Please choose your operation:\n"
          "1. scan duplicate files\n"
          "2. delete duplicate files\n")

def main():
    show_main_desc()
    a = sys.stdin.readline()
    print(a)
    if a == 1:
        print("12")
    return


main()