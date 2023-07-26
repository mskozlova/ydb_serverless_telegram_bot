export function_id="<YOUR FUNCTION ID>"
export service_account_id="<YOUR SERVICE ACCOUNT ID>"
export ydb_database="<YOUR YDB DATABASE CONNECTION>"
export ydb_endpoint="<YOUR YDB ENDPOINT>"
export bot_token="<YOUR BOT TOKEN>"

zip code *.py *.md *.txt database/* user_interaction/* bot/* tests/*.py &&
yc serverless function version create \
    --function-id="$function_id" \
    --runtime python311 \
    --entrypoint index.handler \
    --memory 128m \
    --execution-timeout 40s \
    --source-path code.zip \
    --service-account-id="$service_account_id" \
    --environment YDB_DATABASE="$ydb_database" \
    --environment YDB_ENDPOINT="$ydb_endpoint" \
    --environment BOT_TOKEN="$bot_token"
