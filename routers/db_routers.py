class AuthRouter:
    route_app_labels = ['posts', 'myarchive', 'auth', 'contenttypes', 'sessions', 'admin', 'users']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'users'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'users'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in ['posts', 'myarchive', 'auth', 'contenttypes', 'sessions', 'admin', 'users'] or
                obj2._meta.app_label in ['posts', 'myarchive', 'auth', 'contenttypes', 'sessions', 'admin', 'users']
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'users'
        return None


class posts:
    route_app_labels = ['posts', 'myarchive', 'auth', 'contenttypes', 'sessions', 'admin', 'users']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'posts'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'posts'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in ['posts', 'myarchive', 'auth', 'contenttypes', 'sessions', 'admin', 'users'] or
                obj2._meta.app_label in ['posts', 'myarchive', 'auth', 'contenttypes', 'sessions', 'admin', 'users']
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'posts'
        return None


class myarchive:
    route_app_labels = ['posts', 'myarchive', 'auth', 'contenttypes', 'sessions', 'admin', 'users']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'myarchive'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'myarchive'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'myarchive'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in ['posts', 'myarchive', 'auth', 'contenttypes', 'sessions', 'admin', 'users'] or
                obj2._meta.app_label in ['posts', 'myarchive', 'auth', 'contenttypes', 'sessions', 'admin', 'users']
        ):
            return True
        return None