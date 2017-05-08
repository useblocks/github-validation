.. _gwdbvalidators:

GwDbValidatorsPattern
=====================

This patterns provides functions to automatically hash and validate data requests on SQLAlchemy models.

It is used to prove that data handling of used libraries and services works correct.
The below image shows the flow of data which is stored to a database and requested back.
As you can see at least 3 libraries/services are used, which behavior and source code is not under your full control.

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

.. _gwdbvalidator_config:

Configuration
-------------

``GwDbValidatorsPattern`` stores the hashes in its own database.
Like other databases in groundwork, the used database connection string can be configured inside the application
configuration file by setting **HASH_DB**::

   HASH_DB = "sqlite://%s/hash_db" % APP_PATH

The format of the connection string is documented inside the
`SQLAlchemy documentation <http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls>`_.

If no connection string is configured, **"sqlite://"** is used as default value.

Technical background
--------------------
To provide a reliable validation, the
:class:`~groundwork_validation.patterns.gw_db_validators_pattern.gw_db_validators_pattern.GwDbValidatorsPattern`
hooks into the
`event system of SQLAlchemy <http://docs.sqlalchemy.org/en/latest/core/event.html>`_
to get notified about each important action and run own validation tasks.

To store its own hashes, ``GwDbValidatorsPattern`` is using its own database, which is registered and
available in groundwork under the name **hash_db**.

For each database model, ``GwDbValidatorsPattern`` registers a validator with the help of
:class:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.GwValidatorsPattern`.
As attributes only the table columns are taking into account.
So no additional attributes like SQLALchemy internal ones or model functions are used.

Storing data
~~~~~~~~~~~~
``GwDbValidatorsPattern`` has registered its own hash creation function for the SQLAlchemy events **after_update** and
**after_insert**.

If one of these events is triggered, ``GwDbValidatorsPattern`` gets the model instance and creates with the help of
:class:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.GwValidatorsPattern` a new
hash.

This hash gets stored together with an ID into the hash database. The ID must be unique and our function must
be able to regenerate it based on given and static information.
So the ID contains: validator name, database table name and model instance id.
Example: *my_validator.user_table.5*.
This kind of an ID allows us to store hashes for all database models into one single database table.

Receiving data
~~~~~~~~~~~~~~
``GwDbValidatorsPattern`` has registered its own hash validation function for the SQLAlchemy event
**refresh**.

If this gets called, ``GwDbValidatorsPattern`` retrieves the received database model instance.
For this it regenerates the hash ID and requests the stored hash value.
With the configured validator of the
:class:`~groundwork_validation.patterns.gw_validators_pattern.gw_validators_pattern.GwValidatorsPattern` it validates
the stored hash against the retrieved database model instance.

If the validation fails, the exception
:class:`~groundwork_validation.patterns.gw_db_validators_pattern.gw_db_validators_pattern.ValidationError`
gets raised. If this happens, the plugin developer is responsible to handle this exception the correct way.


Requirements & Specifications
-----------------------------

The following sections describes the implemented requirements and their related specifications.

**Available requirements**

.. needfilter::
   :tags: gwdbvalidator_pattern
   :types: req
   :layout: table

**Available specifications**

.. needfilter::
   :tags: gwdbvalidator_pattern
   :types: spec
   :layout: table

Requirements
~~~~~~~~~~~~

.. req:: Validation per database table
   :tags: gwdbvalidator_pattern

   As developer I want to be able to to activate the validation of single database table so that
   I'm sure retrieved data is valid.

Specification
~~~~~~~~~~~~~

.. spec:: DB Validation registration
   :tags: gwdbvalidator_pattern
   :links: R_7F7C2;

   A function ``self.validators.db.register`` must be implemented, to allow the registration of database classes
   for validation. The following parameters must be available:

   * name of the registered db validator.
   * description of the registered db validator.
   * database class (sqlalchemy), which write/read operations shall be validated.


