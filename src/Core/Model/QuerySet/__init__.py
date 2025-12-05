class QuerySet:
    def __init__(self, model, db):
        self.model = model
        self.db = db
        self._filters = []
        self._order = []
        self._limit = None
        self._offset = None
    
    def filter(self, **kwargs):
        new = self._clone()
        for field, value in kwargs.items():
            if '__' in field:
                field_name, operator = field.split('__', 1)
                ops = {
                    'gt': '>',
                    'gte': '>=',
                    'lt': '<',
                    'lte': '<=',
                    'contains': 'LIKE',
                    'icontains': 'LIKE',
                    'startswith': 'LIKE',
                    'endswith': 'LIKE'
                }
                sql_op = ops.get(operator, '=')
                
                if operator in ['contains', 'icontains']:
                    value = f'%{value}%'
                elif operator == 'startswith':
                    value = f'{value}%'
                elif operator == 'endswith':
                    value = f'%{value}'
                
                new._filters.append((field_name, sql_op, value))
            else:
                new._filters.append((field, '=', value))
        return new
    
    def order_by(self, *fields):
        new = self._clone()
        for field in fields:
            if field.startswith('-'):
                new._order.append((field[1:], 'DESC'))
            else:
                new._order.append((field, 'ASC'))
        return new
    
    def limit(self, n):
        new = self._clone()
        new._limit = n
        return new
    
    def offset(self, n):
        new = self._clone()
        new._offset = n
        return new
    
    def first(self):
        results = self.limit(1).execute()
        return results[0] if results else None
    
    def get(self, **kwargs):
        results = self.filter(**kwargs).execute()
        if len(results) == 0:
            raise Exception(f"{self.model.__name__} not found with {kwargs}")
        if len(results) > 1:
            raise Exception(f"Multiple {self.model.__name__} found with {kwargs}")
        return results[0]
    
    def count(self):
        sql = f"SELECT COUNT(*) FROM {self.model._table_name}"
        where, params = self._build_where()
        if where:
            sql += f" WHERE {where}"
        
        cursor = self.db.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()[0]
    
    def exists(self):
        return self.count() > 0
    
    def execute(self):
        sql = f"SELECT * FROM {self.model._table_name}"
        
        where, params = self._build_where()
        if where:
            sql += f" WHERE {where}"
        
        if self._order:
            order_sql = ", ".join([f"{field} {direction}" for field, direction in self._order])
            sql += f" ORDER BY {order_sql}"
        
        if self._limit:
            sql += f" LIMIT {self._limit}"
        
        if self._offset:
            sql += f" OFFSET {self._offset}"
        
        cursor = self.db.cursor()
        cursor.execute(sql, params)
        
        results = []
        for row in cursor.fetchall():
            obj = self.model._from_db(row, cursor.description)
            results.append(obj)
        
        return results
    
    def _build_where(self):
        if not self._filters:
            return "", []
        
        conditions = []
        params = []
        
        for field, op, value in self._filters:
            conditions.append(f"{field} {op} ?")
            params.append(value)
        
        return " AND ".join(conditions), params
    
    def _clone(self):
        new = QuerySet(self.model, self.db)
        new._filters = self._filters.copy()
        new._order = self._order.copy()
        new._limit = self._limit
        new._offset = self._offset
        return new
    
    def __iter__(self):
        return iter(self.execute())
    
    def __len__(self):
        return self.count()
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            new = self._clone()
            if key.start:
                new._offset = key.start
            if key.stop:
                new._limit = key.stop - (key.start or 0)
            return new.execute()
        else:
            return self.offset(key).limit(1).execute()[0]
