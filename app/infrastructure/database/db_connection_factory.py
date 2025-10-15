from psycopg2 import pool

class DBConnectionFactory:
    _connection_pool = None

    @classmethod
    def initialize(cls, minconn: int = 1, maxconn: int = 5):
        if cls._connection_pool is None: #Singleton pattern
            cls._connection_pool = pool.SimpleConnectionPool(
                minconn, maxconn,
                user='your_user',
                password='your_password',
                host='your_host',
                port='your_port',
                database='your_database'
            )

    @classmethod
    def get_connection(cls):
        if cls._connection_pool is None:
            raise Exception("Connection pool is not initialized")
        return cls._connection_pool.getconn()
    
    @classmethod
    def release_connection(cls, connection): # Return connection to the pool
        cls._connection_pool.putconn(connection)

    @classmethod
    def close_pool(cls): #only when application shuts down
        if cls._connection_pool is not None:
            cls._connection_pool.closeall()
            cls._connection_pool = None