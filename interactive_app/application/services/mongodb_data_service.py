# Uses pymysql for interacting with MySQL
#
import pymongo

# We will use multiple databases over the semester.
# To simplify REST resource implementation and loosely couple application logic to data access.
# In many cases, the design allows modifying the database without affecting application logic.
#
from resources.base_data_service import BaseDataService


class MongoDataServiceConfig:
    """
    Class with configuration information
    """

    def __init__(self, url=None):
        """
        See the pymongo documentation for the explanation of the connection parameters.


        :param url: The connection URL for MongoClient.
        """
        self.url = url


class MongoDBDataService(BaseDataService):

    """
    Implements a class for accessing MongoDB. There are generic implementations of functions, and developers
    can extend for application specific scenarios.
    """

    def __init__(self, config: MongoDataServiceConfig):
        """

        :param config: An object providing configuration information and dependencies. This is a very simple form
            of dependency injection (https://en.wikipedia.org/wiki/Dependency_injection).
        """
        super().__init__(config)

    def get_client(self):
        """

        :return: Returns a new client connected to the Mongo DB server.
        """
        client = pymongo.MongoClient(self.config.url)
        return client

    def run_q(self, sql, args=None, con=None, fetch=False):
        """
        A function that "simplifies" making pymysql SQL calls to the DB.
        :param sql: A SQL statement that may have parameters.
            https://pynative.com/python-mysql-execute-parameterized-query-using-prepared-statement/
        :param args: Arguments for the parameters in the query.
        :param con: A connection for sending commands to the DB.
        :param fetch: If True, return data using fetchall(). If false, return the result of execution.
            https://pymysql.readthedocs.io/en/latest/modules/cursors.html
        :return: Either the result of cursor.execute() for cursor.fetchall()
        """
        pass

    def retrieve(self, database, collection, predicate, project):
        """
        Query the data service/database and return matching items.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param predicate: A dictionary of the form {k, v}. A entity matches if the resource's property v has
            value k, for all entries in the dictionary. That is, a match if logically
            k1 = v1 AND k2 = v2 AND ... ... This maps to a filter in Mongo.
        :param project: A list of subsets of the entity's properties to return. That is, if the list is
            [k1, k2, k3], this is logically like SELECT k1, k2, k3 ...
        :return: A list containing dictionaries of the projected properties for matching entities.
        """
        client = self.get_client()

        f = predicate

        if project:
            project = {k: 1 for k in project}

        result = client[database][collection].find(
            filter=f, projection=project
        )
        client = self.get_client()
        result = list(result)

        client.close()

        return result

    def retrieve_by_id(self, database, collection, id_value):
        """
        Query the data service/database and return matching items.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param id_value: The MongoDB object ID.
        :return:The resource with matching ID.
        """
        raise NotImplemented()

    def delete(self, database, collection, predicate):
        """
        Delete documents from the collection matching the condition.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param predicate: A dictionary of the form {k, v}. A entity matches if the resource's property v has
            value k, for all entries in the dictionary. That is, a match if logically
            k1 = v1 AND k2 = v2 AND ... ...
        :return: The count of the number of elements deleted.
        """
        raise NotImplemented()

    def update(self, database, collection, predicate, new_data):
        """
        Update matching documents.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param predicate: A dictionary of the form {k, v}. A entity matches if the resource's property v has
            value k, for all entries in the dictionary. That is, a match if logically
            k1 = v1 AND k2 = v2 AND ... ...
        :param new_data: The keys and values used to update the documents.
        :return: The number of documents updated.
        """
        raise NotImplemented()

    def create(self, database, collection, new_data):
        """
       Insert documents into the database.

        :param database: The database.
        :param collection: In MySQL, this would be a table. In MongoDB this is a collection.
        :param new_data: The data to insert into the table. This is a single document.
        :return: The ID of the created document.
        """
        raise NotImplemented()
