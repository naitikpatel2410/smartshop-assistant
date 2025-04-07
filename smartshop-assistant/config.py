import os

uri = os.getenv("DATABASE_URL", "postgres://u9in8d2gip7r00:p943f03b75821760deb5a9288f375bd4642372e9f8e97d97b3db3236c56444eb4@cb5ajfjosdpmil.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d2k6atf2cv0m7k")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

class Config:
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
