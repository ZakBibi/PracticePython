from contextlib import closing
import pg8000

from CodingPractice.PythonAssignments.shoppingcart.dao.PostageRateDao import PostageRateDao
from CodingPractice.PythonAssignments.shoppingcart.domain.PostageRateDto import PostageRateDto
from CodingPractice.PythonAssignments.shoppingcart.dao.PostageRateDict import PostageRateDict


class PostageRatePostgresDao(PostageRateDao, PostageRateDict):

    def __init__(self, postgres_instance):
        super().__init__()
        self._postgres_conn = pg8000.connect(**postgres_instance.dsn())
        self._make_postage_rate_dict(self.get_postage_rates())

    INSERT_SQL = '''INSERT INTO postage(iso_country_code,
                    weight,
                    postage_class,
                    rates)
                    VALUES(%s, %s, %s, %s);'''

    @staticmethod
    def _create_postage_rate_dto_from_row(row):
        return PostageRateDto(iso_country_code=row[0], weight=row[1], postage_class=row[2], rate=row[3])

    def _fetch_products_with_sql(self, sql):
        with closing(self._postgres_conn.cursor()) as cursor:
            cursor.execute(sql)
            postages = cursor.fetchall()
            return [self._create_postage_rate_dto_from_row(row) for row in postages]

    def get_postage_rates(self):
        return self._fetch_products_with_sql('SELECT * FROM postage;')

    def get_postage_rates_by_iso_country_code(self, iso_country_code):
        postage = self._fetch_products_with_sql("SELECT * FROM postage WHERE iso_country_code='"+iso_country_code+"';")
        if postage:
            return postage[0]

    def get_postage_rates_by_weight(self, weight):
        postage = self._fetch_products_with_sql(f"SELECT * FROM postage WHERE weight={weight};")
        if postage:
            return postage[0]

    def get_postage_rates_by_postage_class(self, postage_class):
        postage = self._fetch_products_with_sql(f"SELECT * FROM postage WHERE postage_class={postage_class};")
        if postage:
            return postage[0]

    def get_postage_rate(self, iso_country_code, weight, postage_class):
        key = (iso_country_code, self._convert_weight(weight), postage_class)
        return self._postage_rate_dict[key]

    def create_postage_rate(self, postage_dto):
        weight = self._convert_weight(postage_dto.get_weight())
        postage_tuple = (postage_dto.get_iso_country_code(),
                         weight,
                         postage_dto.get_postage_class(),
                         float(postage_dto.get_rate()))
        with closing(self._postgres_conn.cursor()) as cursor:
            cursor.execute(self.INSERT_SQL, postage_tuple)