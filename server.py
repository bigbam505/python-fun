#!/usr/bin/python

import sys
import json
import yaml
import os.path
from bottle import route, run, template, response, request, error

config = 0

def make_json_response(obj):
  response.content_type = "application/json"
  return json_convert(obj)

def json_convert(obj):
  return json.dumps(obj)

def json_parse(obj):
  return json.loads(obj)

@route('/api/url', method="GET")
def get_url():
  url_object = load_url()
  return make_json_response(url_object)

@route('/api/url', method="POST")
def set_url():
  json = request.json
  if(not json):
    response.status = 400
    return

  response.status = 202
  save_url(json['url'])
  return make_json_response({})

@error(404)
def mistake_404(code):
  return make_json_response({ 'error': 'Not Found'})

def save_url(url):
  url_file_path = config['url_location']
  if(not os.path.isdir(os.path.dirname(url_file_path))):
    os.makedirs(os.path.dirname(url_file_path))

  f = open(url_file_path,'w')
  f.write(json_convert({'url': url}))
  f.close()

def load_url():
  url_file_path = config['url_location']
  if(not os.path.isdir(os.path.dirname(url_file_path))):
    os.makedirs(os.path.dirname(url_file_path))

  if(not os.path.isfile(url_file_path)):
    save_url('')

  f = open(url_file_path, 'r')
  return json_parse(f.read())


def load_config(config_file):
  global config
  if(os.path.isfile(config_file)):
    f = open(config_file)
    config = yaml.safe_load(f)
    f.close()

def main(argv):
  if(len(argv) > 0):
    load_config(argv[0])
  else:
    load_config('service.yaml')
  if(not config):
    print 'Not config loaded, please add a config file'
    print 'Usage: python server.py configfile.yaml'
    return
  print 'Argument List:', str(argv)
  run(host=config['host'], port=config['port'])

if __name__ == "__main__":
  main(sys.argv[1:])
