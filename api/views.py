#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import re, json
import traceback
from flask import request
from flask import Response

from .decorators import authenticate

from .util import RawHtmlFetcher, GooseAPI
import json

import traceback
import os, redis, psycopg2


@authenticate.requires_auth
def extract():
    err = lambda code, message: Response(
        json.dumps({"success": False, "error": message}),
        mimetype="application/json",
        status=str(code),
    )
    try:
        url = request.args.get("url")
        if url is None:
            return err(422, "`url` parameter is missing")

        redis_url = request.args.get("redis_url")
        if redis_url is None:
            return err(422, "`redis_url` parameter is missing")

        data_key = request.args.get("data_key")
        if data_key is None:
            return err(422, "`data_key` parameter is missing")

        data_from_redis = RawHtmlFetcher(redis_url, data_key).acquire()

        if data_from_redis:
            extracted_content = GooseAPI(
                url, data_from_redis["result"]["body"]
            ).extract()
            return Response(json.dumps(extracted_content), mimetype="application/json")
        else:
            return err(500, "Could not fetch raw html from redis")
    except Exception as error:
        print(traceback.format_exc().splitlines())
        return err(500, "Goose Internal server error: " + str(error))


def health_check():
    try:
        connection = psycopg2.connect(
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"],
        )
        cursor = connection.cursor()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return "Health check failed: %s" % error, 500
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return "SERVICE OK"


def redis_health_check():
    try:
        redis.from_url(os.environ["REDIS_URL"]).ping()
    except Exception as error:
        print("Error while connecting to Redis", error)
        return "Health check failed: %s" % error, 500
    return "SERVICE OK"


def temproute():
    return "SERVICE running OK"
