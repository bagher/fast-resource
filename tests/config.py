from fast_resource import Resource

inputs = {
    'bagher': {'id': 1, 'name': 'Bagher', 'family': 'Rokni'},
    'sepehr': {'id': 2, 'name': 'Sepehr', 'family': 'Rokni'},
    'sama': {'id': 3, 'name': 'Sama', 'family': 'Rokni'},
}

outputs = {
    'bagher': {'id': 1, 'name': 'Bagher Rokni'},
    'sepehr': {'id': 2, 'name': 'Sepehr Rokni'},
    'sama': {'id': 3, 'name': 'Sama Rokni'},
}


class UserResource(Resource):
    class Meta:
        fields = (
            'id',
            'name',
        )

    def name(self, input_data):
        return f'{input_data["name"]} {input_data["family"]}'
