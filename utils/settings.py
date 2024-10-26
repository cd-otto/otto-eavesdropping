import json
import os
from functools import cached_property
from typing import Any

import boto3
from dotenv import load_dotenv, dotenv_values
from pydantic_settings import BaseSettings
from datetime import timedelta

load_dotenv()


class Settings(BaseSettings):
    OTTO_ENV: str = os.getenv("OTTO_ENV")

    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def secrets_manager(self) -> Any:
        return boto3.client(service_name='secretsmanager')

    @cached_property
    def aws_secrets_dict(self) -> dict[str, Any]:
        secret_name: str = f"otto-server-{self.OTTO_ENV.lower()}"
        aws_secret: dict[str, str] = self.secrets_manager.get_secret_value(SecretId=secret_name)  # noqa

        if "SecretString" in aws_secret:
            secret_data_str: str = aws_secret["SecretString"]
            secret_data = json.loads(secret_data_str)
            return secret_data

        return {}

    @cached_property
    def all_secrets_dict(self) -> dict[str, Any]:
        env_secrets = dotenv_values()

        return {**self.aws_secrets_dict, **env_secrets}

    @property
    def OTTO_APP_SECRET(self) -> str:
        return self.all_secrets_dict.get("OTTO_APP_SECRET")

    @property
    def PG_USER(self) -> str:
        return self.all_secrets_dict.get("PG_USER")

    @property
    def PG_PASSWORD(self) -> str:
        return self.all_secrets_dict.get("PG_PASSWORD")

    @property
    def PG_HOST(self) -> str:
        return self.all_secrets_dict.get("PG_HOST")

    @property
    def PG_PORT(self) -> str:
        return self.all_secrets_dict.get("PG_PORT")

    @property
    def PG_DATABASE(self) -> str:
        return self.all_secrets_dict.get("PG_DATABASE")

    @property
    def GOOGLE_CLIENT_ID(self) -> str:
        return self.all_secrets_dict.get("GOOGLE_CLIENT_ID")

    @property
    def GOOGLE_MOBILE_CLIENT_ID(self) -> str:
        return self.all_secrets_dict.get("GOOGLE_MOBILE_CLIENT_ID")

    @property
    def GOOGLE_CLIENT_SECRET(self) -> str:
        return self.all_secrets_dict.get("GOOGLE_CLIENT_SECRET")

    @property
    def SERVER_DNS(self) -> str:
        return self.all_secrets_dict.get("SERVER_DNS")

    @property
    def OPENAI_API_KEY(self) -> str:
        return self.all_secrets_dict.get("OPENAI_API_KEY")

    @property
    def MONGO_USER(self) -> str:
        return self.all_secrets_dict.get("MONGO_USER")

    @property
    def MONGO_PASSWORD(self) -> str:
        return self.all_secrets_dict.get("MONGO_PASSWORD")

    @property
    def MONGO_HOST(self) -> str:
        return self.all_secrets_dict.get("MONGO_HOST")

    @property
    def MONGO_PORT(self) -> str:
        return self.all_secrets_dict.get("MONGO_PORT")

    @property
    def MONGO_DATABASE(self) -> str:
        return self.all_secrets_dict.get("MONGO_DATABASE")

    @property
    def ALLOWED_DOMAINS(self) -> str:
        return self.all_secrets_dict.get("ALLOWED_DOMAINS")

    @property
    def COOKIES_DOMAIN(self) -> str:
        return self.all_secrets_dict.get("COOKIES_DOMAIN")

    @property
    def LOG_GROUP_NAME(self) -> str:
        return self.all_secrets_dict.get("LOG_GROUP_NAME")

    @property
    def CLOUDWATCH_METRICS_NAMESPACE(self) -> str:
        return self.all_secrets_dict.get("CLOUDWATCH_METRICS_NAMESPACE")

    @property
    def GOOGLE_MAPS_API_KEY(self) -> str:
        return self.all_secrets_dict.get("GOOGLE_MAPS_API_KEY")

    @property
    def SPOTNANA_HOST(self) -> str:
        return self.all_secrets_dict.get("SPOTNANA_HOST")

    @property
    def SPOTNANA_CLIENT_ID(self) -> str:
        return self.all_secrets_dict.get("SPOTNANA_CLIENT_ID")

    @property
    def ANDROID_AUTH_KEY(self) -> str:
        return self.all_secrets_dict.get("ANDROID_AUTH_KEY")

    @property
    def IOS_AUTH_KEY(self) -> str:
        return self.all_secrets_dict.get("IOS_AUTH_KEY")

    @property
    def APP_ID_IOS(self) -> str:
        return self.all_secrets_dict.get("APP_ID_IOS")

    @property
    def APP_ID_ANDROID(self) -> str:
        return self.all_secrets_dict.get("APP_ID_ANDROID")

    @property
    def SPOTNANA_CLIENT_SECRET(self) -> str:
        return self.all_secrets_dict.get("SPOTNANA_CLIENT_SECRET")

    @property
    def SPOTNANA_COMPANY_GUID(self) -> str:
        return self.all_secrets_dict.get("SPOTNANA_COMPANY_GUID")

    @property
    def SPOTNANA_COMPANY_LEGAL_ID(self) -> str:
        return self.all_secrets_dict.get("SPOTNANA_COMPANY_LEGAL_ID")

    @property
    def SPOTNANA_USER_GUID(self) -> str:
        return self.all_secrets_dict.get("SPOTNANA_USER_GUID")

    @property
    def SPOTNANA_API_KEY(self) -> str:
        return self.all_secrets_dict.get("SPOTNANA_API_KEY")

    @property
    def SPOTNANA_VGS_HOST(self) -> str:
        return self.all_secrets_dict.get("SPOTNANA_VGS_HOST")

    @property
    def OTTO_VGS_INBOUND_HOST(self) -> str:
        return self.all_secrets_dict.get("OTTO_VGS_INBOUND_HOST")

    @property
    def OTTO_VGS_OUTBOUND_HOST(self) -> str:
        return self.all_secrets_dict.get("OTTO_VGS_OUTBOUND_HOST")

    @property
    def BOOKING_DOT_COM_API_KEY(self) -> str:
        return self.all_secrets_dict.get("BOOKING_DOT_COM_API_KEY")

    @property
    def BOOKING_DOT_COM_AFFILIATE_ID(self) -> str:
        return self.all_secrets_dict.get("BOOKING_DOT_COM_AFFILIATE_ID")


settings = Settings()
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

