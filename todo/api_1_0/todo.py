from flask import current_app, jsonify

from flask_restful import Resource, fields, marshal_with, marshal
from flask_restful import reqparse
from flask_restful import abort
from flask_jwt_extended import jwt_required

from todo.api_1_0 import api
from todo.models import Todo


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', required=True, help="Specified a todo name.")
parser.add_argument('is_done', type=bool, location='json', required=True, help="Specified a todo is done flag.")

parser.add_argument('is_important', type=bool, location='json', required=True, help="Specified a todo is important flag.")


class ToDoMixin:
    fields = dict(
        id=fields.Integer,
        name=fields.String,
        publish_time=fields.DateTime,
        is_done=fields.Boolean,
        is_important=fields.Boolean
    )

    def get_object_or_404(self, id):
        todo = Todo.query.get(id)
        if todo is None:
            abort(404, message="Task {} doesn\'t exist".format(id))
        else:
            return todo


class ToDoList(Resource, ToDoMixin):

    method_decorators = [jwt_required]

    def get(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('page', type=int, location='args', required=False)
        args = get_parser.parse_args()
        page = args.get('page', 1)
        page_fields = dict(
            prev=fields.Boolean,
            next=fields.Boolean,
            total=fields.Integer,
            per=fields.Integer,
            current=fields.Integer
        )
        todos_fields = dict(
            page=fields.Nested(page_fields),
            todos=fields.Nested(ToDoMixin.fields)
        )
        pagination = Todo.query.order_by(
            Todo.is_done.desc(),
            # Todo.is_important.desc(),
            Todo.publish_time.desc()
        ).paginate(
            page,
            per_page=current_app.config['COUNTS_OF_PER_PAGE'],
            error_out=False
        )
        todos_data = dict(
            page=dict(
                prev=pagination.has_prev,
                next=pagination.has_next,
                total=pagination.total,
                per=current_app.config['COUNTS_OF_PER_PAGE'],
                current=page
            ),
            todos=pagination.items
        )
        return jsonify(marshal(todos_data, todos_fields))

    def post(self):
        todo = Todo()
        args = parser.parse_args()
        todo.name = args.get('name')
        todo.is_done = args.get('is_done')
        todo.is_important = args.get('is_important')
        todo.save()
        return jsonify(marshal(todo, self.fields)), 201


class ToDo(Resource, ToDoMixin):

    method_decorators = [jwt_required]

    @marshal_with(ToDoMixin.fields)
    def get(self, todo_id):
        return jsonify(self.get_object_or_404(todo_id))

    def put(self, todo_id):
        todo = self.get_object_or_404(todo_id)
        args = parser.parse_args()
        todo.name = args.get('name')
        todo.is_done = args.get('is_done')
        todo.is_important = args.get('is_important')
        todo.save()
        return jsonify(marshal(todo, self.fields))

    def delete(self, todo_id):
        todo = self.get_object_or_404(todo_id)
        todo.delete()
        return jsonify({'message': 'Task {} has been deleted.'.format(todo_id)}), 201


api.add_url_rule('/todos/', view_func=ToDoList.as_view('todolist'))
api.add_url_rule('/todos/<int:todo_id>/', view_func=ToDo.as_view('todo'))


# def format_request_datetime(value, name):
#     try:
#         value = datetime.datetime.strptime(
#             value,
#             current_app.config['DATETIME_FORMAT_STRING']
#         )
#     except ValueError:
#         return ValueError('Specified datetime format like {}.'.format(current_app.config['DATETIME_FORMAT_STRING']))
#     return value
