# pyreport - a lightweight Python reporting library
from .formatter import truncate, center_heading, bullet_list
from .stats import mean, weighted_average, median, variance
from .filters import filter_by_value, filter_date_range, filter_top_n
from .serializer import serialize_record, serialize_records, to_json
from .aggregator import group_by, sum_column, count_distinct
from .validator import validate_email, validate_positive_number, validate_record
from .pager import paginate, total_pages
from .merger import deep_merge, merge_shards

__all__ = [
    "truncate", "center_heading", "bullet_list",
    "mean", "weighted_average", "median", "variance",
    "filter_by_value", "filter_date_range", "filter_top_n",
    "serialize_record", "serialize_records", "to_json",
    "group_by", "sum_column", "count_distinct",
    "validate_email", "validate_positive_number", "validate_record",
    "paginate", "total_pages",
    "deep_merge", "merge_shards",
]
