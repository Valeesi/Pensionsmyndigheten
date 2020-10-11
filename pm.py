#!/usr/bin/python3

import argparse
import datetime
import time
import sys
import os


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Find unmodified files in a directory")
    parser.add_argument("-i", '--include_hidden', action='store_true', help="Include hidden files")
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument("-p", '--path', type=str, metavar='', required=True, help="Target directory")
    required_args.add_argument("-d", '--days', type=str, metavar='', required=True,
                               help="Days without modification, maximum 50 years")
    return parser


def check_if_days_valid(days):
    try:
        days = int(days)
        if 0 > days or days > 365 * 50:
            sys.exit("Invalid input. Number of days must be a natural number between 0 and 18250 (50 years)")
    except ValueError as err:
        sys.exit("ValueError: " + str(err))


def check_if_path_valid(path):
    if not os.path.isdir(path):
        sys.exit("-p must be a valid directory path.")


def get_cutoff_time_from_now(days):
    return datetime.datetime.now() - datetime.timedelta(days=int(days))


def get_all_files_from_path(path):
    return filter(os.path.isfile, os.listdir(path))


def sort_files_by_mtime(files, include_hidden):
    return sorted((include_hidden and files) or [i for i in files if not i.startswith(".")], key=os.path.getmtime)


def get_maximum_filename_length(files, path):
    return str(max(map(len, files)) + len(path))


def get_output_format(sorted_files, path):
    return "{:" + get_maximum_filename_length(sorted_files, path) + "s} {:30s}"


def print_files_with_mtime(files, output_column_space):
    for f in files:
        print(output_column_space.format(f, datetime.datetime.strftime(get_mtime_from_file(f),
                                                                       "%Y-%m-%d %H:%M:%S.%f")))


def get_mtime_from_file(f):
    return datetime.datetime.fromtimestamp(os.stat(f).st_mtime)


def get_files_before_cutoff_time(files, cutoff_time):
    return list(filter(
        lambda f: get_mtime_from_file(f) <= cutoff_time, files))


def print_files_by_mtime(path, days, include_hidden):
    check_if_days_valid(days)
    check_if_path_valid(path)

    cutoff_time = get_cutoff_time_from_now(days)
    os.chdir(path)
    files = get_all_files_from_path(path)
    files_before_cutoff_time = get_files_before_cutoff_time(files, cutoff_time)

    if len(files_before_cutoff_time) == 0:
        print("No search results.")
        exit(0)
    else:
        sorted_files = sort_files_by_mtime(files_before_cutoff_time, include_hidden)
        output_format = get_output_format(sorted_files, path)
        print_files_with_mtime(sorted_files, output_format)


if __name__ == "__main__":
    args = build_arg_parser().parse_args()
    print_files_by_mtime(args.path, args.days, args.include_hidden)
