from mongodb_migrations.base import BaseMigration
from pymongo.collation import Collation


class Migration(BaseMigration):
    def upgrade(self):
        self.db.create_collection('users', collation=Collation(locale='en_US'))

    def downgrade(self):
        self.db.drop_collection('users')
