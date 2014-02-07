from facepy import graph_api


class GraphAPI(graph_api.GraphAPI):
    def _parse(self, data):
        parsed = super(GraphApi, self)._parse(data)
        return get_data_object(data.decode('utf-8'), parsed)


def get_data_object(raw_data, data):
    class DataType(type(data)):
        __slots__ = ('raw_data')

    result = DataType(data)
    result.raw_data = raw_data
    return result
