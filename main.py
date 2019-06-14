from Flask import Flask
from google.cloud import bigquery


app = Flask(__name__)


@app.route('/')
def hello():
    client = bigquery.Client()
    sql = """
    #standardSQL
    SELECT
    *
    FROM
    ml.PREDICT(MODEL `msds-434-analytics-app.house_analytics`.house_price_model2,
    (

    #standardSQL
    WITH params AS (
        SELECT
        1 AS TRAIN,
        2 AS EVAL
        ),

    house_sales AS (
    SELECT
        bedrooms,
        bathrooms,
        sqft_living,
        sqft_lot,
        waterfront,
        condition,
        grade,
        yr_built,
        zipcode,
        price
    FROM
        `msds-434-analytics-app.house_analytics.kc_house_data_clean`, params
    WHERE
        price > 0 AND bedrooms < 6
        AND MOD(ABS(FARM_FINGERPRINT(CAST(id AS STRING))),1000) = params.EVAL
    )


    SELECT *
    FROM house_sales
    ))
    """
    # Run a Standard SQL query using the environment's default project
    df = client.query(sql).to_dataframe()

    # Run a Standard SQL query with the project set explicitly
    project_id = 'msds-434-analytics-app'
    df = client.query(sql, project=project_id).to_dataframe()
    return df


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)
