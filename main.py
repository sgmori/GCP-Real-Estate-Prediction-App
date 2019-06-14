# [START gae_python37_render_template]
import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def predict_model():
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
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
