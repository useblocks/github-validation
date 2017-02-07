.. _gwdbvalidators:

GwDbValidatorsPattern
=====================

This patterns provides functions to automatically hash and validate data requests on SQLAlchemy models.

This may be needed to validate that data handling of used libraries and services works correct.
The below image shows the flow of data which is stored to a database and requested back.
As you can see at least 3 libraries/services are used to work with your data.

.. image:: /_static/db_hash_workflow.png
   :scale: 50%
   :align: center

Every time a registered database model is updated and uploaded to the database (add -> commit),
``GwDbValidatorsPattern`` creates and stores a hash of the updated data model.

And every time a request is made on a registered database model (e.g by model.query.filter_by(x="abc").all()),
``GwDbValidatorsPattern`` validates each received row against stored hashes.

Hashes are stored inside a database (via groundwork-database) and based on its configuration, an external
database may be used so that hashes are still available and valid after application restarts.




Register a new database validator
---------------------------------

To register a new database validator, a plugin must inherit from
:class:`~groundwork_validation.patterns.gw_db_validators_pattern.gw_db_validators_pattern.GwDbValidatorsPattern` and use
:func:`~groundwork_validation.patterns.gw_db_validators_pattern.gw_db_validators_pattern.DbValidatorsPlugin.register`
for registration::

    from groundwork_validation.patterns import GwDbValidatorsPattern

    class My_Plugin(GwDbValidatorsPattern):
        def __init__(self, app, **kwargs):
            self.name = "My_Plugin"
            super(My_Plugin, self).__init__(app, **kwargs)
            self.db = None
            self.Test = None

        def activate(self):

            # START: groundwork-database related configuration
            ##########################################################################

            # Let's create a new database, which models shall use validated request.
            self.db = self.app.databases.register("test_db",
                                                  "sqlite://",
                                                  "database for test values")

            # A simple SQLAlchemy database model
            class Test(self.db.Base):
                __tablename__ = "test"
                id = Column(Integer, primary_key=True)
                name = Column(String(512), nullable=False, unique=True)

            # Register our database model
            self.Test = self.db.classes.register(Test)
            # Create all tables
            self.db.create_all()

            ###########################################################################
            # END: groundwork-database related configuration

            # Register and activate validation for your model
            self.validators.db.register("db_test_validator",
                                        "my db test validator",
                                        self.Test)

Validate requests
-----------------
Your validation has already started. The registration of a database model is enough to start the validation for
each request. If a validation problem occurs, groundwork-validation will throw the exception
:class:`~groundwork_validation.patterns.gw_db_validators_pattern.gw_db_validators_pattern.ValidationError`.

Test validation
---------------

To test the validation, you need to manipulate the data of a stored and monitored data model.
This could be done via an external database editor like the `Sqlite Browser <http://sqlitebrowser.org/>`_ or by
executing SQL statements directly::

    from groundwork_validation.patterns import GwDbValidatorsPattern

    class My_Plugin(GwDbValidatorsPattern):
        ...

        def activate(self):
            ...
            my_test = self.Test(name="blub")
            self.db.add(my_test)
            self.db.commit()
            self.db.query(self.Test).all()

            my_test.name = "Boohaaaa"
            self.db.add(my_test)
            self.db.commit()
            self.db.query(self.Test).all()

            # Execute sql-statement, which does not trigger the sqlalchemy events.
            # So no hash gets updated.
            self.db.engine.execute("UPDATE test SET name='not_working' WHERE id=1")

            # Reloads the data from db and will throw an exception
            self.db.session.refresh(my_test)


