from flask import Flask, request, redirect, jsonify, render_template, url_for, session
from flask_restful import Api, Resource, reqparse
import database

app = Flask(__name__, template_folder='templates', static_folder='templates/static')
api = Api()























# courses = {
#             1: {'name': 'Java' , 'videos': '15'},
#             2: {'name': 'Kotlin' , 'videos': '20'},
#             3: {'name': 'PHP' , 'videos': '25'}
# }


# class Main(Resource):
#     def get(self):
#         return courses
#
#     def delete(self, id_course):
#         del(courses[id_course])
#         return courses
#
#     def post(self, id_course):
#         parser = reqparse.RequestParser()
#         parser.add_argument("name", type=str)
#         parser.add_argument("videos", type=str)
#         courses[id_course] = parser.parse_args()
#         return courses
#
#     def put(self, id_course):
#         parser = reqparse.RequestParser()
#         parser.add_argument("name", type=str)
#         parser.add_argument("videos", type=str)
#         courses[id_course] = parser.parse_args()
#         return courses
#
#
# api.add_resource(Main, "/api/courses/<int:id_course>")
# api.init_app(app)