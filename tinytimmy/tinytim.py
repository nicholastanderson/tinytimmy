import polars as pl
from pyspark.sql import SparkSession

from tinytimmy.data_quality import DataQuality


class TinyTim(DataQuality):
    def __init__(
        self,
        source_type: str,
        dataframe=None,
        file_path: str = None,
        spark_session: SparkSession = None,
    ):
        super().__init__()
        self.supported_source_types = ["polars", "pandas", "pyspark", "csv", "parquet"]
        self.source_type = source_type
        self.file_path = file_path
        self.spark_session = spark_session
        self.check_source()
        self.raw_df = dataframe
        self.dataframe = self.convert_all_to_polars(self.raw_df)

    def check_source(self):
        if self.source_type not in self.supported_source_types:
            raise ValueError(
                "Source type must be one of: " + str(self.supported_source_types)
            )
        if self.source_type in ["csv", "parquet"] and self.file_path is None:
            raise ValueError("File path must be provided for csv and parquet sources")

    def convert_all_to_polars(self, df: object) -> pl.DataFrame:
        if self.source_type == "polars":
            return df.lazy()
        elif self.source_type == "pandas":
            return pl.from_pandas(data=df).lazy()
        elif self.source_type == "pyspark":
            return pl.from_pandas(df.toPandas()).lazy()
        elif self.source_type == "csv":
            return pl.scan_csv(self.file_path, infer_schema_length=10000)
        elif self.source_type == "parquet":
            return pl.scan_parquet(self.file_path)
        # TODO: add support for s3, gcs, etc.
