import final_server as fs
import pytest
from pymongo import MongoClient
from flask import Flask, jsonify, request

db = fs.init_mongoDB()
app = Flask(__name__)


def test_pullAllData():
    with app.app_context():
        json_payload, http_status = fs.pullAllData()
        payload = json_payload.json
        exp_payload = {
                            "background": [5089.225822202072,
                                           3928.5359746102604,
                                           3928.5359746102604,
                                           3928.5359746102604,
                                           3928.5359746102604,
                                           3928.5359746102604,
                                           3928.5359746102604,
                                           3928.5359746102604,
                                           3928.5359746102604,
                                           3928.5359746102604,
                                           3928.5359746102604,
                                           3928.5359746102604],
                            "filename": ["slide1_1.tiff", "slide1_0.tiff",
                                         "slide1_0.tiff", "slide1_0.tiff",
                                         "slide1_0.tiff", "slide1_0.tiff",
                                         "slide1_0.tiff", "slide1_0.tiff",
                                         "slide1_0.tiff", "slide1_0.tiff",
                                         "slide1_0.tiff", "slide1_0.tiff"],
                            "spots": [[65492.36420233463, 65496.348638132295,
                                       65417.20778210117, 65520.0,
                                       65384.57276264591],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085],
                                      [48030.58677042802, 46267.2186770428,
                                       42864.66614785992, 43446.404006677796,
                                       44654.580544747085]]
                           }
        exp_http_status = 200
        assert payload["background"][0] == exp_payload["background"][0]
        assert payload["filename"][0] == exp_payload["filename"][0]
        assert payload["spots"][0] == exp_payload["spots"][0]
        assert http_status == exp_http_status
