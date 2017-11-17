# -*- coding: utf-8 -*-

"""JSON log tailer.

Usage:
  tail [--cross-finger] [--message=<text>] [--grep=<text> <filename>
  tail (-h | --help)
  tail --version

Options:
  -h --help       Show this screen.
  --version       Show version.
  --cross-finger  Output only if there was ERROR.
  --message=<text> Show only items with this text in message.
  --grep=<text> Show only items with this text in any field.

"""

import tailer
import anyjson
import re
import click
import sys

from click import echo
from collections import defaultdict


def print_item(item, only_fields):
    fields = item.get('@fields', item.get('fields', {}))

    if '@timestamp' in item:
        ts = item['@timestamp'].replace('T', ' ')
    elif 'timestamp' in item:
        ts = item['timestamp'].replace('T', ' ')
    elif 'time' in item:
        ts = item['time'].replace('T', ' ')
    elif 'timestamp' in fields:
        ts = fields['timestamp'].replace('T', ' ')
    elif 'time' in fields and isinstance(fields['time'], basestring):
        ts = fields['time'].replace('T', ' ')
    else:
        ts = None

    if '@message' in item:
        msg = item['@message']
    elif 'message' in item:
        msg = item['message']
    elif 'msg' in item:
        msg = item['msg']
    elif 'message' in fields:
        msg = fields['message']
    elif 'msg' in fields:
        msg = fields['msg']
    else:
        msg = 'No message'

    if ts:
        echo(u'{ts} {msg}'.format(ts=ts, msg=msg))
    else:
        echo(u'{msg}'.format(ts=ts, msg=msg))

    for key, value in sorted(fields.items()):
        if not only_fields or key in only_fields:
            echo((u' ' * 20 + u'{0} = {1}').format(key, value))


@click.command()
@click.option('--cross-finger', is_flag=True,
              help='Output only if there was ERROR.')
@click.option('--message',
              help='Show only items with this text in message.')
@click.option('--fields',
              help='Comma-separated list of fields to output. By default, all fields are printed.',
              default='')
@click.option('--grep',
              help='Show only items with this text in any field.')
@click.option('--name',
              help='Show only items with logger name which matches to this regexp.')
@click.argument('filename', required=False)
def main_func(filename, cross_finger, message, fields, grep, name):
    buffer = defaultdict(list)

    fields = set(filter(None, fields.split(',')))

    def print_if_needed(item, line):
        if message:
            if re.search(message, item['@message'], re.I) is None:
                return
        if grep:
            if re.search(grep, line, re.I) is None:
                return
        if name:
            if re.search(name, item['@fields'].get('name', ''), re.I) is None:
                return
        print_item(item, fields)


    if filename:
        stream = open(filename)
        stream = tailer.follow(stream)
    else:
        def unbuffered_lines(stream):
            while True:
                line = stream.readline()
                if line == '':
                    return

                yield line

        stream = unbuffered_lines(sys.stdin)

    for line in stream:
        try:
            item = anyjson.deserialize(line)
        except:
            continue

        if cross_finger:
            fields = item['@fields']
            if 'uuid' in fields:
                uuid = fields['uuid']
                buffer[uuid].append(item)
                if fields['level'] == 'ERROR':

                    echo('')
                    echo('=' * 80)
                    for item in buffer[uuid]:
                        print_if_needed(item, line)
                    del buffer[uuid]
            else:
                if fields['level'] == 'ERROR':
                    print_if_needed(item, line)
        else:
            print_if_needed(item, line)
