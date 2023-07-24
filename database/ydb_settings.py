import os

import ydb


ydb_driver_config = ydb.DriverConfig(
    os.getenv("YDB_ENDPOINT"), os.getenv("YDB_DATABASE"),
    credentials=ydb.credentials_from_env_variables(),
    root_certificates=ydb.load_ydb_root_certificate(),
)

ydb_driver = ydb.Driver(ydb_driver_config)
ydb_driver.wait(fail_fast=True, timeout=30)
pool = ydb.SessionPool(ydb_driver)
