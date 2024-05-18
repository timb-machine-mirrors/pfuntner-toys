#! /usr/bin/env bash

parser=$(argparse argument-parser --name "$0" --description="Description")
parser=$(argparse add-argument --parser "$parser" --argument=paths --metavar=path --nargs='*' --help-text="Zero or more paths")
parser=$(argparse add-argument --parser "$parser" --argument=-v --argument=--verbose --arg-action=count --help-text="Enable debugging")

args=$(argparse parse-args --parser "$parser" -- "$@")
if test -n "$args" && echo "$args" | base64 -d >/dev/null 2>&1
then
  log=$(logging --level=WARNING-$(argparse get --args $args verbose))
  logging --log "$log" --info "paths=$(argparse get --args $args paths)"
else
  echo -n "$args" >&2
fi
