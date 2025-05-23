CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA IF NOT EXISTS bedrock_integration;
CREATE ROLE bedrock_user LOGIN;
ALTER ROLE bedrock_user WITH PASSWORD 'bedrock_user';
GRANT ALL ON SCHEMA bedrock_integration to bedrock_user;
SET SESSION AUTHORIZATION bedrock_user;
CREATE TABLE bedrock_integration.bedrock_kb (
  id uuid PRIMARY KEY,
  embedding vector(1024),
  chunks text,
  metadata json
);
GRANT ALL ON TABLE bedrock_integration.bedrock_kb to bedrock_user;
CREATE INDEX ON bedrock_integration.bedrock_kb
  USING hnsw (embedding vector_cosine_ops);