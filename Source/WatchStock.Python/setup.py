#!python
#cython: language_level=3

from config import Config

import shioaji as sj

if __name__ == "__main__":
    config = Config();

    api = sj.Shioaji()

    accounts = api.login(config.account, config.password)

    api.activate_ca(
        ca_path="Sinopac.pfx",
        ca_passwd=config.account,
        person_id=config.account,
    )


