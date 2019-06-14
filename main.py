# [START gae_python37_bigquery]
import concurrent.futures

import flask
from google.cloud import bigquery


app = flask.Flask(__name__)
bigquery_client = bigquery.Client()


@app.route("/")
def main():
    query_job = bigquery_client.query(
        """
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
    )

    return flask.redirect(
        flask.url_for(
            "results",
            project_id=query_job.project,
            job_id=query_job.job_id,
            location=query_job.location,
        )
    )


@app.route("/results")
def results():
    project_id = flask.request.args.get("project_id")
    job_id = flask.request.args.get("job_id")
    location = flask.request.args.get("location")

    query_job = bigquery_client.get_job(
        job_id,
        project=project_id,
        location=location,
    )

    try:
        # Set a timeout because queries could take longer than one minute.
        results = query_job.result(timeout=30)
    except concurrent.futures.TimeoutError:
        return flask.render_template("timeout.html", job_id=query_job.job_id)

    return flask.render_template("query_result.html", results=results)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_python37_bigquery]
